---
name: workflow-feature-specification
description: Orchestration workflow for producing requirements, acceptance criteria, contracts, or a feature specification before implementation. The deliverable is the spec and plan rather than production code, and the workflow spawns the planner subagent.
---

# Feature Requirements And Specification Workflow

Use for drafting requirements and specifications. This is a requirements and contracts workflow, not a deep technical design or OOP class-design workflow.

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, **Workflow Tiering**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. `planner` creates the specification, implementation plan, and any standards-aware notes.

Add deep implementation details, OOP classes, internal interfaces, or module designs only when the user asks for them, an ADR requires them, or the existing architecture makes them necessary.
