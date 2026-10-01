import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { promises as fs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import {
  installCodexAgents,
  installUpdateChecker,
  syncInstalledSkills,
} from '../skills/setup-lean-coding-agent/scripts/setup-lean-coding-agent.mjs';

const runFile = promisify(execFile);
const repositoryRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const skillRoot = path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent');
const setupScript = path.join(skillRoot, 'scripts', 'setup-lean-coding-agent.mjs');

async function temporaryProject(t) {
  const project = await fs.mkdtemp(path.join(os.tmpdir(), 'lean-coding-agent-test-'));
  t.after(() => fs.rm(project, { recursive: true, force: true }));
  return project;
}

test('agent installation assigns selected models and preserves reasoning effort on rerun', async (t) => {
  const project = await temporaryProject(t);
  const firstModels = {
    planner: 'gpt-6-sol',
    'bug-diagnostician': 'gpt-6-luna',
    implementer: 'gpt-6-luna',
    'code-reviewer': 'gpt-6-luna',
  };
  const selectedModels = {
    planner: 'gpt-6-astra',
    'bug-diagnostician': 'gpt-6-sol',
    implementer: 'gpt-6-astra',
    'code-reviewer': 'gpt-6-sol',
  };

  await installCodexAgents(project, firstModels);
  const customAgent = path.join(project, '.codex', 'agents', 'custom.toml');
  await fs.writeFile(customAgent, 'name = "custom"\n');
  await installCodexAgents(project, selectedModels);

  for (const [agentName, model] of Object.entries(selectedModels)) {
    const installed = await fs.readFile(path.join(project, '.codex', 'agents', `${agentName}.toml`), 'utf8');
    const expectedEffort = ['planner', 'code-reviewer'].includes(agentName) ? 'max' : 'xhigh';
    assert.match(installed, new RegExp(`^model = "${model}"$`, 'm'));
    assert.match(installed, new RegExp(`^model_reasoning_effort = "${expectedEffort}"$`, 'm'));
  }
  assert.equal(await fs.readFile(customAgent, 'utf8'), 'name = "custom"\n');
});

test('installed skill sync refreshes managed copies and preserves project-owned skills on rerun', async (t) => {
  const project = await temporaryProject(t);
  await fs.mkdir(path.join(project, 'agent-context'));

  const firstSync = await syncInstalledSkills(project);
  const installedSkill = path.join(firstSync.skillDirectory, 'setup-lean-coding-agent', 'SKILL.md');
  const sourceSkill = path.join(skillRoot, 'SKILL.md');
  const customSkill = path.join(firstSync.skillDirectory, 'project-skill', 'SKILL.md');
  await fs.mkdir(path.dirname(customSkill));
  await fs.writeFile(customSkill, 'Project-owned skill\n');
  await fs.writeFile(installedSkill, 'Local edit to a managed skill\n');

  const secondSync = await syncInstalledSkills(project);
  const manifest = JSON.parse(await fs.readFile(path.join(project, 'agent-context', 'skills-installed.json'), 'utf8'));
  const release = JSON.parse(await fs.readFile(path.join(skillRoot, 'references', 'release.json'), 'utf8'));

  assert.equal(await fs.readFile(installedSkill, 'utf8'), await fs.readFile(sourceSkill, 'utf8'));
  assert.equal(await fs.readFile(customSkill, 'utf8'), 'Project-owned skill\n');
  assert.equal(secondSync.skillCount, firstSync.skillCount);
  assert.equal(manifest.version, release.version);
  assert.equal(manifest.repository, release.repository);
  assert.ok(manifest.skills.some(({ installed_as }) => installed_as === 'setup-lean-coding-agent'));
  assert.ok(!manifest.skills.some(({ installed_as }) => installed_as === 'project-skill'));
});

test('update checker installation removes legacy hooks and preserves unrelated hooks on rerun', async (t) => {
  const project = await temporaryProject(t);
  const codexDirectory = path.join(project, '.codex');
  const legacyDirectory = path.join(codexDirectory, 'hooks', 'lean-coding-agent');
  await fs.mkdir(legacyDirectory, { recursive: true });
  const legacyScript = path.join(legacyDirectory, 'check-skill-updates.mjs');
  await fs.writeFile(legacyScript, 'old checker\n');

  const hooksPath = path.join(codexDirectory, 'hooks.json');
  const hooks = {
    hooks: {
      SessionStart: [{
        hooks: [
          { command: 'node .codex/hooks/lean-coding-agent/check-skill-updates.mjs' },
          { command: 'node scripts/unrelated-check.mjs' },
        ],
      }],
      AfterToolUse: [{ hooks: [{ command: 'node scripts/after-tool.mjs' }] }],
    },
  };
  await fs.writeFile(hooksPath, JSON.stringify(hooks));

  const configPath = path.join(codexDirectory, 'config.toml');
  await fs.writeFile(configPath, [
    'model = "gpt-6-sol"',
    '# Lean Coding Agent session-start version check',
    '[[hooks.SessionStart]]',
    'command = "node .codex/hooks/lean-coding-agent/check-skill-updates.mjs"',
    'timeout = 10',
    '',
  ].join('\n'));

  const firstInstall = await installUpdateChecker(project);
  const firstHooks = await fs.readFile(hooksPath, 'utf8');
  const firstConfig = await fs.readFile(configPath, 'utf8');
  await installUpdateChecker(project);

  assert.equal(
    await fs.readFile(firstInstall.checkerPath, 'utf8'),
    await fs.readFile(path.join(skillRoot, 'scripts', 'check-skill-updates.mjs'), 'utf8'),
  );
  assert.deepEqual(JSON.parse(firstHooks).hooks.SessionStart[0].hooks, [
    { command: 'node scripts/unrelated-check.mjs' },
  ]);
  assert.deepEqual(JSON.parse(firstHooks).hooks.AfterToolUse, hooks.hooks.AfterToolUse);
  assert.equal(firstConfig, 'model = "gpt-6-sol"\n');
  assert.equal(await fs.readFile(hooksPath, 'utf8'), firstHooks);
  assert.equal(await fs.readFile(configPath, 'utf8'), firstConfig);
  await assert.rejects(fs.access(legacyScript), { code: 'ENOENT' });
});

test('setup rejects an invalid model before changing the target project', async (t) => {
  const project = await temporaryProject(t);

  await assert.rejects(
    runFile(process.execPath, [setupScript, project, '--planner-model', 'invalid model']),
    (error) => {
      assert.match(error.stderr, /Invalid model ID for planner/);
      return true;
    },
  );
  assert.deepEqual(await fs.readdir(project), []);
});

test('setup rejects a missing target directory', async (t) => {
  const project = await temporaryProject(t);
  const missingTarget = path.join(project, 'missing');

  await assert.rejects(
    runFile(process.execPath, [setupScript, missingTarget]),
    (error) => {
      assert.match(error.stderr, /Target project does not exist:/);
      return true;
    },
  );
  assert.deepEqual(await fs.readdir(project), []);
});
