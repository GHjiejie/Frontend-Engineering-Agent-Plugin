---
name: sequence-diagram-generator
description: Map approved versioned user flows and frontend state machines to a confirmed backend API contract, producing frontend/backend interaction sequences with request, response, error, and UI-state transitions. Use to show which action calls which endpoint or write sequence-diagram.md only after the project, version, and clarification gates pass.
---

# Sequence Diagram Generator

Create only `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/sequence-diagram.md`. Do not generate code or write the other pipeline artifacts.

## Require inputs

Require `clarification.md` with confirmed project/feature/version context and `Gate: PASS`, approved `user-flow.md` and `state-machine.md` from that same directory, and a readable backend API PRD, OpenAPI document, or equivalent contract. If a source is missing, paths disagree, or a gate is blocked, return to `requirement-clarification` and pause without creating or updating `sequence-diagram.md`. Never select another project/version or derive endpoints from UI labels.

## Map interactions

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Build an API inventory with method, path, purpose, authentication, request fields, response shape, declared errors, and source location.
3. Map each API-triggering `UF-xx` action to the affected `SM-xx` transition. Assign a stable sequence ID such as `SQ-01`.
4. Create one sequence per meaningful load or mutation flow. Do not create a separate diagram for trivial clicks that never cross a system boundary.
5. Use `User`, `Browser / Frontend`, and `Backend / BFF` as baseline participants. Add downstream services only when supplied evidence explicitly exposes them. Never invent a database or internal service.
6. Show client-side validation short-circuits, request dispatch, response handling, visible state changes, refreshes, retries, cancellation, and declared error branches only when their behavior is confirmed.
7. Route any missing or conflicting endpoint, request, response, error, permission, idempotency, pagination, or cancellation decision back to `requirement-clarification` in the same version; block the gate and stop.
8. Write Mermaid `sequenceDiagram` blocks and a traceability table with `CL-xx` references.

## Preserve the API contract

- Copy method and path exactly from the source.
- Summarize fields; do not invent request parameters, response properties, status codes, idempotency, pagination, or permissions.
- Never leave an API contract gap inside a completed sequence artifact; convert consequential gaps into `CL-xx` questions before generation.
- Resolve contradictions only through explicit user decisions recorded in `clarification.md`.
- Preserve reviewer notes and manual decisions when updating an existing artifact.

## Validate and hand off

Verify that the artifact path matches the confirmed context, every called endpoint exists in the API inventory, every request corresponds to a user action or lifecycle event, every confirmed response reaches a modeled UI state, and success/failure branches agree with the state machine and clarification decisions. End with confirmation that all gates still pass and the sequences that `frontend-plan-generator` may consume.
