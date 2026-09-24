#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { constants as fsConstants, promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const skillDirectory = path.resolve(scriptDirectory, '..');
const pluginSkillsDirectory = path.resolve(skillDirectory, '..');
const referencesDirectory = path.join(skillDirectory, 'references');
const codebaseOnboardingReferencesDirectory = path.join(
  pluginSkillsDirectory,
  'codebase-onboarding',
  'references',
);
const releaseMetadataPath = path.join(referencesDirectory, 'release.json');
const updateCheckerSourcePath = path.join(scriptDirectory, 'check-skill-updates.mjs');
const agentNames = ['bug-diagnostician', 'implementer', 'code-reviewer'];
const defaultModel = 'gpt-6-luna';
const modelIdPattern = /^[A-Za-z0-9][A-Za-z0-9._:/-]*$/;
const modelAssignmentPattern = /^model\s*=\s*"[^"]*"\s*$/m;
const manifestName = 'skills-installed.json';
const agentContextDirectoryName = 'agent-context';
const agentsDirectoryName = '.agents';
const skillOverridesDirectoryName = 'skill-overrides';
const skillOverridesIndexName = 'INDEX.md';
const lessonsIndexName = 'LESSONS.md';
const projectUpdateHookMarker = '# Lean Coding Agent session-start version check';
const projectUpdateCheckerPath = 'scripts/check-skill-updates.mjs';
const legacyProjectUpdateHookScripts = [
  '.codex/hooks/lean-coding-agent/check-skill-updates.mjs',
  '.codex/hooks/lean-coding-agent/check_skill_updates.mjs',
];
const localFiles = ['AGENTS.local.md', 'CLAUDE.local.md'];
const ignoredAgentFiles = [
  '.agents/code-reviews/',
  '.agents/plans/',
  '.agents/implementation-reports/',
  '.agents/tasks/',
  '.codex/tasks/',
  'node_modules/',
];

const upstreamSkillGroups = [
  {
    source: 'https://github.com/vercel-labs/agent-browser',
    skills: ['agent-browser'],
  },
  {
    source: 'https://github.com/mattpocock/skills',
    skills: ['handoff', 'resolving-merge-conflicts', 'tdd'],
  },
  {
    source: 'https://github.com/wshobson/agents',
    skills: ['changelog-automation'],
  },
  {
    source: 'https://github.com/github/awesome-copilot',
    skills: [
      'create-readme',
      'refactor',
      'sql-code-review',
      'sql-optimization',
    ],
  },
];

const packageManagerCommands = {
  npm: ['npm', 'install', '--save-dev'],
  pnpm: ['pnpm', 'add', '--save-dev'],
  yarn: ['yarn', 'add', '--dev'],
  bun: ['bun', 'add', '--dev'],
};

const agentBrowserInstallCommands = {
  npm: ['npm', 'exec', '--', 'agent-browser', 'install'],
  pnpm: ['pnpm', 'exec', '--', 'agent-browser', 'install'],
  yarn: ['yarn', 'run', 'agent-browser', 'install'],
  bun: ['bun', 'run', 'agent-browser', 'install'],
};

function readOptions() {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      help: { type: 'boolean', short: 'h' },
      'bug-diagnostician-model': { type: 'string', default: defaultModel },
      'implementer-model': { type: 'string', default: defaultModel },
      'code-reviewer-model': { type: 'string', default: defaultModel },
    },
  });

  if (values.help) {
    console.log(
      [
        'Usage: node setup-lean-coding-agent.mjs [target-project] [options]',
        '',
        'Options:',
        `  --bug-diagnostician-model <id>  Model for bug-diagnostician (default ${defaultModel})`,
        `  --implementer-model <id>        Model for implementer (default ${defaultModel})`,
        `  --code-reviewer-model <id>      Model for code-reviewer (default ${defaultModel})`,
        '  -h, --help                      Show this help',
      ].join('\n'),
    );
    return null;
  }
  if (positionals.length > 1) {
    throw new Error('Provide at most one target project directory.');
  }

  return {
    targetProject: path.resolve(positionals[0] ?? process.cwd()),
    models: {
      'bug-diagnostician': values['bug-diagnostician-model'],
      implementer: values['implementer-model'],
      'code-reviewer': values['code-reviewer-model'],
    },
  };
}

