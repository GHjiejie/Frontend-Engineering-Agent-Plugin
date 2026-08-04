---
name: interaction-designer
description: Bind product requirements, UI elements, API operations, and frontend state into complete interaction specifications. Use when Codex must define click, submit, search, pagination, navigation, dialog, upload, mutation, and recovery flows with validation, loading, success, error, permission, concurrency, and refresh behavior.
---

# Interaction Designer

Write `frontend-spec/interaction/interaction-spec.json`. Treat this as the central binding artifact.

## Design each interaction

1. Read `../../references/artifact-contract.md` and `../../schemas/interaction-spec.schema.json`.
2. Use only approved requirements, parsed UI IDs, API IDs, project constraints, and recorded decisions.
3. Assign stable IDs `IX-###`.
4. Capture requirement IDs, element IDs, event, preconditions, client validation, ordered actions, API calls, state transitions, success feedback, error mapping, retry/recovery, cancellation, refresh or cache invalidation, permission behavior, and postconditions.
5. Cover duplicate submission, stale data, destructive confirmation, optimistic versus pessimistic update, partial failure, focus management, and accessibility feedback when relevant.

## Enforce coverage

- Every interactive UI element must map to an interaction or be explicitly decorative/read-only.
- Every user-facing requirement must map to one or more interactions.
- Every API mutation must define pending, success, failure, and retry or recovery behavior.
- Do not hide contract or design gaps inside prose. Add them to `unmapped_requirements` or `conflicts`.

Complete the stage only when traceability is bidirectional or the remaining gaps are explicitly blocking.
