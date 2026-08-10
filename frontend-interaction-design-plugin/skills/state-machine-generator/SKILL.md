---
name: state-machine-generator
description: Convert an approved user-flow artifact, frontend prototype, and passed clarification gate into explicit page and component state models with transition tables and Mermaid diagrams. Use when Codex is asked to define loading, empty, success, error, dialog, submitting, permission, cancellation, or recovery behavior, or to write frontend-design/{feature-name}/state-machine.md after clarification.md and user-flow.md are approved.
---

# State Machine Generator

Create only `frontend-design/<feature-name>/state-machine.md`. Do not generate code or write the user-flow, sequence, or plan artifacts.

## Require inputs

Require `clarification.md` with `Gate: PASS`, the approved `user-flow.md`, and readable prototype evidence. If any input is unavailable or the gate is blocked, pause without creating or updating `state-machine.md`.

## Model states

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Build a coverage matrix from each `UF-xx` step to the page or component that renders feedback.
3. Model a page state for every asynchronous data surface. Consider `idle`, `loading`, `empty`, `success`, `error`, and `permission-denied` only when relevant.
4. Model a component state for every dialog, form, upload, destructive confirmation, or multi-step control. Include opened/closed, editing, validating, submitting, success, failure, retry, and cancellation only when evidence or confirmed `CL-xx` decisions require them.
5. Assign stable state-machine IDs such as `SM-01` and stable event names such as `LOAD`, `SUBMIT`, `RESOLVE`, `REJECT`, and `CANCEL`.
6. Define every transition as current state + event + optional guard + next state + visible effect.
7. If any guard, transition, feedback, reset, retry, or cancellation behavior is unresolved, return it to `requirement-clarification-generator`, block the gate, and stop.
8. Write Mermaid `stateDiagram-v2` diagrams and transition tables with `CL-xx` traceability.

## Preserve evidence

- Link each state machine to one or more `UF-xx` flows and prototype views.
- Separate persistent data from transient UI state.
- Never model unspecified guards, retry behavior, disabled behavior, or data preservation as if confirmed.
- Do not invent API endpoints, backend behavior, or source-code architecture.
- Preserve reviewer notes and manual decisions when updating an existing artifact.

## Validate and hand off

Verify that every event has a valid source state, all async paths have confirmed success and failure outcomes, cancellation has a confirmed target or is confirmed unavailable, visible effects agree with evidence, and no state is unreachable. End with a handoff confirming the gate still passes and listing state IDs for `sequence-diagram-generator`.