async function pathExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch (error) {
    if (error.code === 'ENOENT') return false;
    throw error;
  }
}

async function requireDirectory(directoryPath, label) {
  const resolvedPath = path.resolve(directoryPath);
  let details;
  try {
    details = await fs.stat(resolvedPath);
  } catch (error) {
    if (error.code === 'ENOENT') throw new Error(`${label} does not exist: ${resolvedPath}`);
    throw error;
  }
  if (!details.isDirectory()) throw new Error(`${label} is not a directory: ${resolvedPath}`);
  return resolvedPath;
}

async function requiredReference(...parts) {
  const referencePath = path.join(referencesDirectory, ...parts);
  try {
    const details = await fs.stat(referencePath);
    if (!details.isFile()) throw new Error(`Required bundled setup reference is not a file: ${referencePath}`);
  } catch (error) {
    if (error.code === 'ENOENT') throw new Error(`Required bundled setup reference is missing: ${referencePath}`);
    throw error;
  }
  return referencePath;
}

async function readReleaseMetadata() {
  let releaseMetadata;
  try {
    releaseMetadata = JSON.parse(await fs.readFile(releaseMetadataPath, 'utf8'));
  } catch (error) {
    throw new Error(`Could not read setup skill release metadata: ${error.message}`);
  }
  if (
    !releaseMetadata
    || typeof releaseMetadata.version !== 'string'
    || typeof releaseMetadata.repository !== 'string'
  ) {
    throw new Error(`Setup skill release metadata is invalid: ${releaseMetadataPath}`);
  }
  return releaseMetadata;
}

function validateModels(models) {
  for (const [agentName, modelId] of Object.entries(models)) {
    if (!modelIdPattern.test(modelId)) {
      throw new Error(
        `Invalid model ID for ${agentName}: use letters, numbers, '.', '_', ':', '/', or '-'.`,
      );
    }
  }
}

function baselineGuardBlock(filename) {
  const localFilename = filename.replace('.md', '.local.md');
  return [
    '',
    '---',
    '',
    '## Do Not Edit This Baseline File',
    '',
    `**Under no circumstances edit \`${filename}\` or the other baseline file in this project.** These files are the shared agents baseline, copied in from the upstream agents repo, and any edits here are overwritten on the next sync.`,
    '',
    '- For project-specific rules that should be shared and committed, use `agent-context/`.',
    `- For local, private, machine-specific notes, use \`${localFilename}\` (git-ignored).`,
    '',
    'Change the baseline itself only in the upstream agents repo, not here.',
    '',
  ].join('\n');
}

async function copyBaselineFiles(targetProject) {
  const copiedPaths = [];
  for (const filename of ['AGENTS.md', 'CLAUDE.md']) {
    const sourcePath = await requiredReference('baseline', filename);
    const targetPath = path.join(targetProject, filename);
    const baselineText = await fs.readFile(sourcePath, 'utf8');
    const separator = baselineText.endsWith('\n') ? '' : '\n';
    await fs.writeFile(
      targetPath,
      `${baselineText}${separator}${baselineGuardBlock(filename)}`,
      'utf8',
    );
    copiedPaths.push(targetPath);
  }
  return copiedPaths;
}

function localFileContent(filename) {
  return [
    `# ${filename}`,
    '',
    'Local private notes for this project.',
    '',
    'This file is ignored by git and is safe for machine-specific notes.',
    '',
  ].join('\n');
}

async function ensureLocalFiles(targetProject) {
  const localPaths = [];
  for (const filename of localFiles) {
    const localPath = path.join(targetProject, filename);
    if (!(await pathExists(localPath))) {
      await fs.writeFile(localPath, localFileContent(filename), 'utf8');
    }
    localPaths.push(localPath);
  }
  return localPaths;
}

