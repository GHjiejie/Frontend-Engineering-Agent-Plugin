---
name: requirement-clarification
description: Discover and confirm the target frontend project and feature version directory, then compare a product PRD, frontend prototype, and backend API contract to record confirmed decisions in clarification.md. Use before any frontend interaction artifact is created, when starting or continuing a feature design iteration, when source documents change, or whenever a downstream skill discovers a consequential ambiguity.
---

# Requirement Clarification

Create or update only `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/clarification.md`. Do not generate downstream artifacts or application code.

## Run the two preflight gates before writing

1. Inspect the current working directory and likely workspace roots read-only. Use `package.json`, `src/`, framework configs, routes, dependencies, and system names in the PRD or prototype as evidence.
2. Present the most likely frontend project name, absolute root, evidence, and confidence. Ask the developer to confirm. If confidence is insufficient, present the viable candidates and wait. Never choose or write on the developer's behalf.
3. Lock the confirmed frontend project root for the task. All downstream skills must reuse it.
4. Resolve a concise lowercase kebab-case feature name from explicit user input or unambiguous evidence.
5. Inspect `<confirmed-root>/docs/frontend-design/<feature-name>/` read-only. Recommend either continuing the latest version or creating a new `YYYY-MM-DD[-vN]` version.
6. Create a new version only for an independent PRD iteration, behavior-changing prototype/API revision, completed-plan successor, or explicit request. Continue the same version for clarification answers, review edits, diagram corrections, and wording changes.
7. Present the feature, action, and exact version path; ask the developer to confirm. Do not create the directory or any artifact until both project and version are confirmed.

## Audit uncertainty

1. Read `prompt.md` for the artifact contract and `examples/customer-management.md` for the lifecycle shape.
2. Require and inventory the PRD, readable prototype evidence, and API PRD, OpenAPI, or equivalent contract. Treat a missing consequential source as a clarification question.
3. Compare PRD ↔ prototype, PRD ↔ API, and prototype ↔ API. Check validation, permissions, confirmations, loading, empty, success, failure, retry, cancellation, refresh, bulk/single behavior, pagination, concurrency, and data preservation where relevant.
4. Assign each consequential issue a stable `CL-xx` ID. State the evidence, frontend impact, and one focused question. Offer bounded options only when supported; allow another developer decision.
5. Never choose a project, version, endpoint, UI pattern, permission rule, business rule, or version of conflicting evidence on the user's behalf.

## Manage the business gate

- Set `Status: Cleared` and `Gate: PASS` when no consequential questions exist.
- Set `Status: Waiting Confirmation` and `Gate: BLOCKED` when any `CL-xx` item is unresolved. Ask the focused questions and stop the pipeline.
- After answers, update the same version's artifact with the confirmed decisions. Set `Status: Resolved` and `Gate: PASS` only when every blocker is resolved.

Treat developer-confirmed decisions as higher priority than conflicting source documents. Preserve IDs, decisions, reviewer notes, and history; reopen an item rather than deleting history when new evidence invalidates it.

## Hand off

Permit `user-flow-generator` only when all three human gates pass. Hand off the confirmed absolute project root, feature name, version, exact output directory, source versions, gate status, and confirmed `CL-xx` decisions. If any downstream skill finds a new ambiguity, update this same `clarification.md`, block the gate, and pause.
