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
const setupScript = path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent', 'scripts', 'setup-lean-coding-agent.mjs');

async function setupFixture(t) {
  const sandbox = await fs.mkdtemp(path.join(os.tmpdir(), 'lean-coding-agent-setup-'));
  t.after(() => fs.rm(sandbox, { recursive: true, force: true }));
  const project = path.join(sandbox, 'project');
  const binDirectory = path.join(sandbox, 'bin');
  const commandLog = path.join(sandbox, 'commands.jsonl');
  await fs.mkdir(project);
  await fs.mkdir(binDirectory);

  const shimPath = path.join(binDirectory, 'command-shim.cjs');
  await fs.writeFile(shimPath, [
    "const fs = require('node:fs');",
    "fs.appendFileSync(process.env.SETUP_COMMAND_LOG, JSON.stringify({ command: process.argv[2], args: process.argv.slice(3), cwd: process.cwd() }) + '\\n');",
    'if (process.env.SETUP_FAIL_COMMAND === process.argv[2]) process.exit(7);',
    '',
  ].join('\n'));

  for (const command of ['npm', 'pnpm', 'npx']) {
    const executable = path.join(binDirectory, process.platform === 'win32' ? `${command}.cmd` : command);
    const wrapper = process.platform === 'win32'
      ? `@echo off\r\n"${process.execPath}" "${shimPath}" "${command}" %*\r\n`
      : `#!/bin/sh\nexec "${process.execPath}" "${shimPath}" "${command}" "$@"\n`;
    await fs.writeFile(executable, wrapper, { mode: 0o755 });
  }

  const env = { ...process.env, SETUP_COMMAND_LOG: commandLog };
  const pathKey = Object.keys(env).find((key) => key.toLowerCase() === 'path') ?? 'PATH';
  env[pathKey] = binDirectory;
  return { project, commandLog, env };
}

async function loggedCommands(commandLog) {
  return (await fs.readFile(commandLog, 'utf8')).trim().split('\n').map((line) => JSON.parse(line));
}

