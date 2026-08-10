# Reviewability Gate Checklist

Gate #5 passes only when every applicable item is true.

## Context

- The Plan explains the business problem, target users, scenarios, scope, and non-goals.
- No consequential fact exists only in the source conversation.
- Terms and business rules needed by an uninvolved reviewer are defined.

## Sources and prototype

- PRD, prototype, and API sources have stable IDs, locators, versions, scopes, and access states.
- Every pasted prototype image is stored in Feishu and has a `PT-xx`, page/state name, and caption.
- Every Figma capture records the exact node/frame URL and capture time.
- Reviewers can access the document, or the Plan contains a durable replacement summary.

## Plan consistency

- Every in-scope user goal has a `UF-xx`.
- Every asynchronous UI surface has a relevant `SM-xx` success/failure model.
- Every API operation used by the feature appears in an `SQ-xx` and API mapping.
- Every declared failure has visible handling.
- Every `FE-xx` task has a testable acceptance condition.
- Every confirmed `CL-xx` decision appears in affected downstream artifacts.

## Sync

- The local Plan records the Feishu URL and exact Revision.
- `sync-manifest.json` is valid and reports `in-sync`.
- No unresolved local modification conflict exists.
- Media references are stable, or offline media exists as declared.

## Status

- Gate #5 may yield `Ready for Technical Review` before human approval.
- `Ready for Development` additionally requires recorded Technical Review approval against the same synchronized Revision.
