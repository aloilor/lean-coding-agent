# `init-conventions` Rationale: Why `docs/conventions/` Holds Only Repo-Specific, Verified Facts

The `init-conventions` skill writes three files, `docs/conventions/CODING-STANDARDS.md`, `TESTING.md`, and `WORKFLOWS.md`, containing only facts specific to the repository: verified commands, example files to follow, boundaries, forbidden operations, generated files, and traps. It does not describe the codebase. This page explains why, with the evidence behind each rule. The skill in [`skills/init-conventions/`](../skills/init-conventions/SKILL.md) is the canonical source for the instructions.

## History

- `codebase-onboarding` generated an `agent-context/` folder with a directory map, an architecture overview, a skills index, and per-topic inventories. The research below shows that kind of content does not help agents.
- `project-conventions` replaced it with a strict inclusion test and bare section templates. In practice its output was **too generic**: with only a heading to fill and no evidence for it, the agent wrote what is usually true for the stack ("write unit tests", "follow existing patterns"). A filter cannot remove lines that are plausible.
- `init-conventions` keeps the evidence-based scope but changes how facts are gathered: each section has its own evidence sources, commands are run before they are recorded, and a swap test removes stack-generic lines.

## The Rule

Write a fact into `docs/conventions/` only when all of these hold:

1. **Specific.** It passes the swap test: pasted into another repository with the same stack, it would no longer be true. A surviving line names something only this repo has: a path, a command with its flags, a symbol, a config key, a decision.
2. **Actionable.** An agent would run it, imitate it, or avoid something because of it.
3. **Confirmed.** Code, config, CI, docs, git history, a command run, or the user backs it. Otherwise it is written with `(inferred: <evidence>)` so the reader knows how much to trust it.

Directory maps, tech-stack tables, architecture overviews, endpoint or schema inventories, and rules a linter or formatter already enforces stay out. They cost tokens on every read, widen what the agent explores, and go stale.

## Design Choices

### Every section starts from evidence

Each section of each template lists where its facts come from: CI files and hooks for the Definition Of Done, recently added files for Follow These Examples, `DO NOT` comments and reverted commits for Never, and so on. A section with no evidence and no user answer is written as `None.`; it is never padded with general advice. This is the main fix for generic output: the agent starts from something it found, not from a blank heading.

### Commands are run before they are recorded

The most useful content of a context file is operational: exact commands and their prerequisites (see Lulla et al. below). A command that looks right but fails sends the agent on exactly the wrong turn the file should prevent. The skill runs every Definition Of Done command and at least one fast single-test command, and turns failures into Prerequisites or Traps. Commands that deploy, publish, push, or need unavailable credentials are recorded as inferred instead.

### Facts are copied, not linked

When the README, `CONTRIBUTING.md`, or `docs/` already state a fact, such as the test command, the skill copies it, condensed, into the right section. These three files are the one place an agent reads to work correctly; a link costs another read and is easy to skip.

This deliberately trades some redundancy for reliability. Gloaguen et al. (below) found generated context files mostly restate existing documentation; the skill limits that cost by copying only facts that pass the rule, never prose, overviews, or whole guides.

### Fixed headings, explicit absence

Every template heading is always present. `None.` tells the agent the topic was checked, so it does not search for rules that do not exist; a missing heading is ambiguous. Fixed headings also make the files predictable to read and easy to refresh.

### The repo first, then as many questions as needed

The most valuable facts are often not written anywhere: which of two coexisting patterns is current, what reviewers reject, which operations are forbidden, which tests are flaky. The skill looks for each fact in the repo first and asks the user only about real gaps, as many questions as needed, each with a candidate answer drawn from the evidence so the user can confirm instead of compose.

## Evidence

