---
name: requirement-clarification-generator
description: Compare a product PRD, frontend prototype, and backend API contract to detect conflicts, missing rules, and ambiguous interaction or API decisions, then create and maintain frontend-design/{feature-name}/clarification.md as a mandatory pipeline gate. Use before any user-flow, state-machine, sequence-diagram, or frontend-plan generation, when source documents change, or whenever a downstream skill discovers a new unresolved decision.
---

# Requirement Clarification Generator

Create and maintain only `frontend-design/<feature-name>/clarification.md`. Never generate downstream artifacts or application code.

## Require and inventory inputs

Require the product PRD, readable prototype evidence, and backend API PRD, OpenAPI, or equivalent contract. Treat a missing source as a clarification question rather than filling the gap. Use the explicit feature name and output root when supplied; otherwise derive a lowercase kebab-case feature name only when the PRD makes it unambiguous.

## Audit uncertainty

1. Read `prompt.md` for the artifact contract and `examples/customer-management.md` for the lifecycle shape.
2. Inventory sources with filenames, URLs, PRD sections, prototype frames, and API operations.
3. Compare PRD ↔ prototype, PRD ↔ API, and prototype ↔ API.
4. Check interaction form, navigation, validation, confirmation, permission, loading, empty, success, failure, retry, cancellation, refresh, bulk/single behavior, pagination, concurrency, and data preservation where relevant.
5. Assign each consequential issue a stable `CL-xx` ID. State the conflicting evidence, frontend impact, and one focused question. Offer choices only when the sources establish a bounded set; always allow the user to supply another decision.
6. Never choose an endpoint, UI pattern, permission rule, or business behavior on the user's behalf.

## Manage the gate

Always write `clarification.md`:

- Set `Status: Cleared` and `Gate: PASS` when no consequential questions exist.
- Set `Status: Waiting Confirmation` and `Gate: BLOCKED` when any `CL-xx` item is unresolved. Ask the user the focused questions and stop the pipeline.
- After the user answers, update the same items with the confirmed decision and evidence. Set `Status: Resolved` and `Gate: PASS` only when every blocking item is resolved.

Preserve question IDs, user-approved decisions, reviewer notes, and resolution history when inputs change. Reopen an item instead of deleting its history when new evidence invalidates a decision.

## Hand off

Permit `user-flow-generator` only when the gate passes. The handoff must list the status, confirmed `CL-xx` decisions, source versions, and any explicitly non-blocking observations. If a downstream skill returns a new ambiguity, append or reopen the relevant item, set the gate to blocked, and pause again.
