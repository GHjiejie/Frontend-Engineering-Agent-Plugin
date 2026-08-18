# Feishu Review Document Contract

Use this order:

1. Title: `[Frontend Design] <Feature> / <Version>`.
2. Status and review guide.
3. Feature background and business problem.
4. Target users and scenarios.
5. Source inventory and versions.
6. Prototype catalog with inline images and `PT-xx` captions.
7. Scope and explicit non-goals.
8. Requirement clarification and confirmed decisions.
9. Page/component responsibility tree.
10. User Flow: one inline rendered visual per `UF-xx`, with ID/title caption, summary, and evidence IDs.
11. Frontend State Model: one inline rendered visual per `SM-xx`, with ID/title caption, ownership/reset summary, and evidence IDs.
12. API plan and Sequence Diagrams: one inline rendered visual per `SQ-xx`, with ID/title caption and `UF` / `SM` / `API` mapping.
13. Exceptions and boundaries.
14. Development task breakdown and acceptance criteria.
15. Traceability matrix.
16. Unresolved issues.
17. Technical Review checklist and notes.
18. Revision and local snapshot metadata.

The opening sections must let an uninvolved reviewer answer why the feature exists, who uses it, what is in scope, what the prototype shows, and which decisions are confirmed without opening the source chat.

## Review-surface completeness

- The Feishu document must contain the actual User Flow, State Machine, and Sequence Diagram visuals. Local Markdown artifacts are structured composition sources and Coding Agent inputs, not reviewer-accessible substitutes.
- Never write only “详见/参考 `user-flow.md`”, `state-machine.md`, or `sequence-diagram.md`. A local path may appear as engineering metadata only after the full review content is present.
- Place each visual directly below its `UF-xx`, `SM-xx`, or `SQ-xx` heading. Keep a text summary and trace IDs adjacent so reviewers can still understand the behavior when media preview fails.
- Use Feishu image/media blocks for the visual review surface. Do not rely on a Mermaid fenced code block being rendered by Feishu.
- Preserve diagram labels and captions during same-version updates; replace the image for a changed ID rather than appending an ambiguous duplicate.

Use durable document or block anchors for evidence references. Do not embed expiring download URLs as canonical sources.

## Linked visual-artifact IDs

The stable IDs are also the document's navigation surface:

- Link every standalone `PT-xx`, `UF-xx`, `SM-xx`, and `SQ-xx` occurrence in prose, lists, and table cells.
- `PT-xx` jumps to its exact prototype image block. If Feishu cannot link an image block directly, link the uniquely paired caption block immediately adjacent to that image.
- `UF-xx`, `SM-xx`, and `SQ-xx` jump to their exact diagram block. Fall back to the canonical section-heading block only when direct diagram linking is unavailable.
- Link each ID separately when several appear together; one combined link must not represent multiple targets.
- Keep original source locators, such as Figma node URLs, separately. They do not replace Review-document block links.
- Canonical destination headings and IDs rendered inside diagrams/code blocks do not link to themselves.

Resolve block links only after the final document structure exists, then verify every target against the published document. A generic document-home URL, an inaccessible or mismatched block, an expiring media/download URL, or an unlinked visual ID fails Reviewability Gate #5.

Preserve existing review comments and approved notes when republishing the same feature/version.
