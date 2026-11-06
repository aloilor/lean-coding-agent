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

async function assertBaselinesMatchBundledReferences(project) {
  for (const filename of ['AGENTS.md', 'CLAUDE.md']) {
    const installed = await fs.readFile(path.join(project, filename), 'utf8');
    const bundled = await fs.readFile(
      path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent', 'references', 'baseline', filename),
      'utf8',
    );
    assert.equal(installed, bundled, `${filename} matches the bundled baseline`);
    assert.doesNotMatch(installed, /Do Not Edit This Baseline File|Under no circumstances edit/);
  }
}

test('setup initializes project files and preserves project-owned content on rerun', async (t) => {
  const { project, commandLog, env } = await setupFixture(t);
  await fs.writeFile(path.join(project, 'package.json'), '{"packageManager":"pnpm@9.0.0"}\n');
  await fs.writeFile(path.join(project, 'AGENTS.override.md'), 'Private notes\n');
  await fs.writeFile(path.join(project, '.gitignore'), '# Existing rules\nnode_modules/\n');
  const overrideDirectory = path.join(project, '.agents', 'skill-overrides');
  await fs.mkdir(overrideDirectory, { recursive: true });
  await fs.writeFile(path.join(overrideDirectory, 'INDEX.md'), '# Skill Overrides\n\n- [custom](custom.md) - project rule.\n');

  const options = [
    setupScript,
    project,
    '--tools', 'both',
    '--planner-model', 'gpt-6-astra',
    '--bug-diagnostician-model', 'gpt-6-sol',
    '--implementer-model', 'gpt-6-astra',
    '--code-reviewer-model', 'gpt-6-sol',
    '--claude-planner-model', 'opus',
  ];
  await runFile(process.execPath, options, { env });

  await assertBaselinesMatchBundledReferences(project);

  for (const relativePath of [
    'AGENTS.md',
    'CLAUDE.md',
    'AGENTS.override.md',
    '.agents/lessons/LESSONS.md',
    '.agents/skill-overrides/tdd.md',
    '.codex/config.toml',
    '.codex/agents/planner.toml',
    '.codex/agents/bug-diagnostician.toml',
    '.codex/agents/implementer.toml',
    '.codex/agents/code-reviewer.toml',
    '.codex/agents/explorer.toml',
    '.claude/agents/planner.md',
    '.claude/agents/bug-diagnostician.md',
    '.claude/agents/implementer.md',
    '.claude/agents/code-reviewer.md',
    '.claude/agents/explorer.md',
    'docs/incidents/README.md',
  ]) {
    assert.ok((await fs.stat(path.join(project, relativePath))).isFile(), relativePath);
  }
  await assert.rejects(fs.access(path.join(project, '.agents', 'skills')), { code: 'ENOENT' });

  const planner = await fs.readFile(path.join(project, '.codex', 'agents', 'planner.toml'), 'utf8');
  const implementer = await fs.readFile(path.join(project, '.codex', 'agents', 'implementer.toml'), 'utf8');
  assert.match(planner, /^model = "gpt-6-astra"$/m);
  assert.match(planner, /^model_reasoning_effort = "low"$/m);
  assert.match(implementer, /^model = "gpt-6-astra"$/m);
  assert.match(implementer, /^model_reasoning_effort = "xhigh"$/m);
  const claudePlanner = await fs.readFile(path.join(project, '.claude', 'agents', 'planner.md'), 'utf8');
  const claudeImplementer = await fs.readFile(path.join(project, '.claude', 'agents', 'implementer.md'), 'utf8');
  assert.match(claudePlanner, /^model: opus$/m);
  assert.match(claudeImplementer, /^model: haiku$/m);
  assert.equal(
    await fs.readFile(path.join(project, '.codex', 'config.toml'), 'utf8'),
    await fs.readFile(path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent', 'references', 'config.toml'), 'utf8'),
  );

  const firstCommands = await loggedCommands(commandLog);
  assert.deepEqual(firstCommands.map(({ command }) => command), ['pnpm', 'pnpm', 'npx', 'npx', 'npx', 'npx', 'npx']);
  assert.deepEqual(firstCommands[0].args, ['add', '--save-dev', 'agent-browser@latest']);
  assert.deepEqual(firstCommands[1].args, ['exec', '--', 'agent-browser', 'install']);
  assert.deepEqual(firstCommands.slice(2).map(({ args }) => args), [
    ['skills', 'add', 'https://github.com/vercel-labs/agent-browser', '--skill', 'agent-browser', '--agent', 'codex', 'claude-code', '--copy', '-y'],
    ['skills', 'add', 'https://github.com/mattpocock/skills', '--skill', 'handoff', 'tdd', '--agent', 'codex', 'claude-code', '--copy', '-y'],
    ['skills', 'add', 'https://github.com/github/awesome-copilot', '--skill', 'refactor', '--agent', 'codex', 'claude-code', '--copy', '-y'],
    ['skills', 'add', 'https://github.com/anthropics/claude-plugins-community', '--skill', 'eli5', '--agent', 'codex', 'claude-code', '--copy', '-y'],
    ['skills', 'add', 'https://github.com/anthropics/skills', '--skill', 'skill-creator', '--agent', 'codex', 'claude-code', '--copy', '-y'],
  ]);
  assert.ok(firstCommands.every(({ cwd }) => cwd === project));

  await fs.writeFile(path.join(project, 'AGENTS.md'), 'Outdated managed baseline\n');
  await fs.writeFile(path.join(project, 'CLAUDE.md'), 'Outdated managed baseline\n');
  await fs.writeFile(path.join(project, '.codex', 'config.toml'), 'model = "project-choice"\n');
  await fs.writeFile(path.join(overrideDirectory, 'tdd.md'), 'Outdated managed override\n');
  await runFile(process.execPath, options, { env });
  await assert.rejects(fs.stat(path.join(project, 'docs', 'conventions')), { code: 'ENOENT' });

  await assertBaselinesMatchBundledReferences(project);
  assert.equal(await fs.readFile(path.join(project, 'AGENTS.override.md'), 'utf8'), 'Private notes\n');
  assert.equal(await fs.readFile(path.join(project, '.codex', 'config.toml'), 'utf8'), 'model = "project-choice"\n');
  const overrideIndex = await fs.readFile(path.join(overrideDirectory, 'INDEX.md'), 'utf8');
  assert.match(overrideIndex, /- \[custom\]\(custom\.md\)/);
  assert.equal((overrideIndex.match(/- \[tdd\]\(tdd\.md\)/g) ?? []).length, 1);
  assert.equal(
    await fs.readFile(path.join(overrideDirectory, 'tdd.md'), 'utf8'),
    await fs.readFile(path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent', 'references', 'skill-overrides', 'tdd.md'), 'utf8'),
  );
  const ignoreRules = await fs.readFile(path.join(project, '.gitignore'), 'utf8');
  assert.match(ignoreRules, /^AGENTS\.override\.md$/m);
  assert.equal((ignoreRules.match(/^node_modules\/$/gm) ?? []).length, 1);
  assert.equal((await loggedCommands(commandLog)).length, 14);
});

test('setup preserves installed skills and the CLI lock on rerun', async (t) => {
  const { project, env } = await setupFixture(t);
  const skillsDirectory = path.join(project, '.agents', 'skills');
  const skillContents = {
    'setup-lean-coding-agent': 'CLI-installed baseline skill\n',
    'retired-skill': 'Previously copied skill\n',
    'project-skill': 'Project-owned skill\n',
  };
  for (const [name, contents] of Object.entries(skillContents)) {
    await fs.mkdir(path.join(skillsDirectory, name), { recursive: true });
    await fs.writeFile(path.join(skillsDirectory, name, 'SKILL.md'), contents);
  }
  const lockPath = path.join(project, 'skills-lock.json');
  const lock = '{"version":1,"skills":{}}\n';
  await fs.writeFile(lockPath, lock);

  for (let pass = 0; pass < 2; pass += 1) {
    await runFile(process.execPath, [setupScript, project], { env });
    for (const [name, contents] of Object.entries(skillContents)) {
      assert.equal(await fs.readFile(path.join(skillsDirectory, name, 'SKILL.md'), 'utf8'), contents);
    }
    assert.equal(await fs.readFile(lockPath, 'utf8'), lock);
  }
});

test('setup for Claude Code only installs Claude Code agents and skills without Codex files', async (t) => {
  const { project, commandLog, env } = await setupFixture(t);

  await runFile(process.execPath, [setupScript, project, '--tools', 'claude-code'], { env });

  for (const agentName of ['planner', 'bug-diagnostician', 'implementer', 'code-reviewer', 'explorer']) {
    const installed = await fs.readFile(path.join(project, '.claude', 'agents', `${agentName}.md`), 'utf8');
    const expectedModel = ['planner', 'code-reviewer'].includes(agentName) ? 'opus' : 'haiku';
    assert.match(installed, new RegExp(`^model: ${expectedModel}$`, 'm'));
  }
  await assert.rejects(fs.access(path.join(project, '.codex')), { code: 'ENOENT' });
  const skillCommands = (await loggedCommands(commandLog)).filter(({ command }) => command === 'npx');
  assert.equal(skillCommands.length, 5);
  for (const { args } of skillCommands) {
    assert.deepEqual(args.slice(args.indexOf('--agent')), ['--agent', 'claude-code', '--copy', '-y']);
  }
});

test('setup installs shared artifact templates for each tool selection and refreshes only managed templates on rerun', async (t) => {
  for (const tools of ['codex', 'claude-code', 'both']) {
    const { project, env } = await setupFixture(t);
    const options = [setupScript, project, '--tools', tools];
    await runFile(process.execPath, options, { env });
    await assertBaselinesMatchBundledReferences(project);
    const templateDirectory = path.join(project, '.agents', 'templates');
    const installedNames = await fs.readdir(templateDirectory).catch((error) => {
      if (error.code === 'ENOENT') return [];
      throw error;
    });
    assert.deepEqual(installedNames.sort(), ['code-review.md', 'implementation-report.md', 'plan.md'], tools);

    for (const name of installedNames) {
      const source = path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent', 'references', 'templates', name);
      assert.equal(await fs.readFile(path.join(templateDirectory, name), 'utf8'), await fs.readFile(source, 'utf8'));
      await fs.writeFile(path.join(templateDirectory, name), 'Outdated managed template\n');
    }
    await fs.writeFile(path.join(templateDirectory, 'project-template.md'), 'Project-owned template\n');
    await runFile(process.execPath, options, { env });
    for (const name of installedNames) {
      const source = path.join(repositoryRoot, 'skills', 'setup-lean-coding-agent', 'references', 'templates', name);
      assert.equal(await fs.readFile(path.join(templateDirectory, name), 'utf8'), await fs.readFile(source, 'utf8'));
    }
    assert.equal(await fs.readFile(path.join(templateDirectory, 'project-template.md'), 'utf8'), 'Project-owned template\n');

    const selectedTools = tools === 'both' ? ['codex', 'claude-code'] : [tools];
    for (const tool of selectedTools) {
      const directory = tool === 'codex' ? '.codex' : '.claude';
      const extension = tool === 'codex' ? '.toml' : '.md';
      for (const [agent, template] of [['planner', 'plan'], ['implementer', 'implementation-report'], ['code-reviewer', 'code-review']]) {
        const contents = await fs.readFile(path.join(project, directory, 'agents', `${agent}${extension}`), 'utf8');
        assert.ok(contents.includes(`.agents/templates/${template}.md`), `${tool} ${agent} references its installed template`);
      }
    }
  }
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

test('setup with --docs-dir points lean-grill-with-docs at the chosen folder and updates it on rerun', async (t) => {
  const { project, env } = await setupFixture(t);
  const overrideDirectory = path.join(project, '.agents', 'skill-overrides');
  const overridePath = path.join(overrideDirectory, 'lean-grill-with-docs.md');

  await runFile(process.execPath, [setupScript, project, '--docs-dir', 'docs\\domain/'], { env });

  const override = await fs.readFile(overridePath, 'utf8');
  assert.ok(override.includes('`docs/domain/GLOSSARY.md` replaces `docs/conventions/GLOSSARY.md`'));
  assert.ok(override.includes('`docs/domain/GLOSSARY-MAP.md` replaces `docs/conventions/GLOSSARY-MAP.md`'));
  assert.ok(override.includes('`docs/domain/adr/` replaces `docs/conventions/adr/`'));

  await runFile(process.execPath, [setupScript, project, '--docs-dir', 'knowledge'], { env });

  assert.ok((await fs.readFile(overridePath, 'utf8')).includes('`knowledge/adr/` replaces `docs/conventions/adr/`'));
  const index = await fs.readFile(path.join(overrideDirectory, 'INDEX.md'), 'utf8');
  assert.equal((index.match(/^- \[lean-grill-with-docs\]\(lean-grill-with-docs\.md\)/gm) ?? []).length, 1);
  assert.match(index, /^- \[tdd\]\(tdd\.md\)/m);

  await runFile(process.execPath, [setupScript, project], { env });
  assert.ok((await fs.readFile(overridePath, 'utf8')).includes('`knowledge/adr/`'), 'rerun without --docs-dir keeps the folder');

  await runFile(process.execPath, [setupScript, project, '--docs-dir', 'docs/conventions/'], { env });
  await assert.rejects(fs.access(overridePath), { code: 'ENOENT' });
  const restoredIndex = await fs.readFile(path.join(overrideDirectory, 'INDEX.md'), 'utf8');
  assert.doesNotMatch(restoredIndex, /lean-grill-with-docs/);
  assert.match(restoredIndex, /^- \[tdd\]\(tdd\.md\)/m);
});

test('setup without --docs-dir does not add a lean-grill-with-docs override', async (t) => {
  const { project, env } = await setupFixture(t);

  await runFile(process.execPath, [setupScript, project], { env });

  const localInstructions = await fs.readFile(path.join(project, 'AGENTS.override.md'), 'utf8');
  assert.match(localInstructions, /Read `AGENTS\.md` in this directory/);
  await assert.rejects(fs.access(path.join(project, 'AGENTS.local.md')), { code: 'ENOENT' });

  const overrideDirectory = path.join(project, '.agents', 'skill-overrides');
  await assert.rejects(fs.access(path.join(overrideDirectory, 'lean-grill-with-docs.md')), { code: 'ENOENT' });
  assert.doesNotMatch(await fs.readFile(path.join(overrideDirectory, 'INDEX.md'), 'utf8'), /lean-grill-with-docs/);
});

test('setup with --docs-dir preserves a project-owned lean-grill-with-docs override', async (t) => {
  const { project, env } = await setupFixture(t);
  const overrideDirectory = path.join(project, '.agents', 'skill-overrides');
  await fs.mkdir(overrideDirectory, { recursive: true });
  await fs.writeFile(path.join(overrideDirectory, 'lean-grill-with-docs.md'), 'Project-owned override\n');

  await assert.rejects(
    runFile(process.execPath, [setupScript, project, '--docs-dir', 'docs/domain'], { env }),
    (error) => {
      assert.match(error.stderr, /lean-grill-with-docs\.md is project-owned/);
      return true;
    },
  );
  assert.equal(await fs.readFile(path.join(overrideDirectory, 'lean-grill-with-docs.md'), 'utf8'), 'Project-owned override\n');
});

test('setup rejects a --docs-dir outside the target project before changing it', async (t) => {
  for (const docsDirectory of ['../shared-docs', '/abs/docs', 'C:\\docs', '.', 'docs/../..']) {
    const { project, env } = await setupFixture(t);

    await assert.rejects(
      runFile(process.execPath, [setupScript, project, '--docs-dir', docsDirectory], { env }),
      (error) => {
        assert.match(error.stderr, /Invalid --docs-dir value/, docsDirectory);
        return true;
      },
    );
    assert.deepEqual(await fs.readdir(project), [], docsDirectory);
  }
});