async function ensureLocalGitignore(targetProject) {
  const gitignorePath = path.join(targetProject, '.gitignore');
  const existing = (await pathExists(gitignorePath))
    ? await fs.readFile(gitignorePath, 'utf8')
    : '';
  const existingLines = new Set(existing.split(/\r?\n/));
  const managedLines = [...localFiles, ...ignoredAgentFiles];
  const missingLines = managedLines.filter((line) => !existingLines.has(line));
  if (missingLines.length > 0) {
    const separator = existing.length === 0 || existing.endsWith('\n') ? '' : '\n';
    await fs.writeFile(gitignorePath, `${existing}${separator}${missingLines.join('\n')}\n`, 'utf8');
  }
  return gitignorePath;
}

async function ensureCodexConfig(targetProject) {
  const configPath = path.join(targetProject, '.codex', 'config.toml');
  if (!(await pathExists(configPath))) {
    await fs.copyFile(await requiredReference('config.toml'), configPath);
  }
  return configPath;
}

async function installCodexAgents(targetProject, models) {
  const targetDirectory = path.join(targetProject, '.codex', 'agents');
  const installedPaths = [];
  await fs.mkdir(targetDirectory, { recursive: true });

  for (const agentName of agentNames) {
    const sourcePath = await requiredReference('agents', `${agentName}.toml`);
    const contents = await fs.readFile(sourcePath, 'utf8');
    if (!modelAssignmentPattern.test(contents)) {
      throw new Error(`Expected a model setting in bundled agent template: ${sourcePath}`);
    }
    const targetPath = path.join(targetDirectory, `${agentName}.toml`);
    const updatedContents = contents.replace(
      modelAssignmentPattern,
      `model = "${models[agentName]}"`,
    );
    await fs.writeFile(targetPath, updatedContents, 'utf8');
    installedPaths.push(targetPath);
  }
  return installedPaths;
}

async function ensureIncidentsReadme(targetProject) {
  const targetDirectory = path.join(targetProject, 'docs', 'incidents');
  const readmePath = path.join(targetDirectory, 'README.md');
  await fs.mkdir(targetDirectory, { recursive: true });
  if (!(await pathExists(readmePath))) {
    await fs.copyFile(await requiredReference('docs', 'incidents', 'README.md'), readmePath);
  }
  return readmePath;
}

async function ensureLessonsIndex(targetProject) {
  const lessonsDirectory = path.join(targetProject, agentsDirectoryName, 'lessons');
  const indexPath = path.join(lessonsDirectory, lessonsIndexName);
  await fs.mkdir(lessonsDirectory, { recursive: true });
  if (!(await pathExists(indexPath))) {
    await fs.writeFile(indexPath, '# Lessons\n\nAdd shared agent lessons here.\n', 'utf8');
  }
  return indexPath;
}

function indexEntryForSkill(indexText, skillName) {
  const prefix = `- [${skillName}](`;
  return indexText.split(/\r?\n/).find((line) => line.startsWith(prefix));
}

async function updateSkillOverrideIndex(targetIndexPath, sourceIndexPath) {
  const sourceText = await fs.readFile(sourceIndexPath, 'utf8');
  if (!(await pathExists(targetIndexPath))) {
    await fs.mkdir(path.dirname(targetIndexPath), { recursive: true });
    await fs.copyFile(sourceIndexPath, targetIndexPath);
    return;
  }

  let targetText = await fs.readFile(targetIndexPath, 'utf8');
  targetText = targetText
    .split(/\r?\n/)
    .filter((line) => line.trim() !== '- _No skill overrides yet._')
    .join('\n')
    .replace(/\s*$/, '\n');
  const missingEntries = [];
  for (const sourceLine of sourceText.split(/\r?\n/)) {
    const match = sourceLine.match(/^- \[([^)]+)\]\(/);
    if (match && !indexEntryForSkill(targetText, match[1])) missingEntries.push(sourceLine);
  }
  if (missingEntries.length === 0) {
    await fs.writeFile(targetIndexPath, targetText, 'utf8');
    return;
  }

  if (!targetText.includes('## Baseline Overrides')) {
    targetText = `${targetText.trimEnd()}\n\n## Baseline Overrides\n\n`;
  }
  await fs.writeFile(targetIndexPath, `${targetText}${missingEntries.join('\n')}\n`, 'utf8');
}

