---
name: frontend-spec-generator
description: Assemble approved requirements, decisions, UI trees, API mappings, interaction bindings, and flow diagrams into an implementation-ready frontend development specification. Use when Codex must produce the final engineering handoff for a frontend feature from requirement, prototype, and interface evidence without scanning the wider project or generating source code.
---

# Frontend Spec Generator

Write `<feature-root>/document/frontend-development-spec.md` using `../../assets/templates/frontend-development-spec.md`.

## Assemble the specification

1. Read `../../references/artifact-contract.md` and every completed pipeline artifact.
2. Preserve human overrides using the change-tracker skill.
3. Include scope, non-goals, source inventory, page and UI structure, data models, API contracts, page states, user interactions, diagrams, proposed component responsibilities, proposed API/state/type responsibilities, validation, permissions, error handling, accessibility, tests, rollout considerations, open items, and traceability.
4. Reference stable IDs rather than duplicating or silently rewriting authoritative decisions.
5. Separate required implementation from recommendations and assumptions.

## Readiness status

Set exactly one status near the top:

- `ready_for_implementation`: no blocking questions, contract conflicts, required design gaps, or unmapped requirements remain.
- `blocked`: list each blocker, owner, affected IDs, and the evidence needed to resolve it.

Do not claim file names or components already exist unless the user explicitly supplied the relevant frontend code as evidence. Label all proposed file names and component boundaries as `proposed`. Do not search the project to verify them and do not generate application code.
