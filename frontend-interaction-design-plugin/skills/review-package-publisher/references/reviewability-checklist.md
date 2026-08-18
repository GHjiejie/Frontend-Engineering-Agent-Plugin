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
- Every standalone `PT-xx`, `UF-xx`, `SM-xx`, and `SQ-xx` reference in prose, lists, and table cells is individually linked to its exact image, diagram, or canonical section block; canonical target headings and diagram/code contents are exempt.
- Every visual-artifact link resolves inside the expected Review document, points to the matching ID, and does not fall back to the document home or an expiring media URL when a precise block target is available.
- Reviewers can access the document, or the Plan contains a durable replacement summary.

## Plan consistency

- Every in-scope user goal has a `UF-xx`.
- Every `UF-xx` appears in the Feishu Plan as a labeled inline flowchart plus a plain-language summary; a `user-flow.md` reference alone fails the gate.
- Every asynchronous UI surface has a relevant `SM-xx` success/failure model.
- Every `SM-xx` appears in the Feishu Plan as a labeled inline state visual plus ownership/reset behavior; a `state-machine.md` reference alone fails the gate.
- Every API operation used by the feature appears in an `SQ-xx` and API mapping.
- Every `SQ-xx` appears in the Feishu Plan as a labeled inline sequence visual plus its `UF` / `SM` / `API` mapping; a `sequence-diagram.md` reference alone fails the gate.
- Every declared failure has visible handling.
- Every `FE-xx` task has a testable acceptance condition.
- Every confirmed `CL-xx` decision appears in affected downstream artifacts.

## Sync

- The local Plan records the Feishu URL and exact Revision.
- `sync-manifest.json` is valid and reports `in-sync`.
- No unresolved local modification conflict exists.
- Media and visual-artifact ID links are stable, or offline media and local anchors exist as declared.
- The fetched fixed Revision still contains an image/media reference for every expected `UF-xx`, `SM-xx`, and `SQ-xx` in the correct Plan section.

## Status

- Gate #5 may yield `Ready for Technical Review` before human approval.
- `Ready for Development` additionally requires recorded Technical Review approval against the same synchronized Revision.
