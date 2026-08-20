# Source Manifest Contract

Write `<confirmed-output-directory>/source-manifest.md` in this order:

1. `# <Feature> Source Manifest`
2. `Status: Ready | Waiting Source`
3. `Source Gate: PASS | BLOCKED`
4. `## Confirmed Context`
5. `## Feishu Review Document`
6. `## Source Inventory`
7. `## Source Attachment Catalog`
8. `## Prototype Catalog`
9. `## Access and Scope Findings`
10. `## Blocking Source Issues`
11. `## Downstream Handoff`

Use these tables:

```markdown
| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |

| Document URL | Document Token | Planned Title | Access Status |
| --- | --- | --- | --- |

| Source ID | Type | Title | Locator | Version / Revision | Captured At | Scope | Access | Evidence Location | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| Source ID | Original File | Feishu File Card | File Token | Block ID | Size Bytes | SHA-256 | Uploaded At | Download Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

| Prototype ID | Page / State | Preview / Block Link | Block ID | Original Source | Captured At | What It Proves | Unknown Behavior |
| --- | --- | --- | --- | --- | --- | --- | --- |

| ID | Issue | Frontend Impact | Required Action | Status |
| --- | --- | --- | --- | --- |
```

Rules:

- Use absolute local paths in confirmed runtime context.
- Use stable Feishu document/block locators, not expiring media download URLs.
- For a user-uploaded or local PRD/API source, link its Source ID and title to the exact Feishu file-card block and add a `查看/下载原文件` link. Record the returned file token, block ID, original filename, byte size, SHA-256, upload time, and download verification result in the Source Attachment Catalog.
- Keep canonical cloud-document URLs and repository locators separately from the attachment link. A local path is provenance metadata, not a reviewer-accessible source.
- A static filename or unlinked `PRD-xx` / `API-xx` table cell cannot satisfy Source Gate for a local or uploaded source.
- Make every `PT-xx` in the Prototype Catalog a Markdown link to its exact image block or uniquely paired caption block, and keep the raw block ID in the adjacent field for recovery and validation.
- Do not combine multiple prototype IDs into one link or use the document-home URL when an exact block link exists.
- Keep source IDs stable when refreshing evidence; record a new version or capture time instead of renumbering unrelated downstream artifacts.
- Any open blocking issue requires `Status: Waiting Source` and `Source Gate: BLOCKED`.
- Do not place business decisions in this file; route them to `clarification.md`.
