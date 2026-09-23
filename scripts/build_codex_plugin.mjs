#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(SCRIPT_PATH), "..");
const DEFAULT_PLUGIN_DIR = path.join(REPO_ROOT, "plugins", "lean-coding-agent");
const GENERATED_INDEX = ".generated-files.json";

class BuildError extends Error {}

function isWithin(root, candidate) {
  const relativePath = path.relative(root, candidate);
  return relativePath === "" || (!relativePath.startsWith(`..${path.sep}`) && relativePath !== "..");
}

function compareNames(left, right) {
  return left < right ? -1 : left > right ? 1 : 0;
}

function comparePaths(left, right) {
  const leftParts = left.split(path.sep);
  const rightParts = right.split(path.sep);
  const sharedLength = Math.min(leftParts.length, rightParts.length);
  for (let index = 0; index < sharedLength; index += 1) {
    const comparison = compareNames(leftParts[index], rightParts[index]);
    if (comparison !== 0) return comparison;
  }
  return leftParts.length - rightParts.length;
}

function resolvePath(value) {
  let unresolvedPath = path.resolve(value);
  const remainingParts = [];
  while (!fs.existsSync(unresolvedPath)) {
    const parent = path.dirname(unresolvedPath);
    if (parent === unresolvedPath) return path.resolve(value);
    remainingParts.unshift(path.basename(unresolvedPath));
    unresolvedPath = parent;
  }
  return path.join(fs.realpathSync(unresolvedPath), ...remainingParts);
}

function addFile(files, source, destination) {
  if (!fs.existsSync(source)) throw new BuildError(`Required build source is missing: ${source}`);
  const resolvedSource = fs.realpathSync(source);
  const repositoryRoot = fs.realpathSync(REPO_ROOT);
  if (!isWithin(repositoryRoot, resolvedSource)) {
    throw new BuildError(`Build source escapes the repository: ${source}`);
  }
  if (!fs.statSync(resolvedSource).isFile()) {
    throw new BuildError(`Required build source is missing: ${source}`);
  }
  files.set(destination, fs.readFileSync(resolvedSource));
}

function addTree(files, source, destination) {
  if (!fs.existsSync(source) || !fs.statSync(source).isDirectory()) return;

  const sourceRoot = fs.realpathSync(source);
  function visit(directory, relativeDirectory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => compareNames(a.name, b.name))) {
      if (entry.name === ".git" || entry.name === "__pycache__") continue;
      const sourcePath = path.join(directory, entry.name);
      const relativePath = path.join(relativeDirectory, entry.name);
      if (entry.isDirectory()) {
        visit(sourcePath, relativePath);
      } else if (entry.isFile()) {
        addFile(files, sourcePath, path.join(destination, relativePath));
      }
    }
  }

  visit(sourceRoot, "");
}

function generatedFiles() {
  const files = new Map();
  addFile(files, path.join(REPO_ROOT, "plugin.json"), "plugin.json");

  const sourceSkills = path.join(REPO_ROOT, "skills");
  for (const entry of fs.readdirSync(sourceSkills, { withFileTypes: true }).sort((a, b) => compareNames(a.name, b.name))) {
    if (!entry.isDirectory()) continue;
    const skillDirectory = path.join(sourceSkills, entry.name);
    if (!fs.existsSync(path.join(skillDirectory, "SKILL.md"))) continue;
    addTree(files, skillDirectory, path.join("skills", entry.name));
  }

  const fileNames = [...files.keys()].sort(comparePaths).map((name) => name.split(path.sep).join("/"));
  files.set(GENERATED_INDEX, Buffer.from(`${JSON.stringify(fileNames, null, 2)}\n`, "utf8"));
  return files;
}

function currentFiles(destination) {
  if (!fs.existsSync(destination)) return new Map();
  const destinationInfo = fs.lstatSync(destination);
  if (destinationInfo.isSymbolicLink() || !destinationInfo.isDirectory()) {
    throw new BuildError(`Generated output must be a regular directory: ${destination}`);
  }

  const files = new Map();
  function visit(directory, relativeDirectory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const relativePath = path.join(relativeDirectory, entry.name);
      const fullPath = path.join(directory, entry.name);
      if (entry.isDirectory()) {
        visit(fullPath, relativePath);
      } else if (entry.isFile() && !relativePath.split(path.sep).includes("__pycache__")) {
        files.set(relativePath, fs.readFileSync(fullPath));
      }
    }
  }
  visit(destination, "");
  return files;
}

