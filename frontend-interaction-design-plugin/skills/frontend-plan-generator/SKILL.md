---
name: frontend-plan-generator
description: Assemble a product PRD, frontend prototype, confirmed API contract, passed clarification gate, approved user flow, state machine, and sequence diagrams into an implementation-ready but code-free frontend development plan. Use for the final frontend delivery plan, task breakdown, page/component design, state strategy, API plan, exception handling, or an end-to-end package written to frontend-design/{feature-name}/frontend-development-plan.md.
---

# Frontend Plan Generator

Create only `frontend-design/<feature-name>/frontend-development-plan.md`. Never generate or modify application code, create business components, commit changes, or open a pull request.

## Enforce the pipeline

Require the product PRD, prototype, API contract, `clarification.md` with `Gate: PASS`, `user-flow.md`, `state-machine.md`, and `sequence-diagram.md`.

For an end-to-end request where intermediate artifacts do not yet exist, use the other plugin skills in this strict order:

1. `requirement-clarification-generator`
2. Stop and wait when its status is `Waiting Confirmation`.
3. `user-flow-generator`
4. `state-machine-generator`
5. `sequence-diagram-generator`
6. Return here only after all four prerequisite outputs are available and the gate still passes.

If a source is missing or a new ambiguity appears, return it to the clarification artifact, block the gate, and pause without creating or updating the plan. Do not collapse the pipeline into an untraceable single-pass summary.

## Assemble the plan

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Reconcile all seven inputs and confirmed `CL-xx` decisions. A conflict must reopen the clarification gate.
3. Summarize feature scope, actors, business rules, explicit non-goals, and acceptance outcomes.
4. Define a semantic page/component tree based on visible responsibilities, without prescribing framework source files.
5. Define page data, transient UI state, derived state, ownership, reset conditions, and mapped `SM-xx` states.
6. Map lifecycle and user actions to `API-xx` operations and `SQ-xx` sequences, including loading, success, empty, failure, permission, cancellation, and refresh behavior.
7. Describe validation, feedback, recovery, concurrency, and API-contract gaps.
8. Split implementation work into dependency-ordered `FE-xx` tasks with scope, inputs, outputs, dependencies, and acceptance checks.
9. Add a traceability matrix linking requirements, `CL`, `UF`, `SM`, `SQ`, `API`, and task IDs.

## Keep the plan reviewable

- Include no unapproved assumptions or unresolved business decisions; route them back to the clarification gate.
- Keep tasks framework-neutral unless the user supplied a target stack.
- Do not infer components, APIs, permissions, or error behavior without evidence.
- Do not include source-code snippets or scan unrelated repository code for background.
- Preserve reviewer notes, approved decisions, and manual overrides when updating an existing plan.

## Validate

Verify that the clarification gate passes, every confirmed decision is implemented in the plan, every in-scope user goal is covered by a flow, every async interaction has modeled states, every API operation appears in a sequence, every declared failure has visible handling, and every task has a testable completion condition. Finish with a review checklist; if a blocker remains, do not finalize the plan.
