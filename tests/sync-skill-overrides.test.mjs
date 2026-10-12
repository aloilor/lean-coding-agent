import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promises as fs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';

const runFile = promisify(execFile);
const repositoryRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = 'skills/skill-overrides';
const mirror = 'skills/setup-lean-coding-agent/references/skill-overrides';

async function hookFixture(t) {
  const project = await fs.mkdtemp(path.join(os.tmpdir(), 'lean-coding-agent-overrides-'));
  t.after(() => fs.rm(project, { recursive: true, force: true }));
  const git = (...args) => runFile('git', args, { cwd: project });
  await git('init', '--quiet');
  await git('config', 'user.name', 'Test');
  await git('config', 'user.email', 'test@example.com');
  await git('config', 'core.autocrlf', 'false');
  await git('config', 'core.hooksPath', '.githooks');
  for (const file of ['scripts/sync-skill-overrides.mjs', '.githooks/pre-commit']) {
    await fs.mkdir(path.join(project, path.dirname(file)), { recursive: true });
    await fs.copyFile(path.join(repositoryRoot, file), path.join(project, file));
  }
  await fs.mkdir(path.join(project, source), { recursive: true });
  await fs.mkdir(path.join(project, mirror), { recursive: true });
  const write = (file, content) => fs.writeFile(path.join(project, file), content);
  const committed = async (file) => (await git('show', `HEAD:${file}`)).stdout;
  const committedFiles = async (directory) =>
    (await git('ls-tree', '--name-only', 'HEAD', `${directory}/`)).stdout.trim().split('\n').filter(Boolean);
  return { project, git, write, committed, committedFiles };
}

test('pre-commit hook mirrors added, edited, and deleted overrides into the commit', async (t) => {
  const { git, write, committed, committedFiles } = await hookFixture(t);
  await write(`${source}/tdd.md`, 'tdd v1\n');
  await write(`${mirror}/stale.md`, 'stale\n');
  await git('add', '--all');
  await git('commit', '--quiet', '-m', 'add');
  assert.equal(await committed(`${mirror}/tdd.md`), 'tdd v1\n');
  assert.deepEqual(await committedFiles(mirror), [`${mirror}/tdd.md`]);

  await write(`${source}/tdd.md`, 'tdd v2\n');
  await git('add', '--all');
  await git('commit', '--quiet', '-m', 'edit');
  assert.equal(await committed(`${mirror}/tdd.md`), 'tdd v2\n');

  await git('rm', '--quiet', `${source}/tdd.md`);
  await git('commit', '--quiet', '-m', 'delete');
  assert.deepEqual(await committedFiles(mirror), []);
});

test('pre-commit hook rejects unstaged override edits without changing the mirror', async (t) => {
  const { project, git, write } = await hookFixture(t);
  await write(`${source}/tdd.md`, 'tdd staged\n');
  await git('add', '--all');
  await write(`${source}/tdd.md`, 'tdd unstaged\n');

  await assert.rejects(git('commit', '--quiet', '-m', 'partial'), /Stage or stash/);
  await assert.rejects(fs.access(path.join(project, mirror, 'tdd.md')));
});

test('check mode reports drift and sync mode repairs it', async (t) => {
  const { project, write } = await hookFixture(t);
  const script = path.join(project, 'scripts', 'sync-skill-overrides.mjs');
  await write(`${source}/tdd.md`, 'tdd\n');
  await write(`${mirror}/tdd.md`, 'tdd\r\n');

  await assert.rejects(runFile(process.execPath, [script, '--check']), /tdd\.md/);
  await runFile(process.execPath, [script]);
  assert.equal(await fs.readFile(path.join(project, mirror, 'tdd.md'), 'utf8'), 'tdd\n');
  await runFile(process.execPath, [script, '--check']);
});
