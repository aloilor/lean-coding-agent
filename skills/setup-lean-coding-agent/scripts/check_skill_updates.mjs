#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const DEFAULT_PLUGIN_ROOT = path.resolve(path.dirname(SCRIPT_PATH), "..", "..", "..");
const DEFAULT_TIMEOUT_MS = 15_000;
const HOOK_TIMEOUT_MS = 5_000;
const GITHUB_API_VERSION = "2022-11-28";

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
    throw new UpdateCheckError(`plugin.json has an invalid repository URL: ${repositoryValue}`);
  }

  if (repositoryUrl.protocol !== "https:" || repositoryUrl.hostname !== "github.com") {
    throw new UpdateCheckError("plugin.json repository must be an HTTPS GitHub URL.");
  }

  const segments = repositoryUrl.pathname.split("/").filter(Boolean);
  if (segments.length !== 2) {
    throw new UpdateCheckError("plugin.json repository URL must have the form https://github.com/owner/repo.");
  }

  const [owner, repository] = segments;
  return {
    owner: decodeURIComponent(owner),
    repository: decodeURIComponent(repository.replace(/\.git$/, "")),
  };
}

async function readPluginManifest(manifestPath = path.join(process.env.PLUGIN_ROOT || DEFAULT_PLUGIN_ROOT, "plugin.json")) {
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
    throw new UpdateCheckError("plugin.json must contain a JSON object.");
  }

  return {
    version: parseStableVersion(manifest.version, "plugin.json version"),
    repository: getGitHubRepository(manifest.repository),
  };
}

async function fetchLatestRelease({ owner, repository }, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const apiUrl = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repository)}/releases/latest`;
  const headers = {
    Accept: "application/vnd.github+json",
    "User-Agent": "lean-coding-agent-release-check",
    "X-GitHub-Api-Version": GITHUB_API_VERSION,
  };
  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
  if (token) headers.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(apiUrl, { headers, signal: AbortSignal.timeout(timeoutMs) });
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

function createSessionStartHookOutput(installedVersionText, latestVersionText, projectInstall = false) {
  if (latestVersionText === null) return null;

  const installedVersion = parseStableVersion(installedVersionText, "installed plugin version");
  const latestVersion = parseStableVersion(latestVersionText, "latest release version", true);
  if (compareVersions(latestVersion, installedVersion) <= 0) return null;

  const updateContext = projectInstall
    ? `The project's Lean Coding Agent skill copies are outdated (installed from v${installedVersion.text}; v${latestVersion.text} is the latest stable release). In your first reply, briefly tell the user to update Lean Coding Agent and rerun \`$setup-lean-coding-agent\` to refresh this project's skill copies, then continue with their request.`
    : `Lean Coding Agent update available: v${installedVersion.text} is installed and v${latestVersion.text} is the latest stable release. In your first reply, briefly tell the user and recommend updating with \`codex plugin marketplace upgrade lean-coding-agent\`, then continue with their request.`;

  return {
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: updateContext,
    },
  };
}

function printUsage() {
  console.log("Usage: node check_skill_updates.mjs [--hook] [--project] [--manifest <path>]");
  console.log("Compare the installed version with the latest stable GitHub Release.");
  console.log("Use --hook for quiet Codex SessionStart output, --manifest to select the installed version, and --project for project skill copies.");
  console.log("Exit codes: 0 = no newer release (or no release yet), 1 = update available, 2 = check failed.");
}

async function runSessionStartCheck(manifestPath, projectInstall) {
  try {
    const manifest = await readPluginManifest(manifestPath);
    const release = await fetchLatestRelease(manifest.repository, HOOK_TIMEOUT_MS);
    const output = createSessionStartHookOutput(
      manifest.version.text,
      release?.version.text ?? null,
      projectInstall,
    );
    if (output) console.log(JSON.stringify(output));
  } catch {
    // Keep startup quiet when the release check cannot determine the latest version.
  }
  return 0;
}

function parseArgs(argv) {
  let hook = false;
  let projectInstall = false;
  let manifestPath = path.join(process.env.PLUGIN_ROOT || DEFAULT_PLUGIN_ROOT, "plugin.json");
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--hook") {
      hook = true;
    } else if (argument === "--project") {
      projectInstall = true;
    } else if (argument === "--manifest") {
      if (!argv[index + 1] || argv[index + 1].startsWith("--")) {
        throw new UpdateCheckError("--manifest requires a file path.");
      }
      manifestPath = path.resolve(argv[++index]);
    } else {
      throw new UpdateCheckError(`Unknown argument: ${argument}`);
    }
  }
  return { hook, manifestPath, projectInstall };
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
  if (options.hook) return runSessionStartCheck(options.manifestPath, options.projectInstall);

  const manifest = await readPluginManifest(options.manifestPath);
  const release = await fetchLatestRelease(manifest.repository);
  if (!release) {
    console.log("No GitHub Release is published yet; there is nothing to compare.");
    return 0;
  }

  const comparison = compareVersions(release.version, manifest.version);
  console.log(`Local plugin.json version: ${manifest.version.text}`);
  console.log(`Latest stable release:     v${release.version.text}`);
  if (release.url) console.log(`Release page:               ${release.url}`);

  if (comparison > 0) {
    console.log("Update available: the latest release is newer than this checkout.");
    return 1;
  }
  if (comparison < 0) {
    console.log("This checkout is ahead of the latest release; its version has not been released yet.");
    return 0;
  }

  console.log("Up to date: plugin.json matches the latest stable release.");
  return 0;
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
