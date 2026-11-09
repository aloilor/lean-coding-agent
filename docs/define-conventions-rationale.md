# `define-conventions` Rationale: Why Conventions Are Grilled, Not Scanned

The [`define-conventions`](../skills/define-conventions/SKILL.md) skill writes `docs/conventions/` by scanning the repository for evidence and then grilling the user on what the repository cannot show. This page explains why. The skill is the canonical source for the instructions.

## History

- `codebase-onboarding` generated directory maps and architecture overviews. The research below shows that content does not help agents.
- `project-conventions` added a strict inclusion test over bare templates. With only a heading to fill, agents wrote what is usually true for the stack.
- `init-conventions` gathered evidence section by section, ran commands, and asked about gaps. It still treated the repository as the source of truth, so it recorded existing practice whether or not that practice was any good.
- `define-conventions` treats the repository as evidence and the user as the authority.

## Design Choices

### The repository is evidence, not authority

Many people write the code in a repository, and frequency says nothing about quality. A scan can show what is common. Only a person can say what is intended, which of two patterns is current, and what should not spread. Rules the code does not follow yet are written with their scope, so agents neither distrust them nor migrate code unprompted.

### Evidence must not anchor the answer

A grill that recommends the most common pattern gets "yes" for it and turns bad code into policy. On questions about what should be true, the skill shows the split and recommends on quality.

### One test for every line

A line stays only if a competent agent, reading the repository for its task, would otherwise guess wrong, spend real effort finding it, or copy the wrong pattern. There is no length limit, because the test is what controls size.

### No links to repository documents

Each rule stands alone: links rot and agents do not reliably follow them. Code paths remain, because a rule about specific code has to name it. External URLs remain when they are the fact being recorded.

### Files split by task

`AGENTS.md` loads only the convention files relevant to the task. Coding standards, testing, deployment, and change process are separate so a commit does not load deployment rules. Files exist only when they have content.

### The agenda is open

A guide can prompt only for what it names, so a fixed list would miss whatever is specific to a project. The agenda step lets the user add areas and asks what agents or new contributors keep getting wrong.

### Exemplars are confirmed by a person

An agent can find common code, not excellent code. The skill asks the user first, then adds candidates and shows each for confirmation. When nothing qualifies, it writes nothing.

### The skill does not execute the project

Commands are recorded only when the user states or confirms them. The skill never runs anything that changes state, and runs a test or build only with a yes for that command.

## Evidence

- Gloaguen et al., [*Evaluating AGENTS.md*](https://arxiv.org/abs/2602.11988), found that LLM-generated context files slightly reduced task success (−0.5% and −2%, not statistically significant) and raised cost by 20% to 23%. Developer-written files did 2.4% better on average than no file, also not significantly, and cost up to 19% more, but they did significantly better than generated files. Generated files mostly restated existing documentation. **Consequence:** output should be closer to developer-written files, which is why the skill asks rather than only scans.
- The same study found codebase overviews did not help agents reach the right files sooner. **Consequence:** no directory maps or stack summaries.
- Lulla et al. ([arXiv:2601.20404](https://arxiv.org/abs/2601.20404)) found 28.64% lower median runtime and 16.58% fewer output tokens with developer-written `AGENTS.md` files, with comparable completion. The study measured efficiency, not correctness. **Consequence:** keep what saves a wrong turn.
- [*Do Context Files Help Coding Agents?*](https://huggingface.co/papers/2607.27250) found no measurable change in correctness from context injection across 288 evaluated runs on 17 tasks, which bounds any effect to about 10 to 15 percentage points. **Consequence:** convention docs cannot be assumed to improve correctness, so every line has to earn its cost.
- Addy Osmani, [*Stop Using /init for AGENTS.md*](https://addyosmani.com/blog/agents-md/), recommends including only what an agent cannot discover from the code.

## Limits Of The Evidence

- The studies measure context files in general, mostly on Python issue fixing. None tests grilled conventions.
- The studies do not show that normative rules improve code quality. That benefit is this skill's premise, not a finding.
- The skill's evaluation so far uses three scripted-answer cases: a repository whose common pattern is the bad one, an update of the older layout, and a missing grill dependency. Scripted answers cannot show how real users respond to a long interview.

To check the trade-off in a specific project, run a handful of real tasks with and without `docs/conventions/` and compare tokens, steps, and outcomes.
