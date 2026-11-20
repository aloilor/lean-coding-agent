#!/usr/bin/env node
// Claude Code status line, two lines:
//   [Model] effort 📁 project | 🌿 branch
//   ▓▓▓░░░░░ 49.3k/1m | 5h 23% ↻2h13m | 7d 61% ↻3d4h
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';

let j = {};
try { j = JSON.parse(readFileSync(0, 'utf8')); } catch {}

const c = (code, s) => `\x1b[${code}m${s}\x1b[0m`;
const cwd = j.workspace?.current_dir ?? process.cwd();
const project = path.basename(j.workspace?.project_dir ?? cwd);
let branch = '';
try {
  branch = execFileSync('git', ['-C', cwd, 'branch', '--show-current'],
    { stdio: ['ignore', 'pipe', 'ignore'], timeout: 2000 }).toString().trim();
} catch {}

const fmt = (n) => {
  if (n >= 1e6) return `${+(n / 1e6).toFixed(1)}m`;
  if (n >= 1e3) return `${(n / 1e3).toFixed(1)}k`;
  return String(Math.round(n));
};
const bar = (pct, w = 10) => {
  const f = Math.max(0, Math.min(w, Math.round((pct / 100) * w)));
  const col = pct >= 90 ? 31 : pct >= 70 ? 33 : 32;
  return c(col, '█'.repeat(f)) + c(90, '░'.repeat(w - f));
};
// Countdown until a rate-limit window resets (resets_at is Unix epoch seconds).
const until = (epoch) => {
  const m = Math.max(0, Math.round((epoch * 1000 - Date.now()) / 60000));
  const d = Math.floor(m / 1440), h = Math.floor((m % 1440) / 60), min = m % 60;
  return d ? `${d}d${h}h` : h ? `${h}h${min}m` : `${min}m`;
};
const pctColor = (p) => (p >= 90 ? 31 : p >= 70 ? 33 : 37);

// Line 1: model, effort, project, branch
const effort = j.effort?.level ?? j.effort_level ?? j.effort;
const l1 = [];
if (j.model?.display_name) l1.push(c(36, `[${j.model.display_name}]`));
if (typeof effort === 'string' && effort) l1.push(c(35, effort));
l1.push(`📁 ${project}`);
let line1 = l1.join(' ');
if (branch) line1 += ` | 🌿 ${branch}`;

// Line 2: context tokens + rate-limit windows
const cw = j.context_window ?? {};
const fullSize = cw.context_window_size;
// Prefer the configured autoCompactWindow (the real budget) over the model's full window.
const readJson = (p) => { try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return {}; } };
const projDir = j.workspace?.project_dir ?? cwd;
const home = os.homedir();
let compactWin;
for (const p of [path.join(projDir, '.claude/settings.local.json'), path.join(projDir, '.claude/settings.json'), path.join(home, '.claude/settings.json')]) {
  const ms = readJson(p).modelSettings ?? {};
  const id = j.model?.id ?? '';
  const hit = ms[id] ?? Object.entries(ms).find(([k]) => id.startsWith(k))?.[1];
  if (hit?.autoCompactWindow) { compactWin = hit.autoCompactWindow; break; }
}
const size = compactWin && (!fullSize || compactWin < fullSize) ? compactWin : fullSize;
const cu = cw.current_usage ?? {};
let tokens = (cu.input_tokens ?? 0) + (cu.cache_creation_input_tokens ?? 0) + (cu.cache_read_input_tokens ?? 0);
if (!tokens && cw.used_percentage != null && fullSize) tokens = (cw.used_percentage / 100) * fullSize;
let pct = tokens && size ? (tokens / size) * 100 : cw.used_percentage;
const parts = [];
if (pct != null) {
  parts.push(`${bar(pct)} ${size ? `${fmt(tokens)}/${fmt(size)}` : `${Math.round(pct)}%`}`);
}
for (const [key, label] of [['five_hour', '5h'], ['seven_day', '7d']]) {
  const p = j.rate_limits?.[key]?.used_percentage;
  if (p == null) continue;
  const r = j.rate_limits[key].resets_at;
  parts.push(c(pctColor(p), `${label} ${Math.round(p)}%`) + (r ? c(90, ` ↻${until(r)}`) : ""));
}
process.stdout.write(parts.length ? `${line1}\n${parts.join(' | ')}` : line1);
