import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { promises as fs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { installAgents } from '../skills/setup-lean-coding-agent/scripts/setup-lean-coding-agent.mjs';

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
    explorer: 'gpt-6-luna',
  };
  const selectedModels = {
    planner: 'gpt-6-astra',
    'bug-diagnostician': 'gpt-6-sol',
    implementer: 'gpt-6-astra',
    'code-reviewer': 'gpt-6-sol',
    explorer: 'gpt-6-sol',
  };

  await installAgents(project, 'codex', firstModels);
  const customAgent = path.join(project, '.codex', 'agents', 'custom.toml');
  await fs.writeFile(customAgent, 'name = "custom"\n');
  await installAgents(project, 'codex', selectedModels);

  for (const [agentName, model] of Object.entries(selectedModels)) {
    const installed = await fs.readFile(path.join(project, '.codex', 'agents', `${agentName}.toml`), 'utf8');
    const expectedEffort = {
      planner: 'low',
      'bug-diagnostician': 'max',
      implementer: 'xhigh',
      'code-reviewer': 'low',
      explorer: 'high',
    }[agentName];
    assert.match(installed, new RegExp(`^model = "${model}"$`, 'm'));
    assert.match(installed, new RegExp(`^model_reasoning_effort = "${expectedEffort}"$`, 'm'));
  }
  assert.equal(await fs.readFile(customAgent, 'utf8'), 'name = "custom"\n');
});

test('Claude Code agent installation assigns selected models and preserves effort and custom agents', async (t) => {
  const project = await temporaryProject(t);
  const selectedModels = {
    planner: 'opus',
    'bug-diagnostician': 'inherit',
    implementer: 'sonnet',
    'code-reviewer': 'claude-opus-5-5',
    explorer: 'haiku',
  };
  const customAgent = path.join(project, '.claude', 'agents', 'custom.md');
  await fs.mkdir(path.dirname(customAgent), { recursive: true });
  await fs.writeFile(customAgent, '---\nname: custom\n---\n');

  await installAgents(project, 'claude-code', selectedModels);

  for (const [agentName, model] of Object.entries(selectedModels)) {
    const installed = await fs.readFile(path.join(project, '.claude', 'agents', `${agentName}.md`), 'utf8');
    const expectedEffort = {
      planner: 'low',
      'bug-diagnostician': 'xhigh',
      implementer: 'xhigh',
      'code-reviewer': 'low',
      explorer: 'high',
    }[agentName];
    assert.match(installed, new RegExp(`^---\r?\nname: ${agentName}\r?\n`));
    assert.match(installed, new RegExp(`^model: ${model}$`, 'm'));
    assert.match(installed, new RegExp(`^effort: ${expectedEffort}\r?$`, 'm'));
    assert.doesNotMatch(installed, /`\$[A-Za-z0-9-]+`/);
  }
  assert.equal(await fs.readFile(customAgent, 'utf8'), '---\nname: custom\n---\n');
});

test('setup rejects an invalid Claude Code model before changing the target project', async (t) => {
  const project = await temporaryProject(t);

  await assert.rejects(
    runFile(process.execPath, [setupScript, project, '--tools', 'both', '--claude-implementer-model', 'bad model']),
    (error) => {
      assert.match(error.stderr, /Invalid Claude Code model ID for implementer/);
      return true;
    },
  );
  assert.deepEqual(await fs.readdir(project), []);
});

test('setup rejects an unknown tool selection before changing the target project', async (t) => {
  const project = await temporaryProject(t);

  await assert.rejects(
    runFile(process.execPath, [setupScript, project, '--tools', 'cursor']),
    (error) => {
      assert.match(error.stderr, /Invalid --tools value/);
      return true;
    },
  );
  assert.deepEqual(await fs.readdir(project), []);
});

test('setup rejects an invalid model before changing the target project', async (t) => {
  const project = await temporaryProject(t);

  await assert.rejects(
    runFile(process.execPath, [setupScript, project, '--planner-model', 'invalid model']),
    (error) => {
      assert.match(error.stderr, /Invalid Codex model ID for planner/);
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
