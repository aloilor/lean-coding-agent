---
name: workflow-feature-specification
description: Orchestration workflow for producing requirements, acceptance criteria, contracts, or a feature specification before implementation.
---

# Feature Requirements And Specification Workflow

This is a requirements and contracts workflow, not a deep technical design or OOP class-design workflow.

Every run produces the approved specification plan at `.agents/plans/plan_YYYYMMDD_<name>.md`; that plan is the durable artifact handed to any later implementation workflow.

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. **Mandatory grill gate.** The main agent enters Plan mode and **MUST run `$grill-with-docs` first**. It must not consolidate requirements, write the plan, request approval, or proceed until the grill has run. It then consolidates the resolved requirements, contracts, acceptance criteria, non-goals, decisions, risks, verification, and necessary standards-aware implementation notes into `.agents/plans/plan_YYYYMMDD_<name>.md`, then obtains explicit user approval.

Add deep implementation details, OOP classes, internal interfaces, or module designs only when the user asks for them, an ADR requires them, or the existing architecture makes them necessary.

In the final response, link the plan artifact and summarize the resolved requirements, acceptance criteria, contracts, risks, and verification expectations.
