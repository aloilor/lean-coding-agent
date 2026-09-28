#!/usr/bin/env node
import fs from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const DEFAULT_RELEASE_METADATA_PATH = path.resolve(path.dirname(SCRIPT_PATH), "../references/release.json");
const DEFAULT_TIMEOUT_MS = 15_000;
const GITHUB_API_VERSION = "2022-11-28";
const SKILLS_LOCK_FILE = "skills-lock.json";

class UpdateCheckError extends Error {}

function parseStableVersion(value, label, allowVPrefix = false) {
  if (typeof value !== "string") {
    throw new UpdateCheckError(`${label} must be a semantic version string.`);
  }

  const version = allowVPrefix && value.startsWith("v") ? value.slice(1) : value;
  const match = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.exec(version);
  if (!match) {
    throw new UpdateCheckError(`${label} must use MAJOR.MINOR.PATCH format (got "${value}").`);
  }

  return {
    text: version,
    parts: match.slice(1).map((part) => BigInt(part)),
  };
}

function compareVersions(left, right) {
  for (let index = 0; index < left.parts.length; index += 1) {
    if (left.parts[index] < right.parts[index]) return -1;
    if (left.parts[index] > right.parts[index]) return 1;
  }
  return 0;
}

function getGitHubRepository(repositoryValue) {
  let repositoryUrl;
  try {
    repositoryUrl = new URL(repositoryValue);
  } catch {
    throw new UpdateCheckError(`Invalid GitHub repository URL: ${repositoryValue}`);
  }

  if (repositoryUrl.protocol !== "https:" || repositoryUrl.hostname !== "github.com") {
    throw new UpdateCheckError("Repository must be an HTTPS GitHub URL.");
  }

  const segments = repositoryUrl.pathname.split("/").filter(Boolean);
  if (segments.length !== 2) {
    throw new UpdateCheckError("Repository URL must have the form https://github.com/owner/repo.");
  }

  const [owner, repository] = segments;
  return {
    owner: decodeURIComponent(owner),
    repository: decodeURIComponent(repository.replace(/\.git$/, "")),
  };
}

async function readVersionManifest(manifestPath) {
  let manifest;
  try {
    manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new UpdateCheckError(`Could not parse ${manifestPath}: ${error.message}`);
    }
    throw new UpdateCheckError(`Could not read ${manifestPath}: ${error.message}`);
  }

  if (!manifest || typeof manifest !== "object" || Array.isArray(manifest)) {
    throw new UpdateCheckError("Skills release metadata must contain a JSON object.");
  }

  return {
    version: parseStableVersion(manifest.version, "installed version"),
    repository: getGitHubRepository(manifest.repository),
  };
}

async function fetchLatestRelease({ owner, repository }, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const apiUrl = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repository)}/releases/latest`;
  let response;
  try {
    response = await fetch(apiUrl, { headers: getGitHubHeaders(), signal: AbortSignal.timeout(timeoutMs) });
  } catch (error) {
    throw new UpdateCheckError(`Could not reach GitHub: ${error.message}`);
  }

  if (response.status === 404) return null;
  if (!response.ok) {
    const reason = response.status === 403 || response.status === 429
      ? "GitHub API rate limit or access restriction. Set GITHUB_TOKEN or GH_TOKEN to authenticate."
      : `GitHub API returned HTTP ${response.status}.`;
    throw new UpdateCheckError(reason);
  }

  let release;
  try {
    release = await response.json();
  } catch {
    throw new UpdateCheckError("GitHub returned an invalid release response.");
  }

  if (!release || typeof release.tag_name !== "string") {
    throw new UpdateCheckError("GitHub's latest release response is missing tag_name.");
  }

  return {
    version: parseStableVersion(release.tag_name, "latest release tag", true),
    url: release.html_url,
  };
}

async function pathExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw error;
  }
}

function getGitHubRepositoryFromSkillLock(source) {
  if (typeof source !== "string") {
    throw new UpdateCheckError("A tracked GitHub skill is missing its source repository.");
  }

  const shorthand = /^([^/]+)\/([^/]+?)(?:\.git)?$/.exec(source);
  if (shorthand) return { owner: shorthand[1], repository: shorthand[2] };
  return getGitHubRepository(source);
}

function getGitHubHeaders() {
  const headers = {
    Accept: "application/vnd.github+json",
    "User-Agent": "lean-coding-agent-update-check",
    "X-GitHub-Api-Version": GITHUB_API_VERSION,
  };
  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

async function fetchGitHubJson(apiUrl, timeoutMs = DEFAULT_TIMEOUT_MS) {
  let response;
  try {
    response = await fetch(apiUrl, {
      headers: getGitHubHeaders(),
      signal: AbortSignal.timeout(timeoutMs),
    });
  } catch (error) {
    throw new UpdateCheckError(`Could not reach GitHub: ${error.message}`);
  }

  if (!response.ok) {
    const reason = response.status === 403 || response.status === 429
      ? "GitHub API rate limit or access restriction. Set GITHUB_TOKEN or GH_TOKEN to authenticate."
      : `GitHub API returned HTTP ${response.status}.`;
    throw new UpdateCheckError(reason);
  }

  try {
    return await response.json();
  } catch {
    throw new UpdateCheckError("GitHub returned an invalid API response.");
  }
}

async function fetchGitHubFile(repository, ref, filePath, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const encodedRef = ref.split("/").map(encodeURIComponent).join("/");
  const encodedPath = filePath.split("/").map(encodeURIComponent).join("/");
  const fileUrl = `https://raw.githubusercontent.com/${encodeURIComponent(repository.owner)}/${encodeURIComponent(repository.repository)}/${encodedRef}/${encodedPath}`;

  let response;
  try {
    response = await fetch(fileUrl, {
      headers: getGitHubHeaders(),
      signal: AbortSignal.timeout(timeoutMs),
    });
  } catch (error) {
    throw new UpdateCheckError(`Could not fetch an upstream skill file from GitHub: ${error.message}`);
  }

  if (!response.ok) {
    throw new UpdateCheckError(`GitHub returned HTTP ${response.status} while fetching ${filePath}.`);
  }
  try {
    return Buffer.from(await response.arrayBuffer());
  } catch (error) {
    throw new UpdateCheckError(`Could not read the upstream skill file ${filePath}: ${error.message}`);
  }
}

