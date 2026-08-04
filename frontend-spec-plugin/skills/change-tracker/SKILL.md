---
name: change-tracker
description: Preserve manual overrides, approved decisions, and regeneration history for frontend specification artifacts. Use when Codex updates, regenerates, compares, or reconciles an existing frontend specification after requirement, API, design, project, or developer feedback changes.
---

# Change Tracker

Maintain `frontend-spec/manual/override.md` and `frontend-spec/history/change-log.json` before modifying existing generated artifacts.

## Reconcile changes

1. Read `../../references/artifact-contract.md`, `../../schemas/change-log.schema.json`, current artifacts, decision log, and manual overrides.
2. Compare source inputs and generated sections using stable IDs.
3. Classify each change as `source_update`, `decision`, `manual_override`, `generated_update`, `conflict`, or `superseded`.
4. Preserve an active manual override unless the user explicitly accepts a replacement.
5. When an override conflicts with a new authoritative source, keep both, mark the affected section blocked, and request disposition.
6. Append a change record with timestamp, actor, type, affected IDs, artifact, section, before/after summary, rationale, and superseded entry when applicable.

Never rewrite history entries. Never treat generated text as higher authority than a confirmed human decision. Report preserved overrides and unresolved conflicts after regeneration.
