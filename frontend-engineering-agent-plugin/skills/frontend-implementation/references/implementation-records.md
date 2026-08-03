# Implementation records

## Change log

Write `docs/frontend-ai/reports/<feature-id>-change-log.md` with:

1. Feature id and implementation timestamp.
2. Contract criteria implemented, using their stable ids.
3. Files created, modified, moved, or deleted with concise reasons.
4. User-visible behavior changes.
5. API, state, route, component, style, accessibility, and test changes.
6. Deviations from `implementation.yaml`, their approval state, and consequences.
7. Commands executed and pass, fail, or not-run status.
8. Known limitations, follow-ups, and rollback notes.
9. Durable memory files updated.

## Feature history

Append an entry to `history.yaml` rather than replacing earlier entries:

```yaml
entries:
  - at: 2026-08-03T00:00:00Z
    from: DESIGNED
    to: IMPLEMENTING
    orchestratorState: IMPLEMENTING
    summary: "Implementation started"
    evidence: docs/frontend-ai/reports/customer-import-change-log.md
```

## Memory update rules

- Add project-index entries only when their paths exist.
- Record capability-oriented evolution events only after review passes; Git already records raw file changes.
- Update architecture memory only for an established pattern or approved decision, not a one-off implementation detail.
- Record business rules with their source and confidence.
- Update timestamps and source revision in `memory-index.json` after successful verification.
- Never erase older feature history or ADRs to make current state appear cleaner.
