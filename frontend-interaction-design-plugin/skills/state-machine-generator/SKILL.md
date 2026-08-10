---
name: state-machine-generator
description: Convert an approved user-flow artifact and frontend prototype into explicit page and component state models with transition tables and Mermaid state diagrams. Use when Codex is asked to define idle, loading, empty, success, error, dialog, submitting, disabled, permission, or recovery behavior, or to write frontend-design/{feature-name}/state-machine.md after user-flow.md is available.
---

# State Machine Generator

Create only `frontend-design/<feature-name>/state-machine.md`. Do not generate code or write the user-flow, sequence, or plan artifacts.

## Require inputs

Require the approved `user-flow.md` and readable prototype evidence. If either is unavailable, identify the missing input and pause. Treat unresolved items from the user flow as constraints; do not resolve them by guessing.

## Model states

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Build a coverage matrix from each `UF-xx` step to the page or component that renders feedback.
3. Model a page state for every asynchronous data surface. Consider `idle`, `loading`, `empty`, `success`, `error`, and `permission-denied` only when relevant.
4. Model a component state for every dialog, form, upload, destructive confirmation, or multi-step control. Include opened/closed, editing, validating, submitting, success, failure, retry, and cancellation where evidence requires them.
5. Assign stable state-machine IDs such as `SM-01` and stable event names such as `LOAD`, `SUBMIT`, `RESOLVE`, `REJECT`, and `CANCEL`.
6. Define every transition as current state + event + optional guard + next state + visible effect.
7. Write Mermaid `stateDiagram-v2` diagrams and transition tables.

## Preserve evidence

- Link each state machine to one or more `UF-xx` flows and prototype views.
- Separate persistent data from transient UI state.
- Mark unspecified guards, retry behavior, disabled behavior, and data preservation as `待确认`.
- Do not invent API endpoints, backend behavior, or source-code architecture.
- Preserve reviewer notes and manual decisions when updating an existing artifact.

## Validate and hand off

Verify that every event has a valid source state, all async paths have success and failure outcomes, cancellation has a defined target, visible effects agree with the prototype, and no state is unreachable. End with a handoff listing state IDs and unresolved gaps for `sequence-diagram-generator`.