async function fetchGitHubSkillTree(repository, ref, timeoutMs = DEFAULT_TIMEOUT_MS) {
  let resolvedRef = ref;
  if (!resolvedRef) {
    const repositoryUrl = `https://api.github.com/repos/${encodeURIComponent(repository.owner)}/${encodeURIComponent(repository.repository)}`;
    const repositoryDetails = await fetchGitHubJson(repositoryUrl, timeoutMs);
    if (!repositoryDetails || typeof repositoryDetails !== "object" || Array.isArray(repositoryDetails)
      || typeof repositoryDetails.default_branch !== "string" || !repositoryDetails.default_branch) {
      throw new UpdateCheckError(`GitHub did not report a default branch for ${repository.owner}/${repository.repository}.`);
    }
    resolvedRef = repositoryDetails.default_branch;
  }

  const encodedRef = encodeURIComponent(resolvedRef);
  const treeUrl = `https://api.github.com/repos/${encodeURIComponent(repository.owner)}/${encodeURIComponent(repository.repository)}/git/trees/${encodedRef}?recursive=1`;
  const tree = await fetchGitHubJson(treeUrl, timeoutMs);
  if (!tree || typeof tree !== "object" || Array.isArray(tree) || !Array.isArray(tree.tree)) {
    throw new UpdateCheckError(`GitHub returned an invalid file tree for ${repository.owner}/${repository.repository}.`);
  }
  if (tree.truncated) {
    throw new UpdateCheckError(`GitHub's file tree is too large to check ${repository.owner}/${repository.repository}.`);
  }
  return { ref: resolvedRef, entries: tree.tree };
}

function getSkillDirectory(skillPath, skillName) {
  if (typeof skillPath !== "string" || skillPath.includes("\\") || skillPath.startsWith("/")) {
    throw new UpdateCheckError(`The GitHub skill lock entry for ${skillName} has an invalid skillPath.`);
  }
  const pathParts = skillPath.split("/");
  if (pathParts.some((part) => !part || part === "." || part === "..") || pathParts.at(-1) !== "SKILL.md") {
    throw new UpdateCheckError(`The GitHub skill lock entry for ${skillName} must point to a SKILL.md file.`);
  }
  return pathParts.slice(0, -1).join("/");
}

async function collectSkillFiles(baseDirectory, currentDirectory, files) {
  const entries = await fs.readdir(currentDirectory, { withFileTypes: true });
  await Promise.all(entries.map(async (entry) => {
    if (entry.name === ".git" || entry.name === "node_modules") return;
    const fullPath = path.join(currentDirectory, entry.name);
    if (entry.isDirectory()) {
      await collectSkillFiles(baseDirectory, fullPath, files);
    } else if (entry.isFile()) {
      const relativePath = path.relative(baseDirectory, fullPath).split(path.sep).join("/");
      files.push({ relativePath, content: await fs.readFile(fullPath) });
    }
  }));
}

