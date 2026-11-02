#!/usr/bin/env node
// List every commit reachable from HEAD that is a changelog candidate.
//
// Usage:
//   node list-candidates.mjs --since YYYY-MM-DD [--offset +HH:MM]
//   node list-candidates.mjs --after <commit>
//
// --since keeps commits whose committer date is at or after midnight of that
// day, in the given UTC offset or the local timezone. History is enumerated in
// full and filtered afterwards, so out-of-order timestamps cannot hide commits.
// --after keeps commits reachable from HEAD but not from <commit> (excluded).

import { execFileSync } from "node:child_process";

const git = (...args) =>
  execFileSync("git", args, { encoding: "utf8", maxBuffer: 1 << 30 }).trim();

function parseArgs(argv) {
  const options = {};
  for (let i = 0; i < argv.length; i += 2) {
    const [key, value] = [argv[i], argv[i + 1]];
    if (!["--since", "--offset", "--after"].includes(key) || value === undefined) {
      throw new Error(`Unexpected argument: ${key}`);
    }
    options[key.slice(2)] = value;
  }
  if (!options.since === !options.after) {
    throw new Error("Pass exactly one of --since or --after.");
  }
  return options;
}

function cutoffFor(date, offset) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error(`Invalid date: ${date}`);
  if (offset && !/^[+-]\d{2}:\d{2}$/.test(offset)) throw new Error(`Invalid offset: ${offset}`);
  const [year, month, day] = date.split("-").map(Number);
  return offset
    ? new Date(`${date}T00:00:00${offset}`)
    : new Date(year, month - 1, day);
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const range = options.after ? [`${options.after}..HEAD`] : ["HEAD"];
  const cutoff = options.since && cutoffFor(options.since, options.offset);

  const separator = "\x1f";
  const log = git("log", "--reverse", `--format=%H${separator}%cI${separator}%P${separator}%s`, ...range);
  const commits = (log ? log.split("\n") : [])
    .map((line) => {
      const [hash, committed, parents, subject] = line.split(separator);
      return { hash, committed, parents: parents.split(" ").filter(Boolean), subject };
    })
    .filter((commit) => !cutoff || new Date(commit.committed) >= cutoff);

  const branch = git("rev-parse", "--abbrev-ref", "HEAD");
  const head = git("rev-parse", "--short", "HEAD");
  const boundary = options.after
    ? `after ${options.after} (excluded)`
    : `committer date >= ${cutoff.toISOString()} (${options.since}, ${options.offset ?? "local time"})`;

  console.log(`# branch ${branch}, HEAD ${head}`);
  console.log(`# boundary: ${boundary}`);
  if (git("rev-parse", "--is-shallow-repository") === "true") {
    console.log("# WARNING: shallow repository; history before the graft point is missing.");
  }
  console.log(`# ${commits.length} candidate commit(s), oldest first`);
  console.log("hash\tcommitted\tkind\tsubject");
  for (const { hash, committed, parents, subject } of commits) {
    const kind = parents.length > 1 ? `merge(${parents.length})` : parents.length ? "commit" : "root";
    console.log(`${hash.slice(0, 12)}\t${committed}\t${kind}\t${subject}`);
  }
}

try {
  main();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
