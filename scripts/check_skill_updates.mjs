#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(SCRIPT_PATH), "..");
const PLUGIN_MANIFEST_PATH = path.join(REPO_ROOT, "plugin.json");
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

async function readPluginManifest() {
  let manifest;
  try {
    manifest = JSON.parse(await fs.readFile(PLUGIN_MANIFEST_PATH, "utf8"));
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new UpdateCheckError(`Could not parse ${PLUGIN_MANIFEST_PATH}: ${error.message}`);
    }
    throw new UpdateCheckError(`Could not read ${PLUGIN_MANIFEST_PATH}: ${error.message}`);
  }

  if (!manifest || typeof manifest !== "object" || Array.isArray(manifest)) {
    throw new UpdateCheckError("plugin.json must contain a JSON object.");
  }

  return {
    version: parseStableVersion(manifest.version, "plugin.json version"),
    repository: getGitHubRepository(manifest.repository),
  };
}

async function fetchLatestRelease({ owner, repository }) {
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
    response = await fetch(apiUrl, { headers, signal: AbortSignal.timeout(15_000) });
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
  console.log("Usage: node scripts/check_skill_updates.mjs");
  console.log("Compare plugin.json with the latest stable GitHub Release.");
  console.log("Exit codes: 0 = no newer release (or no release yet), 1 = update available, 2 = check failed.");
}

async function main(argv = process.argv.slice(2)) {
  if (argv.includes("--help") || argv.includes("-h")) {
    printUsage();
    return 0;
  }
  if (argv.length > 0) {
    console.error(`Unknown argument: ${argv[0]}`);
    printUsage();
    return 2;
  }

  const manifest = await readPluginManifest();
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

main().then((exitCode) => {
  process.exitCode = exitCode;
}).catch((error) => {
  const message = error instanceof UpdateCheckError ? error.message : "Unexpected error.";
  console.error(`Update check failed: ${message}`);
  process.exitCode = 2;
});
