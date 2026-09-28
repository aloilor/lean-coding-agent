#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptPath = fileURLToPath(import.meta.url);
const repositoryRoot = path.resolve(path.dirname(scriptPath), "..");
const packagePath = path.join(repositoryRoot, "package.json");
const releaseMetadataPath = path.join(
  repositoryRoot,
  "skills",
  "setup-lean-coding-agent",
  "references",
  "release.json",
);
const versionPattern = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

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
    console.error("Usage: node scripts/sync-release-version.mjs [--check]");
    return 2;
  }

  const packageManifest = readJson(packagePath);
  if (typeof packageManifest.version !== "string" || !versionPattern.test(packageManifest.version)) {
    console.error("package.json version must use MAJOR.MINOR.PATCH format.");
    return 2;
  }
  const repositoryUrl = packageManifest.repository?.url;
  if (typeof repositoryUrl !== "string") {
    console.error("package.json repository.url must contain the GitHub repository URL.");
    return 2;
  }

  const releaseMetadata = readJson(releaseMetadataPath);
  if (
    !releaseMetadata
    || typeof releaseMetadata.version !== "string"
    || typeof releaseMetadata.repository !== "string"
  ) {
    console.error("Setup release.json must contain a version and repository.");
    return 2;
  }
  const metadataMatches = releaseMetadata.version === packageManifest.version
    && releaseMetadata.repository === repositoryUrl;
  if (metadataMatches) {
    console.log(`Setup skill release metadata is v${packageManifest.version} (in sync).`);
    return 0;
  }

  if (checkOnly) {
    console.error("Setup skill release metadata does not match package.json version/repository.");
    console.error("Run `npm run version`.");
    return 1;
  }

  fs.writeFileSync(
    releaseMetadataPath,
    `${JSON.stringify({ version: packageManifest.version, repository: repositoryUrl }, null, 2)}\n`,
  );
  console.log(`Setup skill release metadata synchronized to v${packageManifest.version}.`);
  return 0;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(`Release metadata sync failed: ${error.message}`);
  process.exitCode = 2;
}
