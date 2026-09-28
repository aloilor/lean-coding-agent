---
name: workflow-feature-specification
description: Orchestration workflow for producing requirements, acceptance criteria, contracts, or a feature specification before implementation.
---

# Feature Specification Workflow

This is a requirements and contracts workflow, not a deep technical design or OOP class-design workflow.

Every run produces the user-approved specification plan at `.agents/plans/plan_YYYYMMDD_<name>.md`; that plan is the durable artifact handed to any later implementation workflow.

The main agent orchestrates this workflow and owns user communication. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions**.

## Steps

1. **Produce and approve the specification plan.** Spawn `planner` with the request and this workflow's planning requirements. The main agent obtains explicit user approval of the completed plan. This workflow ends with that approved plan for a later implementation task; it does not start implementation.

Add deep implementation details, OOP classes, internal interfaces, or module designs only when the user asks for them, an ADR requires them, or the existing architecture makes them necessary.

In the final response, link the plan artifact and summarize the resolved requirements, acceptance criteria, contracts, risks, and verification expectations.
