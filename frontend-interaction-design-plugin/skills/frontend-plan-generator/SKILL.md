---
name: frontend-plan-generator
description: Orchestrate frontend project discovery, feature-version confirmation, requirement clarification, and approved interaction artifacts into a reviewable, implementation-ready but code-free frontend development plan. Use for end-to-end frontend design requests, the final delivery plan, task breakdown, page/component design, state strategy, API mapping, exception handling, or frontend-development-plan.md.
---

# Frontend Plan Generator

Create only `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/frontend-development-plan.md`. Never generate or modify application code, create business components, commit changes, or open a pull request.

## Enforce the pipeline

Require the product PRD, prototype, API contract, `clarification.md` with confirmed project/feature/version context and `Gate: PASS`, plus `user-flow.md`, `state-machine.md`, and `sequence-diagram.md` from the exact same directory.

For an end-to-end request where intermediate artifacts do not yet exist, use the other plugin skills in this strict order:

1. Use `requirement-clarification` to run read-only project discovery and wait for Human Gate #1.
2. Resolve the feature and recommended version, then wait for Human Gate #2 before creating files.
3. Run requirement consistency analysis and stop when Human Gate #3 is `Waiting Confirmation`.
4. Run `user-flow-generator`.
5. Run `state-machine-generator`.
6. Run `sequence-diagram-generator`.
7. Return here only after all prerequisite outputs exist in the confirmed version and every gate still passes.

If a source is missing, artifact paths disagree, or a new ambiguity appears, return it to the same version's clarification artifact, block the gate, and pause without creating or updating the plan. Do not collapse the pipeline into an untraceable single-pass summary, rediscover the project, or create a new version during the same iteration.

## Assemble the plan

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Reconcile all inputs and confirmed `CL-xx` decisions. Treat developer-confirmed decisions as highest priority; a new conflict must reopen the clarification gate.
3. Summarize feature scope, actors, business rules, explicit non-goals, and acceptance outcomes.
4. Define a semantic page/component tree based on visible responsibilities, without prescribing framework source files.
5. Define page data, transient UI state, derived state, ownership, reset conditions, and mapped `SM-xx` states.
6. Map lifecycle and user actions to `API-xx` operations and `SQ-xx` sequences, including loading, success, empty, failure, permission, cancellation, and refresh behavior.
7. Describe validation, feedback, recovery, concurrency, and API-contract gaps.
8. Split implementation work into dependency-ordered `FE-xx` tasks with scope, inputs, outputs, dependencies, and acceptance checks.
9. Add confirmed items and unresolved issues sections plus a traceability matrix linking requirements, `CL`, `UF`, `SM`, `SQ`, `API`, and task IDs.

## Keep the plan reviewable

- Include no unapproved assumptions or unresolved business decisions; route them back to the clarification gate.
- Keep tasks framework-neutral unless the user supplied a target stack.
- Do not infer components, APIs, permissions, or error behavior without evidence.
- Do not include source-code snippets or scan unrelated repository code for background.
- Preserve reviewer notes, approved decisions, and manual overrides when updating an existing plan in the same iteration. Never overwrite another independent version.

## Validate

Verify that all artifacts use the confirmed project/feature/version, the clarification gate passes, every confirmed decision is implemented, every in-scope user goal is covered by a flow, every async interaction has modeled states, every API operation appears in a sequence, every declared failure has visible handling, and every task has a testable completion condition. Mark `Ready for Development` only when no blocking unresolved issue remains; otherwise do not finalize the plan.
