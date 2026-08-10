---
name: sequence-diagram-generator
description: Map approved user flows and frontend state machines to a backend API PRD or OpenAPI contract, producing evidence-backed frontend/backend interaction sequences with request, response, error, and UI-state transitions. Use when Codex is asked to determine which user action calls which endpoint, visualize browser-to-backend behavior, or write frontend-design/{feature-name}/sequence-diagram.md after user-flow.md and state-machine.md exist.
---

# Sequence Diagram Generator

Create only `frontend-design/<feature-name>/sequence-diagram.md`. Do not generate code or write the other pipeline artifacts.

## Require inputs

Require approved `user-flow.md`, `state-machine.md`, and a readable backend API PRD, OpenAPI document, or equivalent interface contract. If a required source is missing, identify it and pause. Do not derive endpoints from UI labels.

## Map interactions

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Build an API inventory with method, path, purpose, authentication, request fields, response shape, declared errors, and source location.
3. Map each API-triggering `UF-xx` action to the affected `SM-xx` transition. Assign a stable sequence ID such as `SQ-01`.
4. Create one sequence per meaningful load or mutation flow. Do not create a separate diagram for trivial clicks that never cross a system boundary.
5. Use `User`, `Frontend`, and `Backend API` as baseline participants. Add gateways, services, databases, or third parties only when the supplied contract explicitly exposes them.
6. Show client-side validation short-circuits, request dispatch, response handling, visible state changes, refreshes, retries, cancellation, and declared error branches.
7. Write Mermaid `sequenceDiagram` blocks and a traceability table.

## Preserve the API contract

- Copy method and path exactly from the source.
- Summarize fields; do not invent request parameters, response properties, status codes, idempotency, pagination, or permissions.
- Label contract gaps `API-GAP-xx` and explain their frontend impact.
- Resolve contradictions only with explicit user direction; otherwise record them as open questions.
- Preserve reviewer notes and manual decisions when updating an existing artifact.

## Validate and hand off

Verify that every called endpoint exists in the API inventory, every request corresponds to a user action or lifecycle event, every response reaches a modeled UI state, and success/failure branches agree with the state machine. End with the sequences and API gaps that `frontend-plan-generator` must consume.