### Context files rarely improve task success and reliably raise cost

Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* (ETH Zurich / LogicStar, ICLR 2026, [arXiv:2602.11988](https://arxiv.org/abs/2602.11988)) tested four coding agents on SWE-bench Lite and on AGENTbench, 138 tasks from repositories whose developers had committed context files.

| Context file | Task success vs. no file | Extra steps per task | Cost |
| --- | --- | --- | --- |
| LLM-generated, following agent-vendor `/init` advice | −0.5% (SWE-bench Lite), −2% (AGENTbench) | +2.45 / +3.92 | +20% / +23% |
| Developer-written | about +4% on average | +3.34 | up to +19% |

Neither success difference was statistically significant; the cost increase was consistent. Agents do follow context-file instructions, which is part of the cost: extra requirements lead to more testing and file traversal than the task needs. The authors recommend that human-written context files "describe only minimal requirements."

**Consequence:** a skill that generates context files from a repo scan alone produces the weakest row above. The skill therefore keeps only specific, confirmed facts and interviews the user, so its output is closer to the developer-written row.

### Codebase overviews do not help agents navigate

In the same study, nearly all LLM-generated files contained a codebase overview (100% for Sonnet-4.5, 99% for GPT-5.2), and 8 of 12 developer-written files did too. Context files did not meaningfully reduce the number of steps before the agent first touched a file changed by the reference fix. The authors conclude context files are not effective at providing a repository overview.

**Consequence:** no directory maps, tech-stack tables, architecture overviews, or "where to look" tables. Follow These Examples is the exception that fits: it does not map the repository, it names the one file to imitate for a recurring kind of change.

### Generated context mostly repeats existing documentation

When the authors removed all documentation from the repositories (`.md` files, examples, `docs/`), LLM-generated context files started to help (+2.7% on average) and outperformed developer-written ones. Generated files were mostly restating documentation the agent could already read.

**Consequence:** copy only facts that pass the rule, never documentation wholesale. The valuable facts are the ones not written down anywhere, which is why the skill asks the user instead of only scanning.

### When context files do help, it is through operational shortcuts

Lulla et al. ([arXiv:2601.20404](https://arxiv.org/abs/2601.20404)) compared paired agent runs with and without an existing developer-written `AGENTS.md` across 10 repositories and 124 pull requests. They found a 28.64% lower median runtime and 16.58% fewer output tokens, with comparable task completion. The study measured efficiency, not patch correctness, and only covered repositories whose developers had chosen to write such a file.

**Consequence:** the content worth keeping is the kind that saves an agent a wrong turn: exact commands with their required flags, environment setup that is not discoverable, and known traps. That is why commands are verified by running them.

### Missing repository knowledge is rarely why agents fail

*Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories* ([arXiv:2607.27250](https://huggingface.co/papers/2607.27250)) ran Claude Code and Codex for 288 runs on 17 real tasks from 3 repositories. The context-injection strategy did not measurably change correctness; failures came from implementation skill rather than missing repository knowledge.

**Consequence:** convention docs are not a lever for correctness. Keep them cheap: about one screen per file.

### Practitioner guidance agrees

- Addy Osmani, [*Stop Using /init for AGENTS.md*](https://addyosmani.com/blog/agents-md/): include only what an agent cannot discover from the code, such as non-obvious tooling, conventions, and landmines; leave out generated overviews, directory structures, and tech-stack summaries.
- Agentic AI Foundation, [*Writing an effective AGENTS.md*](https://aaif.io/blog/writing-an-effective-agents-md): a copied directory listing adds little; the value is the meaning behind the structure. It also warns that the Lulla et al. numbers concern efficiency, not correctness.

## Where Each Kind Of Fact Lives

| Fact | Location | Owner |
| --- | --- | --- |
| Definition Of Done, fast test commands, test prerequisites, how tests are written, test traps | `docs/conventions/TESTING.md` | `init-conventions` |
| Tooling in force, example files to follow, boundaries, data and security rules, forbidden operations | `docs/conventions/CODING-STANDARDS.md` | `init-conventions` |
| Setup, non-default commands, generated files, change process (including docs that must change with code), CI and release, workflow traps | `docs/conventions/WORKFLOWS.md` | `init-conventions` |
| Project terms and preferred names | `docs/conventions/GLOSSARY.md` | `lean-grill-with-docs` |
| Decisions and their reasons | `docs/conventions/adr/` | `lean-grill-with-docs` |
| Directory maps, stack overviews, skill indexes | Nowhere; agents rebuild them, and harnesses already load skill descriptions | — |

The files live under `docs/` rather than in a hidden folder so humans see and maintain them; stale convention docs are worse than none. The skill's refresh mode reruns recorded commands and checks that referenced paths still exist.

## Limits Of The Evidence

- The benchmarks are mostly Python and SWE-bench-style issue fixing. Large, poorly documented, or polyglot repositories may benefit more, which matches the documentation-removal result.
- Lulla et al. and Gloaguen et al. measure different things (output tokens and runtime vs. total inference cost and success), so their numbers are not directly comparable.
- The baseline `AGENTS.md` loads `docs/conventions/` only for codebase tasks, which is cheaper than the always-loaded files the studies tested. The content findings still apply.
- Copying documented facts and running commands are design choices made for this skill, not findings of the studies above.
- The skill's own evaluation so far covers two runs on this repository (a fresh setup and a refresh), which is well documented. With the skill, output had the fixed structure and verified commands every time; without it, output was also specific but unstructured. Whether the skill prevents generic output on a poorly documented repository is not yet tested.

To check the trade-off in a specific project, run a handful of real tasks with and without `docs/conventions/` and compare tokens, steps, and outcomes.