function checkGeneratedTree(destination, expected) {
  const actual = currentFiles(destination);
  const problems = [];
  const names = new Set([...expected.keys(), ...actual.keys()]);
  for (const relativePath of [...names].sort(comparePaths)) {
    const relativeName = relativePath.split(path.sep).join("/");
    if (!actual.has(relativePath)) {
      problems.push(`missing generated file: ${relativeName}`);
    } else if (!expected.has(relativePath)) {
      problems.push(`unexpected package file: ${relativeName}`);
    } else if (!actual.get(relativePath).equals(expected.get(relativePath))) {
      problems.push(`stale generated file: ${relativeName}`);
    }
  }
  return problems;
}

function buildGeneratedTree(destination, expected, check = false) {
  destination = resolvePath(destination);
  if (check) return checkGeneratedTree(destination, expected);

  currentFiles(destination);
  const previousGenerated = new Set();
  const indexPath = path.join(destination, GENERATED_INDEX);
  if (fs.existsSync(indexPath)) {
    try {
      const previous = JSON.parse(fs.readFileSync(indexPath, "utf8"));
      if (Array.isArray(previous) && previous.every((item) => typeof item === "string")) {
        for (const item of previous) previousGenerated.add(path.normalize(item));
      }
    } catch (error) {
      if (error.code !== "ENOENT" && !(error instanceof SyntaxError)) throw error;
    }
  }

  for (const relativePath of previousGenerated) {
    if (expected.has(relativePath)) continue;
    const stalePath = path.resolve(destination, relativePath);
    const resolvedStalePath = fs.existsSync(stalePath) ? fs.realpathSync(stalePath) : stalePath;
    if (!isWithin(destination, resolvedStalePath)) {
      throw new BuildError(`Generated index contains an unsafe path: ${relativePath}`);
    }
    if (fs.existsSync(resolvedStalePath) && fs.statSync(resolvedStalePath).isFile()) fs.unlinkSync(resolvedStalePath);
  }

  for (const [relativePath, content] of expected) {
    const outputPath = path.join(destination, relativePath);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, content);
  }

  const directories = [];
  function collectDirectories(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const child = path.join(directory, entry.name);
      collectDirectories(child);
      directories.push(child);
    }
  }
  if (fs.existsSync(destination)) collectDirectories(destination);
  for (const directory of directories.reverse()) {
    try {
      fs.rmdirSync(directory);
    } catch (error) {
      if (error.code !== "ENOTEMPTY" && error.code !== "EEXIST") throw error;
    }
  }

  return checkGeneratedTree(destination, expected);
}

export function buildPlugin(destination = DEFAULT_PLUGIN_DIR, check = false) {
  return buildGeneratedTree(destination, generatedFiles(), check);
}

function parseArgs(argv) {
  let check = false;
  let output = DEFAULT_PLUGIN_DIR;
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--help" || argument === "-h") {
      console.log("Usage: node scripts/build_codex_plugin.mjs [--check] [--output <directory>]");
      console.log("Build the plugin bundle, or check that its generated files are current.");
      return null;
    } else if (argument === "--check") {
      check = true;
    } else if (argument === "--output") {
      if (!argv[index + 1] || argv[index + 1].startsWith("--")) {
        throw new BuildError("--output requires a directory path.");
      }
      output = argv[++index];
    } else {
      throw new BuildError(`Unknown argument: ${argument}`);
    }
  }
  return { check, output };
}

function main(argv = process.argv.slice(2)) {
  let options;
  try {
    options = parseArgs(argv);
  } catch (error) {
    console.error(`Plugin build failed: ${error.message}`);
    return 2;
  }
  if (options === null) return 0;

  let problems;
  try {
    problems = buildPlugin(options.output, options.check);
  } catch (error) {
    if (!(error instanceof BuildError)) throw error;
    console.error(`Plugin build failed: ${error.message}`);
    return 2;
  }
  if (problems.length > 0) {
    console.error(problems.join("\n"));
    if (options.check) console.error("Run node scripts/build_codex_plugin.mjs to refresh generated package files.");
    return 1;
  }
  const absoluteOutput = resolvePath(options.output);
  console.log(`Plugin package is ${options.check ? "current" : "built"}: ${absoluteOutput}`);
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT_PATH) {
  process.exitCode = main();
}
