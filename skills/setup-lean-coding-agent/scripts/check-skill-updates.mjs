#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const DEFAULT_PLUGIN_ROOT = path.resolve(path.dirname(SCRIPT_PATH), "..", "..", "..");
const DEFAULT_TIMEOUT_MS = 15_000;
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
    throw new UpdateCheckError(`Version manifest has an invalid repository URL: ${repositoryValue}`);
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

async function readVersionManifest(manifestPath = path.join(process.env.PLUGIN_ROOT || DEFAULT_PLUGIN_ROOT, "plugin.json")) {
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
    throw new UpdateCheckError("Version manifest must contain a JSON object.");
  }

  return {
    version: parseStableVersion(manifest.version, "installed version"),
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

function printUsage() {
  console.log("Usage: node check-skill-updates.mjs [--project] [--manifest <path>]");
  console.log("Compare the installed plugin or project skill version with the latest stable GitHub Release.");
  console.log("Use --manifest to select the installed version and --project to describe project skill copies.");
  console.log("CLI exit codes: 0 = no newer release (or no release yet), 1 = update available, 2 = check failed.");
}

function parseArgs(argv) {
  let projectInstall = false;
  let manifestPath = path.join(process.env.PLUGIN_ROOT || DEFAULT_PLUGIN_ROOT, "plugin.json");
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--project") {
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
  return { manifestPath, projectInstall };
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
  const manifest = await readVersionManifest(options.manifestPath);
  const release = await fetchLatestRelease(manifest.repository);
  if (!release) {
    console.log("No GitHub Release is published yet; there is nothing to compare.");
    return 0;
  }

  const comparison = compareVersions(release.version, manifest.version);
  const versionLabel = options.projectInstall ? "Project skill version" : "Local plugin.json version";
  console.log(`${versionLabel}: ${manifest.version.text}`);
  console.log(`Latest stable release:     v${release.version.text}`);
  if (release.url) console.log(`Release page:               ${release.url}`);

  if (comparison > 0) {
    console.log(options.projectInstall
      ? "Update available: the project skill copies are older; update Lean Coding Agent and rerun its setup skill."
      : "Update available: the latest release is newer than this checkout.");
    return 1;
  }
  if (comparison < 0) {
    console.log(options.projectInstall
      ? "The project skill copies are ahead of the latest release; their version has not been released yet."
      : "This checkout is ahead of the latest release; its version has not been released yet.");
    return 0;
  }

  console.log(options.projectInstall
    ? "Up to date: the project skill copies match the latest stable release."
    : "Up to date: plugin.json matches the latest stable release.");
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
