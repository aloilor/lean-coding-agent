#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(SCRIPT_PATH), "..");
const PACKAGE_PATH = path.join(REPO_ROOT, "package.json");
const PLUGIN_PATH = path.join(REPO_ROOT, "plugin.json");
const SETUP_VERSION_PATH = path.join(
  REPO_ROOT,
  "skills",
  "setup-lean-coding-agent",
  "references",
  "release.json",
);
const VERSION_PATTERN = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    throw new Error(`Could not read valid JSON from ${filePath}: ${error.message}`);
  }
}

function main(argv = process.argv.slice(2)) {
  const checkOnly = argv.length === 1 && argv[0] === "--check";
  if (argv.length > 0 && !checkOnly) {
    console.error("Usage: node scripts/sync-plugin-version.mjs [--check]");
    return 2;
  }

  const packageManifest = readJson(PACKAGE_PATH);
  if (typeof packageManifest.version !== "string" || !VERSION_PATTERN.test(packageManifest.version)) {
    console.error("package.json version must use MAJOR.MINOR.PATCH format.");
    return 2;
  }
  const repositoryUrl = packageManifest.repository?.url;
  if (typeof repositoryUrl !== "string") {
    console.error("package.json repository.url must contain the GitHub repository URL.");
    return 2;
  }

  const pluginSource = fs.readFileSync(PLUGIN_PATH, "utf8");
  const pluginManifest = readJson(PLUGIN_PATH);
  const setupVersionManifest = readJson(SETUP_VERSION_PATH);
  const setupVersionMatches = setupVersionManifest.version === packageManifest.version
    && setupVersionManifest.repository === repositoryUrl;
  if (pluginManifest.version === packageManifest.version && setupVersionMatches) {
    console.log(`plugin.json version is ${packageManifest.version} (in sync)`);
    return 0;
  }

  if (checkOnly) {
    if (pluginManifest.version !== packageManifest.version) {
      console.error(`plugin.json version is ${pluginManifest.version}, package.json is ${packageManifest.version}.`);
    }
    if (!setupVersionMatches) {
      console.error(`setup skill release metadata does not match package.json version/repository.`);
    }
    console.error("Run `npm run version`.");
    return 1;
  }

  if (pluginManifest.version !== packageManifest.version) {
    const versionField = /("version"\s*:\s*")[^"]*(")/;
    const updatedPlugin = pluginSource.replace(versionField, `$1${packageManifest.version}$2`);
    if (JSON.parse(updatedPlugin).version !== packageManifest.version) {
      console.error(`Could not synchronize the version in ${PLUGIN_PATH}.`);
      return 2;
    }
    fs.writeFileSync(PLUGIN_PATH, updatedPlugin);
    console.log(`plugin.json version ${pluginManifest.version} -> ${packageManifest.version}`);
  }

  if (!setupVersionMatches) {
    fs.writeFileSync(SETUP_VERSION_PATH, `${JSON.stringify({ version: packageManifest.version, repository: repositoryUrl }, null, 2)}\n`);
    console.log(`setup skill release metadata synchronized to v${packageManifest.version}`);
  }
  return 0;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(`Plugin version sync failed: ${error.message}`);
  process.exitCode = 2;
}