async function hashInstalledSkill(skillDirectory, skillName) {
  try {
    await fs.access(skillDirectory);
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw new UpdateCheckError(`Could not access the installed skill ${skillName}: ${error.message}`);
  }

  const files = [];
  try {
    await collectSkillFiles(skillDirectory, skillDirectory, files);
  } catch (error) {
    throw new UpdateCheckError(`Could not read the installed skill ${skillName}: ${error.message}`);
  }
  if (!files.some((file) => file.relativePath === "SKILL.md")) return null;

  files.sort((left, right) => left.relativePath.localeCompare(right.relativePath));
  const hash = createHash("sha256");
  for (const file of files) {
    hash.update(file.relativePath);
    hash.update(file.content);
  }
  return hash.digest("hex");
}

async function fetchLatestSkillHash(repository, skill, treeCache) {
  const skillDirectory = getSkillDirectory(skill.skillPath, skill.name);
  if (skill.ref !== undefined && (typeof skill.ref !== "string" || !skill.ref.trim())) {
    throw new UpdateCheckError(`The GitHub skill lock entry for ${skill.name} has an invalid ref.`);
  }
  const ref = skill.ref?.trim() || null;
  const cacheKey = `${repository.owner}/${repository.repository}@${ref || "<default>"}`;
  if (!treeCache.has(cacheKey)) {
    treeCache.set(cacheKey, fetchGitHubSkillTree(repository, ref));
  }
  const tree = await treeCache.get(cacheKey);
  const directoryPrefix = skillDirectory ? `${skillDirectory}/` : "";
  const files = tree.entries
    .filter((entry) => {
      if (entry.type !== "blob" || entry.mode === "120000" || typeof entry.path !== "string") return false;
      if (directoryPrefix && !entry.path.startsWith(directoryPrefix)) return false;
      const relativePath = directoryPrefix ? entry.path.slice(directoryPrefix.length) : entry.path;
      const excludedDirectory = relativePath.split("/").some((part) => part === ".git" || part === "node_modules");
      return relativePath.length > 0 && !excludedDirectory;
    })
    .map((entry) => ({ path: entry.path, relativePath: directoryPrefix ? entry.path.slice(directoryPrefix.length) : entry.path }));

  if (!files.some((file) => file.path === skill.skillPath)) {
    throw new UpdateCheckError(`GitHub no longer has ${skill.skillPath} for upstream skill ${skill.name}.`);
  }

  files.sort((left, right) => left.relativePath.localeCompare(right.relativePath));
  const contents = await Promise.all(files.map((file) => fetchGitHubFile(repository, tree.ref, file.path)));
  const hash = createHash("sha256");
  for (let index = 0; index < files.length; index += 1) {
    hash.update(files[index].relativePath);
    hash.update(contents[index]);
  }
  return hash.digest("hex");
}

async function checkUpstreamSkillUpdates(lockPath) {
  let lockText;
  try {
    lockText = await fs.readFile(lockPath, "utf8");
  } catch (error) {
    if (error.code === "ENOENT") {
      console.log(`No ${SKILLS_LOCK_FILE} found; upstream skill updates were not checked.`);
      return false;
    }
    throw new UpdateCheckError(`Could not read ${lockPath}: ${error.message}`);
  }

  let lock;
  try {
    lock = JSON.parse(lockText);
  } catch (error) {
    throw new UpdateCheckError(`Could not parse ${lockPath}: ${error.message}`);
  }
  if (!lock || typeof lock !== "object" || Array.isArray(lock) || !lock.skills || typeof lock.skills !== "object" || Array.isArray(lock.skills)) {
    throw new UpdateCheckError(`${SKILLS_LOCK_FILE} must contain an object with a skills map.`);
  }

  const entries = Object.entries(lock.skills)
    .filter(([, skill]) => skill && skill.sourceType === "github")
    .map(([name, skill]) => ({ name, ...skill }));
  const tracked = entries.filter((skill) => typeof skill.skillPath === "string");
  const untrackedCount = entries.length - tracked.length;

  if (tracked.length === 0) {
    console.log(`No GitHub-backed skills with source paths are tracked in ${lockPath}.`);
    if (untrackedCount > 0) console.log(`Skipped ${untrackedCount} GitHub skill(s) without a source path.`);
    return false;
  }

  const treeCache = new Map();
  const outdated = [];
  const missing = [];
  for (const skill of tracked) {
    if (typeof skill.name !== "string" || !skill.name || skill.name === "." || skill.name === ".." || skill.name.includes("/") || skill.name.includes("\\")) {
      throw new UpdateCheckError("A GitHub skill lock entry has an invalid installed skill name.");
    }
    const repository = getGitHubRepositoryFromSkillLock(skill.sourceUrl || skill.source);
    const localDirectory = path.join(path.dirname(lockPath), ".agents", "skills", skill.name);
    const localHash = await hashInstalledSkill(localDirectory, skill.name);
    if (!localHash) {
      missing.push({ name: skill.name, repository });
      continue;
    }
    const latestHash = await fetchLatestSkillHash(repository, skill, treeCache);
    if (latestHash !== localHash) outdated.push({ name: skill.name, repository });
  }

  console.log(`Tracked upstream GitHub skills: ${tracked.length}`);
  if (untrackedCount > 0) console.log(`Skipped ${untrackedCount} GitHub skill(s) without a source path.`);
  if (missing.length > 0) {
    console.log(`Missing installed upstream skill copies: ${missing.map((skill) => skill.name).join(", ")}`);
  }
  if (outdated.length === 0 && missing.length === 0) {
    console.log("Up to date: all tracked upstream skills match their latest source.");
    return false;
  }

  if (outdated.length > 0) {
    console.log(`Updates available for ${outdated.length} upstream skill(s):`);
    for (const skill of outdated) {
      console.log(`  ${skill.name} (${skill.repository.owner}/${skill.repository.repository})`);
    }
    console.log("Run npx skills update -p to refresh project upstream skills.");
  }
  if (missing.length > 0) console.log("Re-run Lean Coding Agent setup to restore missing upstream skill copies.");
  return true;
}

