# Frontend Development Plan Output Contract

Write the Draft to `<confirmed-output-directory>/frontend-development-plan.md`. After Feishu publication, `review-package-publisher` replaces it with the exact exported Revision only after drift checks.

Use this section order:

1. `# <Feature> Frontend Development Plan`
2. `Status: Draft | Ready for Publication | Ready for Technical Review | Ready for Development | Sync Drift | Blocked`
3. `## Review Source`
4. `## 1. Review 导读`
5. `## 2. 功能背景与问题`
6. `## 3. 目标用户与使用场景`
7. `## 4. 输入资料与版本`
8. `## 5. 原型页面与状态总览`
9. `## 6. 本次开发范围与非目标`
10. `## 7. 页面与组件职责`
11. `## 8. User Flow`
12. `## 9. 前端状态设计`
13. `## 10. API 使用方案`
14. `## 11. API 与交互 Mapping`
15. `## 12. 异常与边界状态`
16. `## 13. 关键开发决策`
17. `## 14. 开发任务拆分`
18. `## 15. 验收标准`
19. `## 16. 已确认事项`
20. `## 17. 未解决问题`
21. `## 18. 追踪矩阵`
22. `## 19. Technical Review 清单`
23. `## 20. Revision 与同步信息`

Required metadata:

```markdown
## Review Source

- Feishu Document: <URL or Pending Publication>
- Feishu Revision: <revision or Pending>
- Synced At: <timestamp or Pending>
- Export Mode: cloud-media | offline-media
```

Required tables:

```markdown
| Source ID | Type | Title / Scope | Version | Open / Download | Original Locator |
| --- | --- | --- | --- | --- | --- |

| Prototype ID | Page / State | Preview / Block Link | Original Source | What It Proves | Related Flow / State |
| --- | --- | --- | --- | --- | --- |

| 状态域 | 数据/状态 | 所有者 | 初始值 | 变化事件 | 重置条件 | State ID |
| --- | --- | --- | --- | --- | --- | --- |

| 场景 | API ID | Method / Path | 触发时机 | 请求摘要 | 成功处理 | 失败处理 | Sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |

| Task ID | 任务 | 输入 | 交付物 | 依赖 | 验收标准 |
| --- | --- | --- | --- | --- | --- |

| Requirement / Source | Prototype | Clarification | User Flow | State | Sequence / API | Task |
| --- | --- | --- | --- | --- | --- | --- |
```

## Linked evidence ID contract

- Render every `PRD-xx`, `API-xx`, `PT-xx`, `UF-xx`, `SM-xx`, and `SQ-xx` reference in prose, lists, and table cells as an individual Markdown link.
- A user-uploaded or local `PRD-xx` / `API-xx` targets its exact Feishu file-card block. Its title and `查看/下载原文件` action use the same stable target; the visible file card provides preview/download.
- A cloud-native `PRD-xx` / `API-xx` may target its durable canonical source. Use a versioned Feishu attachment snapshot when the source is mutable or reviewer access is uncertain.
- `PT-xx` targets the exact Feishu image block, or its uniquely paired caption block when direct image linking is unavailable.
- `UF-xx`, `SM-xx`, and `SQ-xx` target their exact diagram block; use the canonical section-heading block only when Feishu cannot link the diagram block directly.
- Keep original local paths, repository locators, Figma URLs, and canonical PRD/API locators in their own fields; they do not replace a required Feishu attachment.
- Do not group several IDs inside one link, link to a generic document home when a precise block exists, or use expiring signed media URLs.
- Canonical destination headings and IDs drawn inside diagram/code blocks do not need to link to themselves.

Include a semantic responsibility tree such as:

```text
FeaturePage
├── SearchArea
├── ResultTable
├── EditDialog
└── ConfirmDialog
```

Required diagram composition:

````markdown
## 8. User Flow

### UF-01 <用户目标>

<用 2～5 句话说明入口、主路径、备选结果和可见终态。>

```mermaid
flowchart TD
  ...
```

- Evidence / Decisions: PRD-xx, PT-xx, CL-xx

## 9. 前端状态设计

### SM-01 <页面或组件>

<说明状态所有者、关键状态、失败/恢复和重置规则。>

```mermaid
stateDiagram-v2
  ...
```

- Related Flows / Evidence: UF-xx, PT-xx, CL-xx

## 11. API 与交互 Mapping

### SQ-01 <交互场景>

<说明触发条件、API、成功/失败后的 UI 结果。>

```mermaid
sequenceDiagram
  ...
```

- Related Flow / State / API: UF-xx, SM-xx, API-xx
````

Composition rules:

- Copy and reconcile the complete Mermaid body from the approved source artifact; do not abbreviate it into a list of IDs.
- Include one independently renderable visual per `UF-xx`, `SM-xx`, and `SQ-xx`. Do not combine several IDs into an unlabeled image.
- Keep a text summary and trace IDs beside each visual so the document remains understandable if image rendering is unavailable.
- Never use “详见/参考 `user-flow.md`”, `state-machine.md`, or `sequence-diagram.md` as a substitute for inline review content.
- The publisher converts these Mermaid blocks into Feishu image blocks while preserving headings, captions, summaries, and trace IDs.

The Plan must let an uninvolved reviewer answer why the feature exists, who uses it, what is in/out, what each source file contains, how to open or download the reviewed PRD/API version, what each prototype state shows, which APIs are used, which decisions are confirmed, and what must be implemented. Do not include source code, guessed behavior, chat-only facts, or unresolved decisions disguised as tasks.
