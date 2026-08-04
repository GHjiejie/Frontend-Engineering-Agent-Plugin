---
name: frontend-analysis
description: Build a task-scoped frontend engineering context and analyze a feature, bug, or refactor into a Change Contract, requiring a human-provided prototype and complete click-result interaction evidence for every user-facing UI or behavior change. Use when onboarding a frontend task, investigating a UI bug, analyzing a feature or refactor, reconciling manual code changes, or preparing work for the mandatory human approval gate before technical design.
---

# Frontend Analysis

Understand the requested change without modifying product code. Treat repository and human-provided facts as authoritative; treat memory as retrieved evidence with provenance and confidence, not truth. Treat prototypes and interaction effects as required requirements evidence, not optional design inspiration.

## Workflow

1. Read repository instructions and inspect Git status, recent changes, package/configuration files, and the requested sources.
2. Initialize v2 knowledge storage non-destructively when absent:
   `python3 <plugin-root>/scripts/frontend_ai.py init --root <repository-root>`.
3. Move the orchestrator through `MEMORY_SYNC` and `CONTEXT_BUILD` using the runtime CLI. Detect manual code changes, but propose memory changes rather than trusting them automatically.
4. Build `docs/frontend-ai/runtime/task-context.yaml` with the `context` command. Prefer explicit id/path/route/symbol retrieval, then structural relations. Do not claim semantic retrieval in the MVP.
5. Classify the task's design impact as `USER_FACING` when it changes anything a user can see or do, including layout, content, component state, validation, navigation, permissions, or click behavior. Classify it as `NONE` only when UI and interaction behavior are invariants supported by repository evidence.
6. For `USER_FACING`, require the human to provide both:
   - an inspectable prototype for the affected screen or component, such as a specific Figma page/frame/node, annotated image, or wireframe; a bare inaccessible URL is insufficient;
   - the result of every affected click or action, including preconditions, destination or visible result, state changes, side effects, and loading, success, failure, disabled, cancel/back, permission, and validation paths where applicable.
7. Inspect the prototype with an available appropriate tool. Never invent missing UI or interaction intent. A model-generated mockup does not satisfy the gate unless the human supplies it as the approved requirements source.
8. If either input is missing, inaccessible, ambiguous, or incomplete, write the known facts and missing items to a `DRAFT` Change Contract, move to `BLOCKED`, ask for the exact prototype or interaction details, and stop. Do not move to `APPROVAL_REQUIRED`.
9. For `NONE`, record a non-empty `prototypeNotRequiredReason` and concrete `uiInvariantEvidence`. If the evidence does not prove that UI and interaction remain unchanged, reclassify the task as `USER_FACING`.
10. Read the returned entities, project constitution, relevant domain memory, source files, tests, Feature/Bug history, Changes, Decisions, prototype, and interaction evidence. Exclude unrelated memory.
11. Move to `ANALYSIS` and analyze the task as `feature`, `bug`, or `refactor`:
   - Feature: desired behavior, UI, API, interaction, acceptance, compatibility.
   - Bug: observed/expected behavior, reproduction, regression range, hypotheses, evidence, related feature, expected prototype state.
   - Refactor: invariant behavior, motivation, affected dependencies, migration and regression risk; require prototype evidence when any user-facing behavior changes.
12. Write `runtime/change-contract.yaml` according to [references/change-contract.md](references/change-contract.md). Separate facts, inferences, assumptions, and unknowns, and trace UI requirements to prototype and interaction evidence.
13. Set the contract to `READY` only when every requirement has acceptance evidence, the design evidence gate passes, and no unresolved design gap remains.
14. Record a pending analysis approval with the CLI, move to `APPROVAL_REQUIRED`, and validate phase `analysis`.
15. Stop and ask the human to approve or reject the Change Contract. Never record approval without an explicit human decision.

## Gate and safety

- Do not invoke design until `runtime/approvals/analysis.yaml` says `APPROVED`.
- Do not mark a user-facing contract `READY` without a human-provided prototype, complete interaction flows, and UI states.
- Do not accept source code, an AI assumption, or an inaccessible link as a substitute for prototype and interaction evidence.
- Do not create durable Feature, Bug, Change, or Decision knowledge from unapproved analysis.
- Do not implement code, install dependencies, commit, push, or mutate external systems.
- On stale memory or conflicting evidence, enter `CONFLICT`; on a missing prototype, incomplete click effect, or other missing required input, enter `BLOCKED`.

## Handoff

Report the task id, UI-impact classification, prototype references inspected, interaction coverage, retrieved evidence by layer, contract path, risks, unknowns, and the exact input or approval requested from the human.
