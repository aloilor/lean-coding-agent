#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(SCRIPT_PATH), "..");
const PACKAGE_PATH = path.join(REPO_ROOT, "package.json");
const PLUGIN_PATH = path.join(REPO_ROOT, "plugin.json");
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

  const pluginSource = fs.readFileSync(PLUGIN_PATH, "utf8");
  const pluginManifest = readJson(PLUGIN_PATH);
  if (pluginManifest.version === packageManifest.version) {
    console.log(`plugin.json version is ${packageManifest.version} (in sync)`);
    return 0;
  }

  if (checkOnly) {
    console.error(
      `plugin.json version is ${pluginManifest.version}, package.json is ${packageManifest.version}. Run \`npm run version\`.`,
    );
    return 1;
  }

  const versionField = /("version"\s*:\s*")[^"]*(")/;
  const updatedPlugin = pluginSource.replace(versionField, `$1${packageManifest.version}$2`);
  if (JSON.parse(updatedPlugin).version !== packageManifest.version) {
    console.error(`Could not synchronize the version in ${PLUGIN_PATH}.`);
    return 2;
  }

  fs.writeFileSync(PLUGIN_PATH, updatedPlugin);
  console.log(`plugin.json version ${pluginManifest.version} -> ${packageManifest.version}`);
  return 0;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(`Plugin version sync failed: ${error.message}`);
  process.exitCode = 2;
}
