# Source Manifest Contract

Write `<confirmed-output-directory>/source-manifest.md` in this order:

1. `# <Feature> Source Manifest`
2. `Status: Ready | Waiting Source`
3. `Source Gate: PASS | BLOCKED`
4. `## Confirmed Context`
5. `## Feishu Review Document`
6. `## Source Inventory`
7. `## Prototype Catalog`
8. `## Access and Scope Findings`
9. `## Blocking Source Issues`
10. `## Downstream Handoff`

Use these tables:

```markdown
| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |

| Document URL | Document Token | Planned Title | Access Status |
| --- | --- | --- | --- |

| Source ID | Type | Title | Locator | Version / Revision | Captured At | Scope | Access | Evidence Location | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| Prototype ID | Page / State | Preview or Block | Original Source | Captured At | What It Proves | Unknown Behavior |
| --- | --- | --- | --- | --- | --- | --- |

| ID | Issue | Frontend Impact | Required Action | Status |
| --- | --- | --- | --- | --- |
```

Rules:

- Use absolute local paths in confirmed runtime context.
- Use stable Feishu document/block locators, not expiring media download URLs.
- Keep source IDs stable when refreshing evidence; record a new version or capture time instead of renumbering unrelated downstream artifacts.
- Any open blocking issue requires `Status: Waiting Source` and `Source Gate: BLOCKED`.
- Do not place business decisions in this file; route them to `clarification.md`.
