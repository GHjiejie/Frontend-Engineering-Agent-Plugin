# Local Export Contract

## Fixed-revision export

Fetch the exact reviewed Revision as Markdown. With current lark-cli v2 semantics the shape is:

```text
lark-cli docs +fetch --api-version v2 --doc <doc> \
  --doc-format markdown --revision-id <revision-id>
```

Always follow the installed CLI's version-matched instructions if its flags differ.

The command returns document content inside structured output; extract the content deliberately instead of redirecting the entire JSON response into the Markdown file.

## Required plan header

```markdown
Status: Ready for Technical Review | Ready for Development | Sync Drift | Blocked

## Review Source

- Feishu Document: <URL>
- Feishu Revision: <revision-id>
- Synced At: <timestamp with timezone>
- Export Mode: cloud-media | offline-media
```

## sync-manifest.json

Required fields:

```json
{
  "feature": "customer-management",
  "version": "2026-08-10",
  "feishuDocumentUrl": "https://example.feishu.cn/docx/xxx",
  "feishuDocumentToken": "doxcnxxx",
  "feishuRevisionId": 42,
  "syncedAt": "2026-08-10T16:20:00+08:00",
  "exportMode": "cloud-media",
  "syncedFiles": ["frontend-development-plan.md"],
  "prototypeIds": ["PT-01", "PT-02"],
  "fileDigests": {
    "frontend-development-plan.md": "<sha256>"
  },
  "status": "in-sync"
}
```

An `in-sync` package must include SHA-256 digests for synchronized files so later exports can detect local drift before overwrite.

## Drift rules

- Store and compare a SHA-256 digest for every synchronized file when available.
- If the current local file differs from the last synchronized digest, do not overwrite it.
- Set the visible Plan status and manifest status to `Sync Drift` / `drift` until the developer chooses which change to preserve.
- Never perform an automatic two-way merge of business decisions.

## Media rules

- `cloud-media`: preserve linked `PRD-xx` / `API-xx` file-card or canonical-source targets plus every linked `PT-xx`, `UF-xx`, `SM-xx`, and `SQ-xx` block target.
- `offline-media`: download source attachments to `assets/sources/`, prototype images to `assets/prototype/`, and rendered diagrams to `assets/diagrams/`; use deterministic filenames beginning with the matching stable ID, point each navigable ID to its local asset or anchor, and record exported files in the source manifest.
- Do not use expiring signed media URLs in either mode.
- Do not strip links from source or visual-artifact IDs during fixed-revision Markdown export. If the export format loses attachment/block-link semantics, Gate #5 remains blocked until the links are restored and the fixed revision is exported again.
