---
name: frontend-plan-generator
description: Assemble a product PRD, frontend prototype, backend API contract, approved user flow, state machine, and sequence diagrams into an implementation-ready but code-free frontend development plan. Use when Codex is asked for the final frontend delivery方案, task breakdown, page/component design, state strategy, API calling plan, exception handling, or an end-to-end frontend interaction design package written to frontend-design/{feature-name}/frontend-development-plan.md.
---

# Frontend Plan Generator

Create only `frontend-design/<feature-name>/frontend-development-plan.md`. Never generate or modify application code, create business components, commit changes, or open a pull request.

## Enforce the pipeline

Require the product PRD, prototype, API contract, `user-flow.md`, `state-machine.md`, and `sequence-diagram.md`.

For an end-to-end request where intermediate artifacts do not yet exist, use the other plugin skills in this strict order:

1. `user-flow-generator`
2. `state-machine-generator`
3. `sequence-diagram-generator`
4. Return here only after all three outputs are available.

If a required source is missing or a blocking open question makes the plan materially ambiguous, name the missing evidence and pause. Do not collapse the pipeline into an untraceable single-pass summary.

## Assemble the plan

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Reconcile the six inputs. Record conflicts instead of silently preferring one source.
3. Summarize feature scope, actors, business rules, explicit non-goals, and acceptance outcomes.
4. Define a semantic page/component tree based on visible responsibilities, without prescribing framework source files.
5. Define page data, transient UI state, derived state, ownership, reset conditions, and mapped `SM-xx` states.
6. Map lifecycle and user actions to `API-xx` operations and `SQ-xx` sequences, including loading, success, empty, failure, permission, cancellation, and refresh behavior.
7. Describe validation, feedback, recovery, concurrency, and API-contract gaps.
8. Split implementation work into dependency-ordered `FE-xx` tasks with scope, inputs, outputs, dependencies, and acceptance checks.
9. Add a traceability matrix linking requirements or source sections to `UF`, `SM`, `SQ`, `API`, and task IDs.

## Keep the plan reviewable

- Mark every assumption and unresolved decision explicitly.
- Keep tasks framework-neutral unless the user supplied a target stack.
- Do not infer components, APIs, permissions, or error behavior without evidence.
- Do not include source-code snippets or scan unrelated repository code for background.
- Preserve reviewer notes, approved decisions, and manual overrides when updating an existing plan.

## Validate

Verify that every in-scope user goal is covered by a flow, every async interaction has modeled states, every API operation appears in a sequence, every declared failure has visible handling, and every task has a testable completion condition. Finish with a review checklist and a clear list of blockers that must be resolved before coding begins.
