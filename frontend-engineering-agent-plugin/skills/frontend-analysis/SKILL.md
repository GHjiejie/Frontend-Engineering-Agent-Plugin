---
name: frontend-analysis
description: Build a task-scoped frontend engineering context from governed project memory and repository evidence, then analyze a feature, bug, or refactor into a Change Contract with impact, history, risk, and explicit unknowns. Use when onboarding a task, investigating a bug, analyzing a requested feature or refactor, reconciling manual code changes, detecting relevant historical knowledge, or preparing work for the mandatory human approval gate before technical design.
---

# Frontend Analysis

Understand the requested change without modifying product code. Treat repository and human-provided facts as authoritative; treat memory as retrieved evidence with provenance and confidence, not truth.

## Workflow

1. Read repository instructions and inspect Git status, recent changes, package/configuration files, and the requested sources.
2. Initialize v2 knowledge storage non-destructively when absent:
   `python3 <plugin-root>/scripts/frontend_ai.py init --root <repository-root>`.
3. Move the orchestrator through `MEMORY_SYNC` and `CONTEXT_BUILD` using the runtime CLI. Detect manual code changes, but propose memory changes rather than trusting them automatically.
4. Build `docs/frontend-ai/runtime/task-context.yaml` with the `context` command. Prefer explicit id/path/route/symbol retrieval, then structural relations. Do not claim semantic retrieval in the MVP.
5. Read the returned entities, project constitution, relevant domain memory, source files, tests, Feature/Bug history, Changes, and Decisions. Exclude unrelated memory.
6. Move to `ANALYSIS` and analyze the task as `feature`, `bug`, or `refactor`:
   - Feature: desired behavior, UI, API, interaction, acceptance, compatibility.
   - Bug: observed/expected behavior, reproduction, regression range, hypotheses, evidence, related feature.
   - Refactor: invariant behavior, motivation, affected dependencies, migration and regression risk.
7. Write `runtime/change-contract.yaml` according to [references/change-contract.md](references/change-contract.md). Separate facts, inferences, assumptions, and unknowns.
8. Set the contract to `READY` only when every requirement has acceptance evidence and all blocking ambiguity is explicit.
9. Record a pending analysis approval with the CLI, move to `APPROVAL_REQUIRED`, and validate phase `analysis`.
10. Stop and ask the human to approve or reject the Change Contract. Never record approval without an explicit human decision.

## Gate and safety

- Do not invoke design until `runtime/approvals/analysis.yaml` says `APPROVED`.
- Do not create durable Feature, Bug, Change, or Decision knowledge from unapproved analysis.
- Do not implement code, install dependencies, commit, push, or mutate external systems.
- On stale memory or conflicting evidence, enter `CONFLICT`; on missing required input, enter `BLOCKED`.

## Handoff

Report the task id, retrieved evidence by layer, contract path, risks, unknowns, and the exact decision requested from the human.
