#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptPath = fileURLToPath(import.meta.url);
const repositoryRoot = path.resolve(path.dirname(scriptPath), "..");
const sourceDirectory = "skills/skill-overrides";
const mirrorDirectory = "skills/setup-lean-coding-agent/references/skill-overrides";

function git(...args) {
  return execFileSync("git", args, { cwd: repositoryRoot, encoding: "utf8" })
    .split("\n")
    .filter(Boolean);
}

function listFiles(directory) {
  const absolute = path.join(repositoryRoot, directory);
  if (!fs.existsSync(absolute)) return [];
  return fs.readdirSync(absolute, { withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name);
}

// Returns the mirror changes needed to make it a byte-for-byte copy of the source.
function plannedChanges() {
  const sourceFiles = listFiles(sourceDirectory);
  const changes = [];
  for (const name of sourceFiles) {
    const source = fs.readFileSync(path.join(repositoryRoot, sourceDirectory, name));
    const mirrorPath = path.join(repositoryRoot, mirrorDirectory, name);
    if (!fs.existsSync(mirrorPath) || !source.equals(fs.readFileSync(mirrorPath))) {
      changes.push({ name, action: "write" });
    }
  }
  for (const name of listFiles(mirrorDirectory)) {
    if (!sourceFiles.includes(name)) changes.push({ name, action: "delete" });
  }
  return changes;
}

function applyChanges(changes) {
  fs.mkdirSync(path.join(repositoryRoot, mirrorDirectory), { recursive: true });
  for (const { name, action } of changes) {
    const mirrorPath = path.join(repositoryRoot, mirrorDirectory, name);
    if (action === "write") {
      fs.copyFileSync(path.join(repositoryRoot, sourceDirectory, name), mirrorPath);
    } else {
      fs.rmSync(mirrorPath);
    }
    console.log(`${action === "write" ? "Synced" : "Removed"} ${mirrorDirectory}/${name}`);
  }
}

function preCommit() {
  if (git("diff", "--cached", "--name-only", "--", sourceDirectory).length === 0) return 0;

  // The sync copies working-tree files, so unstaged source edits would leak into the commit.
  const unstaged = [
    ...git("diff", "--name-only", "--", sourceDirectory),
    ...git("ls-files", "--others", "--exclude-standard", "--", sourceDirectory),
  ];
  if (unstaged.length > 0) {
    console.error("Skill override sync needs every override change staged. Stage or stash:");
    for (const file of unstaged) console.error(`  ${file}`);
    return 1;
  }

  applyChanges(plannedChanges());
  git("add", "--all", "--", mirrorDirectory);
  return 0;
}

function main(argv = process.argv.slice(2)) {
  const mode = argv[0];
  if (argv.length > 1 || (mode !== undefined && mode !== "--check" && mode !== "--pre-commit")) {
    console.error("Usage: node scripts/sync-skill-overrides.mjs [--check | --pre-commit]");
    return 2;
  }
  if (mode === "--pre-commit") return preCommit();

  const changes = plannedChanges();
  if (changes.length === 0) {
    console.log("Setup skill overrides are in sync.");
    return 0;
  }
  if (mode === "--check") {
    console.error(`Setup skill overrides differ from ${sourceDirectory}:`);
    for (const { name } of changes) console.error(`  ${name}`);
    console.error("Run `npm run sync-skill-overrides`.");
    return 1;
  }
  applyChanges(changes);
  return 0;
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(`Skill override sync failed: ${error.message}`);
  process.exitCode = 2;
}