async function syncBaselineSkillOverrides(targetProject) {
  const sourceDirectory = path.join(referencesDirectory, skillOverridesDirectoryName);
  const targetDirectory = path.join(
    targetProject,
    agentsDirectoryName,
    skillOverridesDirectoryName,
  );
  await fs.mkdir(targetDirectory, { recursive: true });
  const copiedPaths = [];
  const entries = await fs.readdir(sourceDirectory, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isFile() || entry.name === skillOverridesIndexName || !entry.name.endsWith('.md')) {
      continue;
    }
    const targetPath = path.join(targetDirectory, entry.name);
    await fs.copyFile(path.join(sourceDirectory, entry.name), targetPath);
    copiedPaths.push(targetPath);
  }
  const targetIndexPath = path.join(targetDirectory, skillOverridesIndexName);
  const sourceIndexPath = await requiredReference('skill-overrides', skillOverridesIndexName);
  await updateSkillOverrideIndex(targetIndexPath, sourceIndexPath);
  copiedPaths.push(targetIndexPath);
  return copiedPaths;
}

async function discoverBundledSkills() {
  const entries = await fs.readdir(pluginSkillsDirectory, { withFileTypes: true });
  const skillDirectories = [];
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const sourceDirectory = path.join(pluginSkillsDirectory, entry.name);
    if (await pathExists(path.join(sourceDirectory, 'SKILL.md'))) {
      skillDirectories.push(sourceDirectory);
    }
  }
  skillDirectories.sort((left, right) => path.basename(left).localeCompare(path.basename(right)));
  if (skillDirectories.length === 0) {
    throw new Error(`No installable skills found in the plugin bundle: ${pluginSkillsDirectory}`);
  }
  return skillDirectories;
}

