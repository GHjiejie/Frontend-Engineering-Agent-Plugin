---
name: sequence-diagram-generator
description: Map approved UF-xx flows and SM-xx frontend states to a confirmed API-xx backend contract, producing request, response, error, refresh, cancellation, and visible UI-state sequences for one confirmed feature version. Use after source and clarification gates pass to create sequence-diagram.md without inventing endpoints or backend internals.
---

# Sequence Diagram Generator

Create only `<confirmed-output-directory>/sequence-diagram.md`. Do not generate code or write other pipeline artifacts.

## Require inputs

Require same-version `source-manifest.md` with `Source Gate: PASS`, `clarification.md` with `Clarification Gate: PASS`, approved `user-flow.md`, `state-machine.md`, and a readable `API-xx` contract. Route missing API evidence to `source-evidence-manager` and semantic contract gaps to `requirement-clarification`.

## Map interactions

1. Read `prompt.md` and the example when useful.
2. Build an API inventory with exact method/path, purpose, authentication, request/response summary, declared errors, version, and source location.
3. Map each API-triggering `UF-xx` action to an `SM-xx` transition and assign stable `SQ-xx`.
4. Create one sequence per meaningful load or mutation, not for clicks that never cross a system boundary.
5. Use `User`, `Browser / Frontend`, and `Backend / BFF` as baseline participants. Add downstream services only when source evidence exposes them.
6. Show client validation, dispatch, responses, UI transitions, refreshes, retries, cancellation, and declared errors only when confirmed.
7. Reopen clarification for missing or conflicting endpoint, request, response, error, permission, pagination, idempotency, or cancellation behavior.

## Preserve the contract

Copy method/path exactly. Never invent parameters, fields, codes, permissions, databases, or internal services. Preserve reviewer notes and approved decisions.

## Validate and hand off

Verify every endpoint exists in the API inventory, every request has a user/lifecycle trigger, every confirmed response reaches a modeled UI state, and branches agree with `SM-xx` and `CL-xx`. Hand off stable `SQ-xx` and `API-xx` IDs to `frontend-plan-generator`.