function printUsage() {
  console.log("Usage: node check-skill-updates.mjs [--project] [--manifest <path>] [--lock <path>]");
  console.log("Compare a Lean Coding Agent skill version with GitHub Releases and check upstream GitHub skills.");
  console.log("Use --manifest for an initialized project's installed version and --lock for its upstream skills lock file.");
  console.log("CLI exit codes: 0 = no updates available (or no release yet), 1 = update available, 2 = check failed.");
}

function parseArgs(argv) {
  let projectInstall = false;
  let manifestPath = null;
  let lockPath = path.resolve(SKILLS_LOCK_FILE);
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--project") {
      projectInstall = true;
    } else if (argument === "--manifest") {
      if (!argv[index + 1] || argv[index + 1].startsWith("--")) {
        throw new UpdateCheckError("--manifest requires a file path.");
      }
      manifestPath = path.resolve(argv[++index]);
    } else if (argument === "--lock") {
      if (!argv[index + 1] || argv[index + 1].startsWith("--")) {
        throw new UpdateCheckError("--lock requires a file path.");
      }
      lockPath = path.resolve(argv[++index]);
    } else {
      throw new UpdateCheckError(`Unknown argument: ${argument}`);
    }
  }
  return { lockPath, manifestPath, projectInstall };
}

async function main(argv = process.argv.slice(2)) {
  if (argv.includes("--help") || argv.includes("-h")) {
    printUsage();
    return 0;
  }
  let options;
  try {
    options = parseArgs(argv);
  } catch (error) {
    console.error(error.message);
    printUsage();
    return 2;
  }
  const manifestPath = options.manifestPath ?? DEFAULT_RELEASE_METADATA_PATH;
  let releaseUpdateAvailable = false;
  if (options.manifestPath || await pathExists(manifestPath)) {
    const manifest = await readVersionManifest(manifestPath);
    const release = await fetchLatestRelease(manifest.repository);
    if (!release) {
      console.log("No GitHub Release is published yet; there is nothing to compare.");
    } else {
      const comparison = compareVersions(release.version, manifest.version);
      const versionLabel = options.projectInstall
        ? "Installed Lean Coding Agent skill version"
        : "Local Lean Coding Agent skill version";
      console.log(`${versionLabel}: ${manifest.version.text}`);
      console.log(`Latest stable release:     v${release.version.text}`);
      if (release.url) console.log(`Release page:               ${release.url}`);

      if (comparison > 0) {
        releaseUpdateAvailable = true;
        console.log(options.projectInstall
          ? "Update available: run npx skills update -p, then rerun setup to refresh managed skill copies."
          : "Update available: the latest GitHub Release is newer than this skills checkout.");
      } else if (comparison < 0) {
        console.log(options.projectInstall
          ? "The installed skill copies are ahead of the latest release; their version has not been released yet."
          : "This skills checkout is ahead of the latest release; its version has not been released yet.");
      } else {
        console.log(options.projectInstall
          ? "Up to date: the installed skill copies match the latest stable release."
          : "Up to date: release metadata matches the latest stable release.");
      }
    }
  } else {
    console.log("No Lean Coding Agent release metadata found; skill package updates were not checked.");
  }

  const upstreamUpdateAvailable = await checkUpstreamSkillUpdates(options.lockPath);
  return releaseUpdateAvailable || upstreamUpdateAvailable ? 1 : 0;
}

export function runCli() {
  main().then((exitCode) => {
    process.exitCode = exitCode;
  }).catch((error) => {
    const message = error instanceof UpdateCheckError ? error.message : "Unexpected error.";
    console.error(`Update check failed: ${message}`);
    process.exitCode = 2;
  });
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT_PATH) runCli();