test('setup initializes project files and preserves project-owned content on rerun', async (t) => {
  const { project, commandLog, env } = await setupFixture(t);
  await fs.writeFile(path.join(project, 'package.json'), '{"packageManager":"pnpm@9.0.0"}\n');
  await fs.writeFile(path.join(project, 'AGENTS.local.md'), 'Private notes\n');
  await fs.writeFile(path.join(project, '.gitignore'), '# Existing rules\nnode_modules/\n');
  await fs.mkdir(path.join(project, 'agent-context'));
  await fs.writeFile(path.join(project, 'agent-context', 'testing.md'), 'Project testing guidance\n');
  const overrideDirectory = path.join(project, '.agents', 'skill-overrides');
  await fs.mkdir(overrideDirectory, { recursive: true });
  await fs.writeFile(path.join(overrideDirectory, 'INDEX.md'), '# Skill Overrides\n\n- [custom](custom.md) - project rule.\n');

  const options = [
    setupScript,
    project,
    '--planner-model', 'gpt-6-astra',
    '--bug-diagnostician-model', 'gpt-6-sol',
    '--implementer-model', 'gpt-6-astra',
    '--code-reviewer-model', 'gpt-6-sol',
  ];
  await runFile(process.execPath, options, { env });

  for (const relativePath of [
    'AGENTS.md',
    'CLAUDE.md',
    'CLAUDE.local.md',
    '.agents/lessons/LESSONS.md',
    '.agents/skill-overrides/tdd.md',
    '.agents/skills/setup-lean-coding-agent/SKILL.md',
    '.codex/config.toml',
    '.codex/agents/planner.toml',
    '.codex/agents/bug-diagnostician.toml',
    '.codex/agents/implementer.toml',
    '.codex/agents/code-reviewer.toml',
    'docs/incidents/README.md',
    'agent-context/architecture.md',
    'agent-context/skills-installed.json',
    'scripts/check-skill-updates.mjs',
  ]) {
    assert.ok((await fs.stat(path.join(project, relativePath))).isFile(), relativePath);
  }

  const planner = await fs.readFile(path.join(project, '.codex', 'agents', 'planner.toml'), 'utf8');
  const implementer = await fs.readFile(path.join(project, '.codex', 'agents', 'implementer.toml'), 'utf8');
  assert.match(planner, /^model = "gpt-6-astra"$/m);
  assert.match(planner, /^model_reasoning_effort = "high"$/m);
  assert.match(implementer, /^model = "gpt-6-astra"$/m);
  assert.match(implementer, /^model_reasoning_effort = "xhigh"$/m);
  assert.equal(
    await fs.readFile(path.join(project, '.codex', 'config.toml'), 'utf8'),
    await fs.readFile(path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent', 'references', 'config.toml'), 'utf8'),
  );

  const firstCommands = await loggedCommands(commandLog);
  assert.deepEqual(firstCommands.map(({ command }) => command), ['pnpm', 'pnpm', 'npx', 'npx', 'npx', 'npx']);
  assert.deepEqual(firstCommands[0].args, ['add', '--save-dev', 'agent-browser@latest']);
  assert.deepEqual(firstCommands[1].args, ['exec', '--', 'agent-browser', 'install']);
  assert.deepEqual(firstCommands.slice(2).map(({ args }) => args), [
    ['skills', 'add', 'https://github.com/vercel-labs/agent-browser', '--skill', 'agent-browser', '--agent', 'codex', '--copy', '-y'],
    ['skills', 'add', 'https://github.com/mattpocock/skills', '--skill', 'handoff', 'resolving-merge-conflicts', 'tdd', '--agent', 'codex', '--copy', '-y'],
    ['skills', 'add', 'https://github.com/wshobson/agents', '--skill', 'changelog-automation', '--agent', 'codex', '--copy', '-y'],
    ['skills', 'add', 'https://github.com/github/awesome-copilot', '--skill', 'create-readme', 'refactor', '--agent', 'codex', '--copy', '-y'],
  ]);
  assert.ok(firstCommands.every(({ cwd }) => cwd === project));

  await fs.writeFile(path.join(project, 'AGENTS.md'), 'Outdated managed baseline\n');
  await fs.writeFile(path.join(project, '.codex', 'config.toml'), 'model = "project-choice"\n');
  await fs.writeFile(path.join(overrideDirectory, 'tdd.md'), 'Outdated managed override\n');
  await runFile(process.execPath, options, { env });

  assert.match(await fs.readFile(path.join(project, 'AGENTS.md'), 'utf8'), /## Do Not Edit This Baseline File/);
  assert.equal(await fs.readFile(path.join(project, 'AGENTS.local.md'), 'utf8'), 'Private notes\n');
  assert.equal(await fs.readFile(path.join(project, '.codex', 'config.toml'), 'utf8'), 'model = "project-choice"\n');
  assert.equal(await fs.readFile(path.join(project, 'agent-context', 'testing.md'), 'utf8'), 'Project testing guidance\n');
  const overrideIndex = await fs.readFile(path.join(overrideDirectory, 'INDEX.md'), 'utf8');
  assert.match(overrideIndex, /- \[custom\]\(custom\.md\)/);
  assert.equal((overrideIndex.match(/- \[tdd\]\(tdd\.md\)/g) ?? []).length, 1);
  assert.equal(
    await fs.readFile(path.join(overrideDirectory, 'tdd.md'), 'utf8'),
    await fs.readFile(path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent', 'references', 'skill-overrides', 'tdd.md'), 'utf8'),
  );
  const ignoreRules = await fs.readFile(path.join(project, '.gitignore'), 'utf8');
  assert.equal((ignoreRules.match(/^node_modules\/$/gm) ?? []).length, 1);
  assert.equal((await loggedCommands(commandLog)).length, 12);
});

test('setup reports installer failures and stops before later commands', async (t) => {
  const { project, commandLog, env } = await setupFixture(t);
  env.SETUP_FAIL_COMMAND = 'npm';

  await assert.rejects(
    runFile(process.execPath, [setupScript, project], { env }),
    (error) => {
      assert.match(error.stderr, /Could not install agent-browser@latest with npm \(exit code 7\)/);
      return true;
    },
  );
  assert.deepEqual((await loggedCommands(commandLog)).map(({ command }) => command), ['npm']);
});
