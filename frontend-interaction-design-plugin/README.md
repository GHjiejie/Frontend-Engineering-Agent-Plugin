# Frontend Interaction Design Plugin

将 Product PRD、持久化原型证据和后端 API 合同转换为可供产品、研发、测试和 Coding Agent 使用的前端设计包。

V5 的核心约束是：任何影响最终方案的信息都不得只存在于当前会话中。飞书文档是面向人类的主要 Review 载体，本地 Markdown 是指定飞书 Revision 的工程快照；飞书操作优先使用 `lark-cli`。

## 输入

- Product PRD、需求正文或可访问的需求链接。
- Figma/Axure 链接、会话中粘贴的原型图片或本地图片。
- API PRD、OpenAPI、Swagger 或等价后端合同。

## 输出

```text
<confirmed-frontend-project-root>/
└── docs/frontend-design/<feature-name>/<YYYY-MM-DD[-vN]>/
    ├── source-manifest.md
    ├── clarification.md
    ├── user-flow.md
    ├── state-machine.md
    ├── sequence-diagram.md
    ├── frontend-development-plan.md
    ├── sync-manifest.json
    └── assets/                 # 仅 offline-media 导出模式
        ├── sources/
        ├── prototype/
        └── diagrams/
```

同时生成或更新一份飞书 Review 文档，用于内嵌原型图片、User Flow、State Machine、Sequence Diagram，展示完整上下文并承载 Technical Review。`user-flow.md` 等本地文件是结构化生成源，不是 Reviewer 需要自行访问的替代文档。

## 七个 Skill

1. `source-evidence-manager`：确认项目与版本后，持久化 PRD、原型和 API 证据；本地来源文件上传为可下载的飞书文件卡片，会话图片和 Figma 截图上传为媒体证据。
2. `requirement-clarification`：比较 PRD、Prototype、API 和已确认决策，记录 `CL-xx`。
3. `user-flow-generator`：生成引用 `PT-xx` 和 `CL-xx` 的用户流程。
4. `state-machine-generator`：生成可见 UI 状态及转换模型。
5. `sequence-diagram-generator`：将用户动作、前端状态和 API 映射为时序。
6. `frontend-plan-generator`：编排全流程并生成具有完整 Review Context 的 Plan Draft。
7. `review-package-publisher`：发布飞书 Review 文档、固定 Revision、显式导出本地快照并运行 Reviewability Gate。

## 五道 Gate

1. 确认目标前端项目。
2. 确认 Feature 和版本目录。
3. 确认来源完整、原型已持久化且可访问。
4. 确认影响流程、状态、API 或实现的业务歧义。
5. 确认脱离当前会话后仍然可理解、可访问、可追踪且同步一致。

## 严格流水线

```text
Project Discovery
→ Gate #1
→ Feature / Version Resolution
→ Gate #2
→ Source Evidence Manager
→ Gate #3
→ Requirement Clarification
→ Gate #4
→ User Flow
→ State Machine
→ Sequence Diagram
→ Frontend Plan Draft
→ Feishu Publish
→ Revision-pinned Local Export
→ Gate #5
→ Technical Review
```

如果下游发现新的来源缺失或业务歧义，必须回到同一版本的 `source-manifest.md` 或 `clarification.md`，阻塞流水线后等待确认；不得创建新版本规避问题。

## 飞书与同步边界

- 会话图片必须上传飞书并获得稳定 `PT-xx`，不得用“聊天中的第几张图”引用。
- 用户上传或本地提供的 PRD、API 合同、权限矩阵等来源文件必须作为带标签的飞书文件卡片上传；`PRD-xx` / `API-xx`、标题和查看/下载操作都要链接到精确附件 Block，静态文件名不能通过 Source Gate。
- Figma 必须记录具体 Node/Frame URL 和截图时间，再将关键状态截图上传飞书。
- 每个 `UF-xx`、`SM-xx`、`SQ-xx` 必须渲染成带标题和 ID 的图片，插入飞书对应章节，并保留相邻文字摘要和追踪 ID；只写“参考本地 Markdown”不能通过 Reviewability Gate。
- 最终 Review 文档中出现的 `PT-xx`、`UF-xx`、`SM-xx`、`SQ-xx` 必须逐个链接到对应图片、流程图、状态图或时序图的精确 Block；不得只链接文档首页或使用临时媒体 URL。
- 飞书在线文档不能依赖普通 `drive sync`；最终使用 `lark-cli docs +fetch --api-version v2 --doc <doc> --doc-format markdown --revision-id <id>` 显式导出。
- `sync-manifest.json` 记录飞书 URL、Token、Revision、导出模式和同步状态。
- 本地已有人工修改时进入 `Sync Drift`，不得静默覆盖。

## 边界

Plugin 只分析、建模、发布和同步设计文档，不生成应用代码，不修改前端源码，不创建业务组件，不提交 Git Commit 或 PR，也不未经授权改变飞书文档权限。
