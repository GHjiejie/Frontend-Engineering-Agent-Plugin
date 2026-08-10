---
name: sequence-diagram-generator
description: Map approved user flows and frontend state machines to a confirmed backend API contract after the clarification gate passes, producing frontend/backend interaction sequences with request, response, error, and UI-state transitions. Use when Codex is asked which action calls which endpoint or to write frontend-design/{feature-name}/sequence-diagram.md after clarification.md, user-flow.md, and state-machine.md are approved.
---

# Sequence Diagram Generator

Create only `frontend-design/<feature-name>/sequence-diagram.md`. Do not generate code or write the other pipeline artifacts.

## Require inputs

Require `clarification.md` with `Gate: PASS`, approved `user-flow.md`, `state-machine.md`, and a readable backend API PRD, OpenAPI document, or equivalent interface contract. If a source is missing or the gate is blocked, pause without creating or updating `sequence-diagram.md`. Do not derive endpoints from UI labels.

## Map interactions

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Build an API inventory with method, path, purpose, authentication, request fields, response shape, declared errors, and source location.
3. Map each API-triggering `UF-xx` action to the affected `SM-xx` transition. Assign a stable sequence ID such as `SQ-01`.
4. Create one sequence per meaningful load or mutation flow. Do not create a separate diagram for trivial clicks that never cross a system boundary.
5. Use `User`, `Frontend`, and `Backend API` as baseline participants. Add gateways, services, databases, or third parties only when the supplied contract explicitly exposes them.
6. Show client-side validation short-circuits, request dispatch, response handling, visible state changes, refreshes, retries, cancellation, and declared error branches only when their behavior is confirmed.
7. Route any missing or conflicting endpoint, request, response, error, permission, idempotency, pagination, or cancellation decision back to `requirement-clarification-generator`; block the gate and stop.
8. Write Mermaid `sequenceDiagram` blocks and a traceability table with `CL-xx` references.

## Preserve the API contract

- Copy method and path exactly from the source.
- Summarize fields; do not invent request parameters, response properties, status codes, idempotency, pagination, or permissions.
- Never leave an API contract gap inside a completed sequence artifact; convert consequential gaps into `CL-xx` questions before generation.
- Resolve contradictions only through explicit user decisions recorded in `clarification.md`.
- Preserve reviewer notes and manual decisions when updating an existing artifact.

## Validate and hand off

Verify that every called endpoint exists in the API inventory, every request corresponds to a user action or lifecycle event, every confirmed response reaches a modeled UI state, and success/failure branches agree with the state machine and clarification decisions. End with a gate confirmation and the sequences that `frontend-plan-generator` may consume.
