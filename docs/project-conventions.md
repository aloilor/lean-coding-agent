# Why `docs/conventions/` Is Kept Small

The `project-conventions` skill writes three files, `docs/conventions/CODING-STANDARDS.md`, `TESTING.md`, and `WORKFLOWS.md`, and records only **what an agent would otherwise get wrong**. It does not describe the codebase. This page explains why, with the evidence behind each rule. The skill in [`skills/project-conventions/`](../skills/project-conventions/SKILL.md) is the canonical source for the instructions.

It replaces the earlier `codebase-onboarding` skill, which generated an `agent-context/` folder with a directory map, an architecture overview, a skills index, and per-topic inventories.

## The Rule

Write a fact into `docs/conventions/` only when all of these hold:

1. **An agent cannot recover it cheaply.** If `rg`, a directory listing, a manifest, linter config, existing code, or the README answers it in under a minute, leave it out.
2. **Getting it wrong costs something.** A wrong command, a broken invariant, a forbidden path, an unsafe operation, a rejected review.
3. **It is confirmed** by code, config, CI, docs, git history, or the user.

Everything else is overhead: it costs tokens on every read, widens what the agent explores, and goes stale.

## Evidence

### Context files rarely improve task success and reliably raise cost

Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* (ETH Zurich / LogicStar, ICLR 2026, [arXiv:2602.11988](https://arxiv.org/abs/2602.11988)) tested four coding agents on SWE-bench Lite and on AGENTbench, 138 tasks from repositories whose developers had committed context files.

| Context file | Task success vs. no file | Extra steps per task | Cost |
| --- | --- | --- | --- |
| LLM-generated, following agent-vendor `/init` advice | −0.5% (SWE-bench Lite), −2% (AGENTbench) | +2.45 / +3.92 | +20% / +23% |
| Developer-written | about +4% on average | +3.34 | up to +19% |

Neither success difference was statistically significant; the cost increase was consistent. Agents do follow context-file instructions, which is part of the cost: extra requirements lead to more testing and file traversal than the task needs. The authors recommend that human-written context files "describe only minimal requirements."

**Consequence:** a skill where an LLM generates context files from a repo scan produces the weakest row above. The skill therefore filters hard and interviews the user, so its output is closer to the developer-written row.

### Codebase overviews do not help agents navigate

In the same study, nearly all LLM-generated files contained a codebase overview (100% for Sonnet-4.5, 99% for GPT-5.2), and 8 of 12 developer-written files did too. Context files did not meaningfully reduce the number of steps before the agent first touched a file changed by the reference fix. The authors conclude context files are not effective at providing a repository overview.

**Consequence:** no directory maps, tech-stack tables, architecture overviews, or "where to look" tables. That is why `folder-structure.md`, `architecture.md`, and `README.md` from `agent-context/` have no successor.

### Generated context mostly repeats existing documentation

When the authors removed all documentation from the repositories (`.md` files, examples, `docs/`), LLM-generated context files started to help (+2.7% on average) and outperformed developer-written ones. Generated files were mostly restating documentation the agent could already read.

**Consequence:** do not copy the README, `docs/`, or manifests. Link to them when they are the source of truth. The valuable facts are the ones not written down anywhere, which is why the skill asks the user instead of only scanning.

### When context files do help, it is through operational shortcuts

Lulla et al. ([arXiv:2601.20404](https://arxiv.org/abs/2601.20404)) compared paired agent runs with and without an existing developer-written `AGENTS.md` across 10 repositories and 124 pull requests. They found a 28.64% lower median runtime and 16.58% fewer output tokens, with comparable task completion. The study measured efficiency, not patch correctness, and only covered repositories whose developers had chosen to write such a file.

**Consequence:** the content worth keeping is the kind that saves an agent a wrong turn: exact commands with their required flags, environment setup that is not discoverable, and known traps. That is what `TESTING.md` and `WORKFLOWS.md` hold.

### Missing repository knowledge is rarely why agents fail

*Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories* ([arXiv:2607.27250](https://huggingface.co/papers/2607.27250)) ran Claude Code and Codex for 288 runs on 17 real tasks from 3 repositories. The context-injection strategy did not measurably change correctness; failures came from implementation skill rather than missing repository knowledge.

**Consequence:** convention docs are not a lever for correctness. Keep them cheap.

### Practitioner guidance agrees

- Addy Osmani, [*Stop Using /init for AGENTS.md*](https://addyosmani.com/blog/agents-md/): include only what an agent cannot discover from the code, such as non-obvious tooling, conventions, and landmines; leave out generated overviews, directory structures, and tech-stack summaries.
- Agentic AI Foundation, [*Writing an effective AGENTS.md*](https://aaif.io/blog/writing-an-effective-agents-md): a copied directory listing adds little; the value is the meaning behind the structure. It also warns that the Lulla et al. numbers concern efficiency, not correctness.

## Where Each Kind Of Fact Lives

| Fact | Location | Owner |
| --- | --- | --- |
| Conventions tooling does not enforce, boundaries, invariants, API, data, and security rules | `docs/conventions/CODING-STANDARDS.md` | `project-conventions` |
| Exact verification commands, what to run per change type, test traps | `docs/conventions/TESTING.md` | `project-conventions` |
| Non-default commands, setup and CI traps, generated files, review and release rules | `docs/conventions/WORKFLOWS.md` | `project-conventions` |
| Project terms and preferred names | `docs/GLOSSARY.md` | `grill-with-docs` |
| Decisions and their reasons | `docs/adr/` | `grill-with-docs` |
| Directory maps, stack overviews, skill indexes | Nowhere; agents rebuild them, and harnesses already load skill descriptions | — |

The files live under `docs/` rather than in a hidden folder so humans see and maintain them; stale convention docs are worse than none.

## Limits Of The Evidence

- The benchmarks are mostly Python and SWE-bench-style issue fixing. Large, poorly documented, or polyglot repositories may benefit more, which matches the documentation-removal result.
- Lulla et al. and Gloaguen et al. measure different things (output tokens and runtime vs. total inference cost and success), so their numbers are not directly comparable.
- The baseline `AGENTS.md` loads `docs/conventions/` only for codebase tasks, which is cheaper than the always-loaded files the studies tested. The content findings still apply.

To check the trade-off in a specific project, run a handful of real tasks with and without `docs/conventions/` and compare tokens, steps, and outcomes.
