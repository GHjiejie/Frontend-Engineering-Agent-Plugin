---
name: state-machine-generator
description: Convert an approved versioned user-flow artifact, frontend prototype, and confirmed decisions into explicit page and component state models with transition tables and Mermaid diagrams. Use to define loading, empty, data, error, dialog, submitting, success, failed, disabled, cancellation, or recovery behavior only after the project, version, and clarification gates pass.
---

# State Machine Generator

Create only `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/state-machine.md`. Do not generate code or write the user-flow, sequence, or plan artifacts.

## Require inputs

Require `clarification.md` with confirmed project/feature/version context and `Gate: PASS`, the approved `user-flow.md` from that same directory, and readable prototype evidence. If any input is unavailable, paths disagree, or a gate is blocked, return to `requirement-clarification` and pause without creating or updating `state-machine.md`. Never select a different project or version.

## Model states

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Build a coverage matrix from each `UF-xx` step to the page or component that renders feedback.
3. Model a page state for every asynchronous data surface. Consider `loading`, `empty`, `data`, and `error` only when relevant.
4. Model component states such as dialog open/close, submitting, success, failed, disabled, retry, and cancellation only when evidence or confirmed `CL-xx` decisions require them. Do not manufacture states merely for completeness.
5. Assign stable state-machine IDs such as `SM-01` and stable event names such as `LOAD`, `SUBMIT`, `RESOLVE`, `REJECT`, and `CANCEL`.
6. Define every transition as current state + event + optional guard + next state + visible effect.
7. If any guard, transition, feedback, reset, retry, or cancellation behavior is unresolved, return it to `requirement-clarification` in the same version, block the gate, and stop.
8. Write Mermaid `stateDiagram-v2` diagrams and transition tables with `CL-xx` traceability.

## Preserve evidence

- Link each state machine to one or more `UF-xx` flows and prototype views.
- Separate persistent data from transient UI state.
- Never model unspecified guards, retry behavior, disabled behavior, or data preservation as if confirmed.
- Do not invent API endpoints, backend behavior, or source-code architecture.
- Preserve reviewer notes and manual decisions when updating an existing artifact.

## Validate and hand off

Verify that the artifact path matches the confirmed context, every event has a valid source state, all async paths have confirmed success and failure outcomes, cancellation has a confirmed target or is confirmed unavailable, visible effects agree with evidence, and no state is unreachable. End with a handoff confirming all gates still pass and listing state IDs for `sequence-diagram-generator`.
