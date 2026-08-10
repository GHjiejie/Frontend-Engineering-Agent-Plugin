---
name: requirement-clarification
description: Compare a persisted Product PRD, durable prototype evidence, backend API contract, and prior confirmed decisions for one confirmed frontend project/feature/version, then record consequential questions and developer decisions in clarification.md. Use after source-evidence-manager passes Source Gate #3, when source versions change, or whenever a downstream artifact reveals ambiguity affecting flows, states, APIs, permissions, validation, errors, or implementation.
---

# Requirement Clarification

Create or update only `<confirmed-output-directory>/clarification.md`. Do not collect ephemeral prototype evidence, generate downstream models, publish a review document, or modify application code.

## Require preflight and evidence

Require:

- Developer-confirmed project root, feature, version, and output directory from Gates #1 and #2.
- `source-manifest.md` from that exact directory with `Source Gate: PASS`.
- Readable PRD, `PT-xx` prototype evidence, and `API-xx` contract entries from the manifest.

If confirmed context is absent, route to `frontend-plan-generator` preflight. If a source is missing, inaccessible, chat-only, or the source gate is blocked, route to `source-evidence-manager` and pause without writing `clarification.md`.

Read `prompt.md` for the artifact contract and the example when a concrete lifecycle is useful.

## Audit consequential uncertainty

1. Compare PRD ↔ prototype, PRD ↔ API, prototype ↔ API, and all sources ↔ prior decisions.
2. Check validation, permissions, confirmations, loading, empty, success, failure, retry, cancellation, refresh, pagination, bulk/single behavior, concurrency, idempotency, and data preservation where relevant.
3. Assign each consequential issue a stable `CL-xx` and cite exact `PRD-xx`, `PT-xx`, and `API-xx` evidence.
4. State the frontend impact and ask one focused question. Offer bounded options only when evidence supports them, while allowing another developer decision.
5. Never choose a source version, endpoint, UI pattern, permission rule, error policy, or business rule for the developer.

## Manage Clarification Gate #4

- `Status: Cleared`, `Clarification Gate: PASS` when no consequential issue exists.
- `Status: Waiting Confirmation`, `Clarification Gate: BLOCKED` while any `CL-xx` is Open or Reopened.
- `Status: Resolved`, `Clarification Gate: PASS` after every blocker receives a developer-confirmed decision.

Developer-confirmed decisions outrank conflicting source documents. Preserve stable IDs, decision history, reviewer notes, and manual overrides; reopen invalidated items instead of deleting them.

## Hand off

Permit `user-flow-generator` only when Source Gate #3 and Clarification Gate #4 pass. Hand off the exact paths, source IDs, Feishu evidence location, gate status, and resolved `CL-xx` decisions. A downstream ambiguity returns to this same version and blocks regeneration.
