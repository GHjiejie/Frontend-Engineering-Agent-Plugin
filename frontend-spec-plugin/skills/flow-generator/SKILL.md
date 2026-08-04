---
name: flow-generator
description: Generate Mermaid sequence diagrams and explicit frontend page or component state models from approved interaction specifications. Use when Codex must visualize user-to-UI-to-API sequences, async responses, alternative error paths, loading, success, empty, failure, disabled, and permission states.
---

# Flow Generator

Write `frontend-spec/flow/sequence-diagrams.md` and `frontend-spec/flow/state-models.md`.

## Generate diagrams

1. Read `../../references/artifact-contract.md`, the interaction specification, and interaction review.
2. Refuse to generate diagrams unless `review_status` is `approved`, the approval object exists, and `approval.revision` equals the current interaction `revision`.
3. Generate one Mermaid sequence diagram per meaningful user flow, not per trivial click.
4. Use stable participant names and annotate each diagram with mapped `RQ`, `UI`, `API`, and `IX` IDs.
5. Include validation short-circuits, success responses, declared error branches, refreshes, and cancellation where applicable.
6. Generate a state model for every async or multi-step page/component. Define initial state, events, guarded transitions, terminal or recoverable states, and rendered feedback.

## Verify consistency

Mermaid must parse syntactically. Every state and branch must exist in the approved interaction revision; report a conflict instead of adding behavior. Update the `flow-generation` stage with the produced paths and unresolved visualization gaps.