async function removeManagedSkill(skillPath) {
  try {
    const details = await fs.lstat(skillPath);
    if (details.isSymbolicLink()) {
      await fs.unlink(skillPath);
    } else if (details.isDirectory()) {
      await fs.rm(skillPath, { recursive: true, force: true });
    } else {
      await fs.unlink(skillPath);
    }
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
}

export async function syncBundledSkills(targetProject) {
  const agentsDirectory = path.join(targetProject, agentsDirectoryName);
  const skillsDirectory = path.join(agentsDirectory, 'skills');
  try {
    if ((await fs.lstat(agentsDirectory)).isSymbolicLink()) {
      throw new Error(`Refusing to write through a symlinked directory: ${agentsDirectory}`);
    }
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
  try {
    if ((await fs.lstat(skillsDirectory)).isSymbolicLink()) {
      throw new Error(`Refusing to write through a symlinked directory: ${skillsDirectory}`);
    }
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
  await fs.mkdir(skillsDirectory, { recursive: true });

  const sourceDirectories = await discoverBundledSkills();
  for (const sourceDirectory of sourceDirectories) {
    const destination = path.join(skillsDirectory, path.basename(sourceDirectory));
    if (path.resolve(sourceDirectory) === path.resolve(destination)) continue;
    await removeManagedSkill(destination);
    await fs.cp(sourceDirectory, destination, {
      recursive: true,
      filter: (sourcePath) => {
        const relativeParts = path.relative(sourceDirectory, sourcePath).split(path.sep);
        return !relativeParts.includes('.git') && !relativeParts.includes('__pycache__');
      },
    });
  }

  const releaseMetadata = await readReleaseMetadata();
  const manifest = {
    source_root: pluginSkillsDirectory,
    version: releaseMetadata.version,
    repository: releaseMetadata.repository,
    managed_skill_dirs: [path.join(agentsDirectoryName, 'skills')],
    skills: sourceDirectories.map((directory) => ({
      source: path.basename(directory),
      installed_as: path.basename(directory),
    })),
  };
  const manifestPath = path.join(targetProject, agentContextDirectoryName, manifestName);
  await fs.writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  return { skillDirectory: skillsDirectory, skillCount: sourceDirectories.length };
}

async function ensureRegularDirectory(directoryPath) {
  try {
    const details = await fs.lstat(directoryPath);
    if (details.isSymbolicLink() || !details.isDirectory()) {
      throw new Error(`Refusing to write through a non-directory path: ${directoryPath}`);
    }
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
    await fs.mkdir(directoryPath);
  }
}

async function ensureCodebaseOnboardingContextFiles(targetProject) {
  let sourceDetails;
  try {
    sourceDetails = await fs.stat(codebaseOnboardingReferencesDirectory);
  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new Error(
        `Bundled codebase-onboarding references are missing: ${codebaseOnboardingReferencesDirectory}`,
      );
    }
    throw error;
  }
  if (!sourceDetails.isDirectory()) {
    throw new Error(
      `Bundled codebase-onboarding references are not a directory: ${codebaseOnboardingReferencesDirectory}`,
    );
  }

  const agentContextDirectory = path.join(targetProject, agentContextDirectoryName);
  await ensureRegularDirectory(agentContextDirectory);

  async function copyMissingFiles(sourceDirectory, destinationDirectory) {
    const createdPaths = [];
    const entries = await fs.readdir(sourceDirectory, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name === '.git' || entry.name === '__pycache__') continue;
      const sourcePath = path.join(sourceDirectory, entry.name);
      const destinationPath = path.join(destinationDirectory, entry.name);
      if (entry.isDirectory()) {
        await ensureRegularDirectory(destinationPath);
        createdPaths.push(...await copyMissingFiles(sourcePath, destinationPath));
      } else if (entry.isFile()) {
        try {
          await fs.copyFile(sourcePath, destinationPath, fsConstants.COPYFILE_EXCL);
          createdPaths.push(destinationPath);
        } catch (error) {
          if (error.code !== 'EEXIST') throw error;
        }
      }
    }
    return createdPaths;
  }

  return copyMissingFiles(codebaseOnboardingReferencesDirectory, agentContextDirectory);
}

function isLegacyProjectUpdateHook(handler) {
  return [handler?.command, handler?.commandWindows].some((command) => {
    if (typeof command !== 'string') return false;
    const normalizedCommand = command.replaceAll('\\', '/');
    return legacyProjectUpdateHookScripts.some((scriptPath) =>
      normalizedCommand.includes(scriptPath.replaceAll('\\', '/')),
    );
  });
}

async function removeLegacyProjectHookFromJson(hooksJsonPath) {
  if (!await pathExists(hooksJsonPath)) return;

  let configuration;
  try {
    configuration = JSON.parse(await fs.readFile(hooksJsonPath, 'utf8'));
  } catch (error) {
    throw new Error(`Project hooks.json is not valid JSON: ${error.message}`);
  }
  if (!configuration || typeof configuration !== 'object' || Array.isArray(configuration)) {
    throw new Error(`Project hooks.json must contain a JSON object: ${hooksJsonPath}`);
  }
  const hooks = configuration.hooks;
  if (hooks === undefined) return;
  if (!hooks || typeof hooks !== 'object' || Array.isArray(hooks)) {
    throw new Error(`Project hooks.json hooks must be an object: ${hooksJsonPath}`);
  }
  const sessionStartGroups = hooks.SessionStart;
  if (sessionStartGroups === undefined) return;
  if (!Array.isArray(sessionStartGroups)) {
    throw new Error(`Project hooks.json SessionStart must be an array: ${hooksJsonPath}`);
  }

  let changed = false;
  const remainingGroups = [];
  for (const group of sessionStartGroups) {
    if (!group || typeof group !== 'object' || !Array.isArray(group.hooks)) {
      remainingGroups.push(group);
      continue;
    }
    const remainingHandlers = group.hooks.filter((handler) => !isLegacyProjectUpdateHook(handler));
    if (remainingHandlers.length !== group.hooks.length) changed = true;
    if (remainingHandlers.length > 0 || group.hooks.length === 0) {
      remainingGroups.push({ ...group, hooks: remainingHandlers });
    }
  }
  if (!changed) return;

  if (remainingGroups.length > 0) hooks.SessionStart = remainingGroups;
  else delete hooks.SessionStart;
  if (Object.keys(hooks).length === 0) delete configuration.hooks;
  if (Object.keys(configuration).length === 0) {
    await fs.rm(hooksJsonPath, { force: true });
    return;
  }
  await fs.writeFile(hooksJsonPath, `${JSON.stringify(configuration, null, 2)}\n`, 'utf8');
}

async function removeLegacyProjectHookFromToml(configPath) {
  if (!await pathExists(configPath)) return;
  const existing = await fs.readFile(configPath, 'utf8');
  const lineEnding = existing.includes('\r\n') ? '\r\n' : '\n';
  const lines = existing.split(/\r?\n/);
  const markerIndex = lines.findIndex((line) => line.trim() === projectUpdateHookMarker);
  if (markerIndex < 0) return;

  const timeoutIndex = lines.findIndex((line, index) => index > markerIndex && line.trim() === 'timeout = 10');
  if (timeoutIndex < 0) return;
  lines.splice(markerIndex, timeoutIndex - markerIndex + 1);
  await fs.writeFile(configPath, lines.join(lineEnding), 'utf8');
}

async function removeEmptyDirectory(directoryPath) {
  let directoryInfo;
  try {
    directoryInfo = await fs.lstat(directoryPath);
  } catch (error) {
    if (error.code === 'ENOENT') return;
    throw error;
  }
  if (!directoryInfo.isDirectory() || (await fs.readdir(directoryPath)).length > 0) return;
  await fs.rmdir(directoryPath);
}

export async function installUpdateChecker(targetProject) {
  const scriptsDirectory = path.join(targetProject, 'scripts');
  await ensureRegularDirectory(scriptsDirectory);
  const checkerPath = path.join(targetProject, projectUpdateCheckerPath);
  await fs.copyFile(updateCheckerSourcePath, checkerPath);

  const codexDirectory = path.join(targetProject, '.codex');
  await removeLegacyProjectHookFromJson(path.join(codexDirectory, 'hooks.json'));
  await removeLegacyProjectHookFromToml(path.join(codexDirectory, 'config.toml'));
  for (const scriptPath of legacyProjectUpdateHookScripts) {
    await fs.rm(path.join(targetProject, scriptPath), { force: true });
  }
  const legacyHookDirectory = path.join(targetProject, '.codex', 'hooks', 'lean-coding-agent');
  await removeEmptyDirectory(legacyHookDirectory);
  await removeEmptyDirectory(path.dirname(legacyHookDirectory));
  return { checkerPath };
}

async function detectPackageManager(targetProject) {
  const packageJsonPath = path.join(targetProject, 'package.json');
  if (await pathExists(packageJsonPath)) {
    let packageJson;
    try {
      packageJson = JSON.parse(await fs.readFile(packageJsonPath, 'utf8'));
    } catch {
      throw new Error(`Target package.json is not valid JSON: ${packageJsonPath}`);
    }
    if (packageJson === null || typeof packageJson !== 'object' || Array.isArray(packageJson)) {
      throw new Error(`Target package.json must contain a JSON object: ${packageJsonPath}`);
    }
    if (typeof packageJson.packageManager === 'string') {
      const managerName = packageJson.packageManager.split('@', 1)[0];
      if (Object.hasOwn(packageManagerCommands, managerName)) return managerName;
    }
  }

  const lockfiles = [
    ['pnpm-lock.yaml', 'pnpm'],
    ['yarn.lock', 'yarn'],
    ['bun.lock', 'bun'],
    ['bun.lockb', 'bun'],
    ['package-lock.json', 'npm'],
    ['npm-shrinkwrap.json', 'npm'],
  ];
  for (const [filename, managerName] of lockfiles) {
    if (await pathExists(path.join(targetProject, filename))) return managerName;
  }
  return 'npm';
}

function executableName(commandName) {
  return process.platform === 'win32' ? `${commandName}.cmd` : commandName;
}

function runCommand(command, args, targetProject, failureMessage) {
  return new Promise((resolve, reject) => {
    const child = spawn(executableName(command), args, {
      cwd: targetProject,
      stdio: 'inherit',
      shell: process.platform === 'win32',
    });
    child.once('error', (error) => {
      reject(new Error(`${failureMessage}: ${error.message}`, { cause: error }));
    });
    child.once('close', (exitCode) => {
      if (exitCode === 0) {
        resolve();
      } else {
        reject(new Error(`${failureMessage} (exit code ${exitCode ?? 'unknown'}).`));
      }
    });
  });
}

async function installAgentBrowser(targetProject) {
  const managerName = await detectPackageManager(targetProject);
  await runCommand(
    packageManagerCommands[managerName][0],
    [...packageManagerCommands[managerName].slice(1), 'agent-browser@latest'],
    targetProject,
    `Could not install agent-browser@latest with ${managerName}`,
  );
  await runCommand(
    agentBrowserInstallCommands[managerName][0],
    agentBrowserInstallCommands[managerName].slice(1),
    targetProject,
    `Could not run agent-browser install with ${managerName}`,
  );
  return `package installed and browser installed with ${managerName}`;
}

async function installUpstreamSkills(targetProject) {
  const installedNames = [];
  for (const { source, skills } of upstreamSkillGroups) {
    await runCommand(
      'npx',
      ['skills', 'add', source, '--skill', ...skills, '--agent', 'codex', '--copy', '-y'],
      targetProject,
      `Could not install upstream skills from ${source} with npx`,
    );
    installedNames.push(...skills);
  }
  return installedNames;
}

async function initializeProject(targetProject, models) {
  const agentContextDirectory = path.join(targetProject, agentContextDirectoryName);
  await fs.mkdir(agentContextDirectory, { recursive: true });
  const onboardingContextPaths = await ensureCodebaseOnboardingContextFiles(targetProject);
  const incidentReadme = await ensureIncidentsReadme(targetProject);
  const lessonsIndex = await ensureLessonsIndex(targetProject);
  const overridePaths = await syncBaselineSkillOverrides(targetProject);
  const agentPaths = await installCodexAgents(targetProject, models);
  const baselinePaths = await copyBaselineFiles(targetProject);
  const localPaths = await ensureLocalFiles(targetProject);
  const gitignorePath = await ensureLocalGitignore(targetProject);
  const skillResult = await syncBundledSkills(targetProject);
  const updateChecker = await installUpdateChecker(targetProject);
  const agentBrowserStatus = await installAgentBrowser(targetProject);
  const upstreamSkillNames = await installUpstreamSkills(targetProject);

  console.log(`Initialized project repo: ${targetProject}`);
  console.log('Copied baseline files:');
  for (const filePath of baselinePaths) console.log(`- ${filePath}`);
  console.log('Ensured private local files:');
  for (const filePath of localPaths) console.log(`- ${filePath}`);
  console.log('Installed Codex agents with selected models:');
  agentNames.forEach((agentName, index) => {
    console.log(`- ${agentPaths[index]}: ${models[agentName]}`);
  });
  console.log(`Agent Browser dependency: ${agentBrowserStatus}`);
  console.log(`Ensured incident reports file: ${incidentReadme}`);
  console.log(`Ensured shared lessons index: ${lessonsIndex}`);
  console.log(`Ensured skill overrides: ${path.join(targetProject, agentsDirectoryName, skillOverridesDirectoryName)}`);
  for (const filePath of overridePaths) console.log(`- ${filePath}`);
  console.log(`Ensured Codex config: ${path.join(targetProject, '.codex', 'config.toml')}`);
  console.log(`Updated ignore rules: ${gitignorePath}`);
  console.log(`Installed ${skillResult.skillCount} bundled skills into: ${skillResult.skillDirectory}`);
  console.log(`Seeded codebase-onboarding context files in: ${path.join(targetProject, agentContextDirectoryName)}`);
  for (const filePath of onboardingContextPaths) console.log(`- ${filePath}`);
  console.log(`Installed version checker: ${updateChecker.checkerPath}`);
  console.log(`Installed upstream skills: ${upstreamSkillNames.join(', ')}`);
}

async function main() {
  const options = readOptions();
  if (options === null) return;
  validateModels(options.models);
  const targetProject = await requireDirectory(options.targetProject, 'Target project');
  await initializeProject(targetProject, options.models);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
