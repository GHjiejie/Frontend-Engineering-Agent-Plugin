# Frontend Interaction Design Plugin 架构设计方案（V5）

## 1. 文档目的

本文档定义 `frontend-interaction-design` Plugin 的最新架构。

该 Plugin 面向真实前端研发与技术评审流程，输入 Product PRD、前端原型和后端 API 合同，在开发者确认工程路径、需求版本和业务歧义后，生成可供产品经理、前端开发、后端开发、测试和 Coding Agent 使用的前端设计包。

最终设计包必须同时满足：

- Reviewer 不依赖原始会话即可理解功能背景、范围、原型、关键决策和开发方案。
- 原型图片不会只存在于聊天上下文中。
- 飞书文档提供适合人类阅读、评论和图片展示的 Review 入口。
- 本地 Markdown 提供可被 Git 版本管理和 Coding Agent 消费的工程快照。
- 所有方案结论均可回溯到 PRD、原型、API 或开发者确认的决策。

核心约束：

> 任何影响最终方案的信息，都不得只存在于当前会话上下文中。

---

## 2. Plugin 定位

### 2.1 Plugin 名称

```text
frontend-interaction-design
```

### 2.2 核心职责

```text
Product PRD
    +
Prototype
    +
Backend API Contract
    ↓
Project / Feature / Version Confirmation
    ↓
Source Evidence Collection
    ↓
Requirement Clarification
    ↓
Interaction Modeling
    ↓
Frontend Development Plan
    ↓
Feishu Review Package
    ↓
Local Engineering Snapshot
    ↓
Technical Review
```

Plugin 负责：

- 识别并确认目标前端项目。
- 识别并确认 Feature 与版本目录。
- 接收链接、文件和会话附件形式的输入资料。
- 将原型证据固化到飞书文档，默认优先使用 `lark-cli`。
- 检查 PRD、原型和 API 之间的缺失、歧义和冲突。
- 生成 User Flow、State Machine 和 Sequence Diagram。
- 生成包含完整 Review Context 的 Frontend Development Plan。
- 将最终方案发布为飞书 Review 文档。
- 将指定飞书 Revision 同步为本地版本化工程文档。
- 验证设计包是否脱离会话后仍然可理解、可访问和可追踪。

Plugin 不负责：

- 自动生成或修改业务代码。
- 自动修改产品需求或后端 API。
- 在存在关键歧义时替代开发者做业务决策。
- 自动提交 Git Commit、Push 或 Pull Request。
- 未经授权调整飞书文档权限或公开范围。
- 把临时会话链接、临时图片 URL 或未确认推测作为正式证据。

后续 Coding Agent 只能消费已通过 Reviewability Gate 的本地工程快照。

---

## 3. 核心设计原则

### 3.1 No Chat-only Context

任何影响 User Flow、状态、API 调用或开发任务的信息，都必须进入以下至少一种持久化载体：

- 飞书 Review 文档正文。
- `source-manifest.md`。
- `clarification.md`。
- 版本目录中的其他设计产物。

聊天记录只是输入渠道，不是设计事实源。

### 3.2 Evidence before Derivation

在生成流程图、状态机、时序图和 Plan 之前，必须先固化输入来源和原型证据。

### 3.3 Human Review First, Engineering Snapshot Second

- 飞书文档是设计与评审阶段面向人类的主 Review 载体。
- 本地 Markdown 是指定飞书 Revision 的工程快照。
- 不允许无冲突检查的双向覆盖。

### 3.4 Machine Discovers; Developer Decides

AI 可以发现问题、给出证据和推荐选项；涉及以下内容时必须由开发者确认：

- 目标前端项目。
- Feature 与版本目录。
- 相互冲突的 PRD、原型或 API 版本。
- 业务规则、权限、异常处理和交互取舍。
- 新增或改变后端 API。

### 3.5 Traceability Is Not Reviewability

`CL-xx → UF-xx → SM-xx → SQ-xx → FE-xx` 只能证明内部产物有关联，不能证明 Reviewer 理解原始上下文。

最终 Plan 还必须展示：

- 为什么做。
- 给谁使用。
- 本期做什么和不做什么。
- 原型页面长什么样。
- 依据了哪些 PRD、原型和 API 版本。
- 哪些行为来自开发者确认。

### 3.6 Stable References Only

正式设计包不得依赖：

- 只在当前会话中可见的附件引用。
- 临时签名图片 URL。
- 无具体 Node 的 Figma 文件首页。
- 无版本信息的 PRD 或 API 链接。
- 无法被 Reviewer 访问的飞书文档。

### 3.7 Same Iteration, Same Version

同一轮澄清、Review 修改、图表修正和文案修正继续更新当前版本，由飞书 Revision 和 Git 记录细粒度历史；只有独立需求迭代才创建新版本。

### 3.8 Review Surface Must Be Self-contained

飞书 Plan 是 Reviewer 的完整评审面，不是本地文件目录的索引。

- `user-flow.md`、`state-machine.md`、`sequence-diagram.md` 是结构化生成源和 Coding Agent 输入。
- 每个 `UF-xx`、`SM-xx`、`SQ-xx` 的实际图、标题、语义摘要和追踪 ID 必须进入飞书对应章节。
- “详见/参考 `user-flow.md`”等路径只能作为工程元数据，不能替代正文内容。
- Reviewer 无需访问开发者工作区，也能看到主要流程、状态转换和前后端时序。
- 即使图片暂时无法预览，相邻文字摘要也必须足以解释入口、分支、终态、恢复和 API 结果。

---

## 4. 事实源与交付载体

### 4.1 事实优先级

当资料之间发生冲突时，优先级为：

```text
Developer Confirmed Decision
            ↓
Confirmed Source Version / Snapshot
            ↓
Unversioned or Mutable Source
            ↓
Model Inference（不得作为正式决策）
```

不得简单规定 PRD、Prototype 或 API 永远优先，因为任意一方都可能不是最新版。

### 4.2 各载体职责

| 载体 | 职责 | 是否主编辑面 | 是否允许包含图片 |
| --- | --- | --- | --- |
| Product PRD / API / Figma | 上游原始资料 | 否 | 是 |
| 飞书 Review 文档 | 人类阅读、原型与三类交互图展示、评论与技术评审 | 是 | 是，必须内嵌评审所需视觉内容 |
| 本地版本目录 | 结构化生成源、Git 留档、自动校验、Coding Agent 输入 | 否 | 默认引用飞书，可选离线图片 |
| 当前会话 | 输入和澄清渠道 | 否 | 可接收，但不得成为唯一存储 |

### 4.3 编辑与同步规则

设计与 Review 阶段采用单向同步：

```text
Feishu Review Document
        ↓ explicit export
Local Engineering Snapshot
```

规则如下：

- 飞书文档是当前设计 Revision 的主编辑面。
- `user-flow.md`、`state-machine.md`、`sequence-diagram.md` 等结构化产物可以在发布前作为本地 Draft 生成；它们是飞书 Plan 的输入，不是与飞书并行维护的第二份 Review 文档。
- Plan 组装阶段必须把三个结构化产物的完整图表载荷合并进 Plan；发布阶段再把 Mermaid 载荷渲染为飞书图片 Block。不得要求 Reviewer 打开本地文件补全上下文。
- 本地快照必须记录飞书文档 Token、Revision ID 和同步时间。
- 首次发布完成后，`frontend-development-plan.md` 必须由确认的飞书 Revision 导出；其他结构化产物必须通过追踪 ID 与该 Revision 保持一致。
- 下一次导出前发现本地文件发生人工修改时，必须先做差异检查。
- 不得静默用飞书覆盖本地人工修改。
- 不得静默用本地文件反向覆盖飞书。
- Review 结论优先回写飞书和 `clarification.md`，再重新导出。

---

## 5. 输入契约

### 5.1 必需输入

1. Product PRD。
2. Prototype。
3. Backend API Contract、API PRD、OpenAPI 或等价资料。

缺少会影响当前功能的任一来源时，必须进入 Source Completeness Gate，不得直接生成 Ready for Development 的 Plan。

### 5.2 支持的来源形式

PRD 和 API 可以是：

- 飞书文档链接。
- 本地 Markdown、Word、PDF、OpenAPI 或其他文件。
- 可访问的内部平台链接。
- 用户粘贴的正文。

Prototype 可以是：

- Figma File、Page、Frame 或 Node 链接。
- Axure 或其他可访问的原型平台链接。
- 用户直接粘贴到会话中的原型图片。
- 本地截图或图片文件。
- PDF 页面或其他可稳定截图的视觉资料。

### 5.3 Source Manifest 字段

每个输入来源必须分配稳定 ID，并记录：

| 字段 | 说明 |
| --- | --- |
| Source ID | `PRD-01`、`PT-01`、`API-01` 等稳定标识 |
| Type | PRD、Prototype、API、Developer Decision |
| Title | 来源标题或页面名称 |
| Locator | URL、文件路径、飞书 Block 链接或附件标识 |
| Version | 文档版本、Figma Node、API 版本或 Revision |
| Captured At | 读取或截图时间及时区 |
| Scope | 本次功能实际使用的范围 |
| Access Status | Verified、Restricted、Unavailable |
| Evidence Location | 飞书文档中的章节或图片 Block |
| Notes | 已知限制、缺失状态或补充说明 |

---

## 6. 原型证据采集协议

### 6.1 会话中直接粘贴原型图片

标准流程：

```text
Chat Image Attachment
    ↓
读取图片并识别页面/状态
    ↓
分配 PT-xx
    ↓
使用 lark-cli 插入飞书文档
    ↓
记录图片 Block、Caption、来源与范围
    ↓
进入需求一致性检查
```

要求：

- 默认优先使用 `lark-cli docs +media-insert` 将图片插入飞书文档。
- 图片来自系统剪贴板时优先走剪贴板上传；图片已有本地路径时使用本地文件上传。
- 每张图必须有唯一 `PT-xx`、页面名称、状态名称和说明。
- 不得把“聊天中的第几张图”作为正式引用。
- 图片无法表达跳转条件、按钮结果或异步反馈时，必须提出澄清问题。
- 如果附件无法读取或上传失败，应要求用户重新提供，不得猜测本地文件路径。

示例：

| Prototype ID | 页面/状态 | 飞书证据 | 说明 |
| --- | --- | --- | --- |
| `PT-01` | 客户列表默认状态 | 飞书图片 Block 链接 | 展示搜索区、表格和新建入口 |
| `PT-02` | 新建客户弹窗 | 飞书图片 Block 链接 | 展示字段、提交与取消按钮 |
| `PT-03` | 提交失败状态 | 飞书图片 Block 链接 | 展示失败反馈和表单保留状态 |

### 6.2 Figma 链接

标准流程：

```text
Figma URL
    ↓
解析 File / Page / Frame / Node
    ↓
确认本次需求涉及的节点范围
    ↓
截取相关页面和关键状态
    ↓
分配 PT-xx
    ↓
使用 lark-cli 上传飞书文档
    ↓
记录原链接、Node ID、Captured At
```

要求：

- 优先使用具体 Frame 或 Node 链接，而不是只记录 Figma 文件首页。
- 截图必须覆盖当前需求涉及的关键页面和状态，而不是无选择地截取整个文件。
- 每个截图同时保留原始 Figma URL 和 Node ID。
- 截图必须记录抓取时间，避免 Figma 后续修改导致证据漂移。
- Figma 无权访问、链接失效或节点范围不明确时，Source Completeness Gate 必须阻塞。
- 静态截图未表达的交互不得从视觉样式中自行推断。

### 6.3 其他原型链接

对于 Axure 或其他平台，沿用 Figma 的证据要求：

- 保留原始链接和可识别页面定位。
- 记录访问时间和范围。
- 截取关键页面与状态。
- 上传飞书并分配 `PT-xx`。
- 无法稳定访问时要求用户提供截图或导出文件。

### 6.4 图片存储策略

默认策略：

- 原型图片正式存储在飞书文档中。
- 本地 Markdown 引用飞书文档和稳定 Block，而不是临时图片下载 URL。
- 本地 Plan 必须保留页面名称、状态说明和 `PT-xx`，即使当前环境暂时无法渲染图片，仍可理解其语义。

可选离线模式：

- 当用户要求离线 Review、跨租户交付或仓库内直接渲染图片时，使用 `lark-cli` 下载媒体到 `assets/prototype/`。
- 离线图片是指定飞书 Revision 的导出副本，不是新的主编辑源。

---

## 7. 总体架构

```text
                              Plugin Start
                                   │
                                   ▼
                        Frontend Project Discovery
                                   │
                                   ▼
                            Human Gate #1
                           确认前端项目路径
                                   │
                                   ▼
                      Feature / Version Resolution
                                   │
                                   ▼
                            Human Gate #2
                         确认 Feature 与版本
                                   │
                                   ▼
                       Source Evidence Manager
                     ┌─────────────┴─────────────┐
                     │                           │
              Chat / Local Image            Figma / URL
                     │                           │
                     └─────────────┬─────────────┘
                                   ▼
                     Feishu Evidence Document
                       （优先使用 lark-cli）
                                   │
                                   ▼
                      Source Completeness Gate #3
                                   │
                                   ▼
                    Requirement Clarification
                                   │
                                   ▼
                            Human Gate #4
                            业务歧义确认
                                   │
                                   ▼
                         User Flow Generator
                                   │
                                   ▼
                       State Machine Generator
                                   │
                                   ▼
                      Sequence Diagram Generator
                                   │
                                   ▼
                        Frontend Plan Generator
                   （合并完整图、摘要与追踪 ID）
                                   │
                                   ▼
                       Review Package Publisher
                  （渲染图表并插入飞书媒体 Block）
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
             Feishu Review Doc          Local Engineering Snapshot
                    └──────────────┬──────────────┘
                                   ▼
                         Reviewability Gate #5
                                   │
                                   ▼
                           Technical Review
                                   │
                                   ▼
                              Coding Agent
```

---

## 8. Plugin 目录结构

Plugin 由编排层和七个核心 Skill 组成：

```text
frontend-interaction-design/
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   ├── source-evidence-manager/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── source-manifest-contract.md
│   │       ├── prototype-evidence-contract.md
│   │       └── lark-publishing-workflow.md
│   ├── requirement-clarification/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── user-flow-generator/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── state-machine-generator/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── sequence-diagram-generator/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── frontend-plan-generator/
│   │   ├── SKILL.md
│   │   └── references/
│   └── review-package-publisher/
│       ├── SKILL.md
│       └── references/
│           ├── feishu-review-document-contract.md
│           ├── local-export-contract.md
│           └── reviewability-checklist.md
└── scripts/
    ├── validate-design-package.*
    └── verify-sync-manifest.*
```

说明：

- Frontend Project Discovery、Feature Resolution、Version Resolution 和 Gate 控制属于 Plugin 编排逻辑，不单独拆成 Skill。
- Figma 或其他视觉工具负责读取和截图，`source-evidence-manager` 负责证据编号、上传和归档。
- `lark-cli` 是默认飞书操作入口；只有它无法覆盖目标操作时，才允许使用其他飞书接口，并记录原因。
- `scripts/` 只承担确定性的结构校验和同步一致性检查，不承担业务判断。

---

## 9. 项目、Feature 与版本模型

### 9.1 Frontend Project Discovery

创建任何本地版本文件或飞书设计文档前，先只读检查：

- 当前 Working Directory。
- `package.json`。
- `src/`、路由和框架配置。
- 前端依赖与构建配置。
- PRD 和原型中的系统名称。
- 工作区中的多个候选前端项目。

Plugin 可以推荐最可能的项目，但必须由开发者确认。

### 9.2 Human Gate #1：项目确认

展示：

- 推荐项目名称。
- 绝对路径。
- 判断证据。
- 置信度和其他候选项。

开发者确认后锁定 `{frontend-project-root}`，所有后续 Skill 必须复用，不得重新推断。

### 9.3 Feature 目录

按业务功能组织，不按文档类型组织：

```text
docs/frontend-design/customer-management/
docs/frontend-design/order-management/
docs/frontend-design/role-permission-management/
```

### 9.4 Version 目录

```text
YYYY-MM-DD
YYYY-MM-DD-v2
YYYY-MM-DD-v3
```

创建新版本：

- 产品发布独立 PRD 迭代。
- 原型出现影响行为的明显变化。
- API 合同发生影响当前功能的重大变化。
- 已完成方案进入下一轮独立需求。
- 用户明确要求创建新版本。

继续当前版本：

- 回答 clarification 问题。
- 当前方案 Review 修改。
- 图表和文字修正。
- 同一轮原型截图补充。
- 飞书文档 Revision 更新和重新同步。

### 9.5 Human Gate #2：Feature 与版本确认

在创建飞书 Review 文档或本地版本目录之前，展示：

- Feature。
- 继续现有版本或创建新版本的建议。
- 精确本地输出目录。
- 计划创建的飞书文档标题。

必须等待开发者确认。

---

## 10. Skill 1：Source Evidence Manager

### 10.1 职责

- 接收 PRD、Prototype 和 API 来源。
- 创建或定位当前 Feature/Version 的飞书 Review 文档。
- 对会话图片、Figma 截图和其他原型证据分配 `PT-xx`。
- 优先使用 `lark-cli` 上传图片和维护飞书文档。
- 生成或更新 `source-manifest.md`。
- 验证来源可访问性、版本和范围。
- 阻止聊天附件成为唯一证据。

### 10.2 输出

```text
source-manifest.md
Feishu Review Document URL / Token
Prototype Evidence IDs
Source Completeness Gate Result
```

### 10.3 Gate #3：Source Completeness

只有满足以下条件才能进入 Requirement Clarification：

- PRD 范围可读取或已被准确持久化摘要。
- 原型关键页面和状态已进入飞书文档。
- API 合同版本可定位。
- 每个来源都具有 Source ID、Locator、Version 和 Scope。
- Reviewer 对主要来源具有访问能力，或 Plan 中已包含足够的证据摘要。
- 不存在只在聊天上下文中的关键图片或规则。

不满足时状态为：

```text
Source Gate: BLOCKED
```

---

## 11. Skill 2：Requirement Clarification

### 11.1 职责

对以下关系进行一致性检查：

- PRD ↔ Prototype。
- PRD ↔ API。
- Prototype ↔ API。
- Source Evidence ↔ 已确认历史决策。

识别：

- 业务规则缺失。
- 原型未覆盖的状态。
- UI 与 API 能力不匹配。
- 权限、校验、确认、取消和重试行为缺失。
- 分页、并发、数据刷新和数据保留行为缺失。
- 来源版本冲突。

### 11.2 输出

```text
clarification.md
```

每个问题使用稳定 `CL-xx`，记录：

- 冲突或缺失证据。
- 影响的 `PRD-xx`、`PT-xx` 或 `API-xx`。
- 对前端流程、状态或调用的影响。
- 聚焦问题。
- Developer Decision。
- Final Decision。
- 状态与影响范围。

### 11.3 Human Gate #4：业务歧义确认

存在任何会改变用户流程、状态、API 调用或实现任务的歧义时：

```text
Clarification Gate: BLOCKED
```

只有全部阻塞问题解决后才允许继续。

---

## 12. Skill 3：User Flow Generator

输入：

- `source-manifest.md`。
- PRD 和 Prototype Evidence。
- `clarification.md`。

输出：

```text
user-flow.md
```

职责：

- 描述用户如何完成当前 Feature 的目标。
- 使用 `UF-xx` 标识主流程和已确认分支。
- 每个重要页面节点引用 `PT-xx`。
- 每个已澄清分支引用 `CL-xx`。
- 不根据静态截图自行制造交互。

---

## 13. Skill 4：State Machine Generator

输入：

- `user-flow.md`。
- Prototype Evidence。
- `clarification.md`。

输出：

```text
state-machine.md
```

职责：

- 描述页面和组件状态变化。
- 使用 `SM-xx` 标识状态模型。
- 覆盖实际涉及的 loading、empty、data、error、submitting、success、failed、disabled、dialog open/close 等状态。
- 关联 `UF-xx`、`PT-xx` 和 `CL-xx`。
- 不为了形式完整而制造没有证据的业务状态。

---

## 14. Skill 5：Sequence Diagram Generator

输入：

- `user-flow.md`。
- `state-machine.md`。
- API Contract。
- `clarification.md`。

输出：

```text
sequence-diagram.md
```

职责：

- 描述用户行为、前端状态和后端 API 的时间关系。
- 使用 `SQ-xx` 和 `API-xx`。
- 明确请求、响应、失败、取消、刷新和 UI 状态变化。
- API 文档未暴露数据库或内部服务时，不得虚构内部调用。

---

## 15. Skill 6：Frontend Plan Generator

### 15.1 输入

- `source-manifest.md`。
- Product PRD。
- Prototype Evidence。
- Backend API Contract。
- `clarification.md`。
- `user-flow.md`。
- `state-machine.md`。
- `sequence-diagram.md`。

### 15.2 输出

生成飞书 Review 文档中的 Plan 正文，并形成可导出的：

```text
frontend-development-plan.md
```

### 15.3 Plan 固定结构

```text
1. Review 导读
2. 功能背景与问题
3. 目标用户与使用场景
4. 输入资料与版本
5. 原型页面与状态总览
6. 本次开发范围与非目标
7. 页面与组件职责
8. User Flow（逐个内嵌 UF 图、摘要和证据）
9. 前端状态设计（逐个内嵌 SM 图、状态语义和证据）
10. API 使用方案
11. API 与交互 Mapping（逐个内嵌 SQ 图和 UF/SM/API 映射）
12. 异常与边界状态
13. 关键开发决策
14. 开发任务拆分
15. 验收标准
16. 已确认事项
17. 未解决问题
18. 追踪矩阵
19. Technical Review 清单
20. 文档 Revision 与同步信息
```

### 15.4 最低自解释要求

Reviewer 只阅读 Plan 时，必须能够回答：

- 这个功能为什么要做？
- 谁会使用？
- 本期做什么、不做什么？
- 主要页面和交互是什么？
- 原型证据在哪里？
- 调用了哪些 API？
- 有哪些关键决策和边界？
- 开发要完成哪些任务？
- 还有什么未解决问题？

Plan 不需要复制整份 PRD，但不得只写 ID 和结论。

以下写法不满足自解释要求：

```text
User Flow：详见 user-flow.md
State Machine：参考 state-machine.md
Sequence Diagram：见 sequence-diagram.md
```

### 15.5 Prototype Catalog

Plan 中必须包含原型目录：

| Prototype ID | 页面/状态 | 预览 | 原始来源 | 说明 | 相关 Flow/State |
| --- | --- | --- | --- | --- | --- |

飞书文档中的“预览”直接内嵌图片；本地快照使用飞书 Block 链接或可选离线图片路径。

### 15.6 Diagram Composition Contract

Plan Draft 将本地结构化文件作为输入，但必须复制并校准完整内容，而不是仅生成引用：

| Plan 章节 | 来源 | 每个 ID 的必需内容 | 飞书表现 |
| --- | --- | --- | --- |
| User Flow | `user-flow.md` | `UF-xx` 标题、流程摘要、完整 Mermaid、`PRD/PT/CL` | 带 Caption 的内嵌流程图 |
| 前端状态设计 | `state-machine.md` | `SM-xx` 标题、所有者/重置摘要、完整 Mermaid、`UF/PT/CL` | 带 Caption 的内嵌状态图 |
| API 与交互 Mapping | `sequence-diagram.md` | `SQ-xx` 标题、触发与 UI 结果摘要、完整 Mermaid、`UF/SM/API` | 带 Caption 的内嵌时序图 |

每个 ID 必须对应一个可独立渲染、可独立替换的视觉单元。不得把多个 ID 合并为一张没有边界和 Caption 的大图。

---

## 16. Skill 7：Review Package Publisher

### 16.1 职责

- 将所有分析产物组织成完整飞书 Review 文档。
- 将 Plan Draft 中每个 `UF-xx`、`SM-xx`、`SQ-xx` 的 Mermaid 载荷渲染为 PNG 或 SVG，并插入飞书对应章节。
- 优先使用 `lark-cli` 创建、更新、读取和插入媒体。
- 将指定飞书 Revision 显式导出到本地版本目录。
- 生成同步元数据。
- 运行 Reviewability Gate。
- 检测飞书 Revision 与本地快照漂移。

### 16.2 为什么不能使用普通 Drive Sync

飞书在线文档不是普通 Drive 文件。普通目录级 `drive sync` 会跳过在线文档，因此必须采用显式导出：

```text
lark-cli docs +fetch --api-version v2 --doc <doc> \
  --doc-format markdown --revision-id <revision-id>
    ↓
读取目标 Revision
    ↓
转换文档内容和媒体引用
    ↓
写入本地 Markdown
    ↓
生成 sync-manifest.json
```

### 16.3 飞书发布规则

- 飞书操作优先使用 `lark-cli`。
- 使用 `lark-cli` 前读取与当前安装版本匹配的 `lark-doc`、`lark-drive` 或 `lark-markdown` 指引。
- 文档写入默认使用用户身份，遵守现有权限。
- 未经用户授权不得扩大公开范围或添加外部协作者。
- 所有原型图片必须具有 Caption 和 `PT-xx`。
- 所有交互图必须具有 Caption 和对应的 `UF-xx`、`SM-xx` 或 `SQ-xx`。
- 飞书评审面必须使用图片/媒体 Block 展示图表，不得假设 Mermaid fenced code 会被飞书自动渲染。
- 图表下方必须保留语义摘要和追踪 ID；媒体加载失败时 Reviewer 仍能理解主要行为。
- 关键章节必须能够被稳定定位，必要时保存 Block ID。

图表发布采用以下单向组合链路：

```text
user-flow.md / state-machine.md / sequence-diagram.md
                        ↓
       frontend-development-plan.md Draft
       （完整 Mermaid + 摘要 + Trace IDs）
                        ↓
           本地 Mermaid Renderer
                        ↓
        lark-cli 上传并插入媒体 Block
                        ↓
       Fetch 验证每个 ID 的媒体存在
                        ↓
          固定 Revision 并显式导出
```

如果当前环境没有可用的 Mermaid 渲染路径，Publisher 必须将发布状态设为 `Blocked` 并报告缺失能力；不得降级为只引用本地 Markdown 的“可发布”文档。

### 16.4 本地导出规则

- 导出固定 Revision，不得在导出过程中混用多个 Revision。
- 输出必须记录文档 URL、Token、Revision ID 和同步时间。
- 不得把临时图片 URL 当作长期引用。
- 默认保留飞书图片 Block 链接和语义说明。
- 离线模式下将原型图片下载到 `assets/prototype/`、交互图下载到 `assets/diagrams/`，并改写为本地相对路径。
- 本地文件已被人工修改时，先生成差异并暂停覆盖。
- 导出完成后运行结构、ID 和追踪矩阵校验。

### 16.5 同步元数据

`sync-manifest.json` 至少包含：

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

`exportMode`：

- `cloud-media`：图片保存在飞书，本地文档引用飞书证据。
- `offline-media`：原型图片导出到本地 `assets/prototype/`，交互图导出到 `assets/diagrams/`。

---

## 17. 飞书 Review 文档设计

### 17.1 文档命名

```text
[Frontend Design] {Feature Display Name} / {Version}
```

### 17.2 文档结构

```text
文档状态与 Review 导读
├── Feature / Version / Owner
├── Ready 状态
├── 本次变更摘要
└── Review 角色指引

上下文与来源
├── 功能背景
├── 目标用户
├── PRD 来源
├── Prototype Catalog
└── API 来源

需求澄清与关键决策
├── 冲突摘要
├── Developer Decisions
└── 未解决问题

交互与实现方案
├── User Flow（UF-xx 标题 + 内嵌图 + 摘要 + Trace）
├── State Machine（SM-xx 标题 + 内嵌图 + 摘要 + Trace）
├── Sequence Diagram（SQ-xx 标题 + 内嵌图 + 摘要 + Trace）
├── 页面与组件职责
├── API Mapping
└── 开发任务

Review 与同步
├── Technical Review Checklist
├── Review Notes
├── Revision ID
└── Local Snapshot Path
```

### 17.3 角色关注点

| 角色 | 主要关注内容 |
| --- | --- |
| 产品经理 | 背景、目标、原型、User Flow、范围、澄清决策 |
| 前端开发 | 页面职责、State Machine、API Mapping、任务拆分 |
| 后端开发 | Sequence Diagram、API Contract Gap、错误语义 |
| 测试 | 验收标准、状态覆盖、异常和边界行为 |
| Reviewer | 完整 Plan、证据、追踪矩阵和未解决问题 |
| Coding Agent | 本地同步快照和稳定 ID |

---

## 18. Reviewability Gate #5

### 18.1 Gate 目标

验证一个没有参与当前会话的开发者或产品经理，只通过飞书 Plan 和同步文件即可理解、评审并继续工作。

### 18.2 必须通过的检查

#### 上下文完整性

- [ ] 功能背景、目标用户和业务问题明确。
- [ ] 本期范围和非目标明确。
- [ ] 关键术语和业务规则可理解。
- [ ] 不存在只保留在会话中的关键事实。

#### 来源与原型

- [ ] PRD、Prototype、API 都具有稳定 Source ID。
- [ ] Figma 证据记录了具体 Node 和截图时间。
- [ ] 会话图片已经上传飞书并分配 `PT-xx`。
- [ ] 原型图片具有页面/状态说明。
- [ ] Reviewer 能访问飞书文档，或文档已包含足够的替代摘要。

#### 方案一致性

- [ ] 每个主要用户目标都具有 `UF-xx`。
- [ ] 每个 `UF-xx` 都在飞书 Plan 中具有带 ID/Caption 的内嵌流程图和文字摘要。
- [ ] 每个异步交互都具有状态模型。
- [ ] 每个 `SM-xx` 都在飞书 Plan 中具有带 ID/Caption 的内嵌状态图和所有者/重置说明。
- [ ] 每个 API 调用都进入 Sequence 和 Mapping。
- [ ] 每个 `SQ-xx` 都在飞书 Plan 中具有带 ID/Caption 的内嵌时序图和 `UF/SM/API` 映射。
- [ ] 每个失败分支都有可见处理。
- [ ] 每个开发任务都有可测试验收条件。
- [ ] 所有 Developer Decision 均进入下游产物。

#### 同步一致性

- [ ] 本地文件记录飞书文档 URL 和 Revision。
- [ ] 本地快照来自单一飞书 Revision。
- [ ] `sync-manifest.json` 状态为 `in-sync`。
- [ ] 不存在未处理的本地人工修改冲突。
- [ ] 图片引用不是临时下载 URL。
- [ ] 固定 Revision 的 Fetch 结果中，每个预期 `UF-xx`、`SM-xx`、`SQ-xx` 都仍有对应媒体引用；不存在仅引用本地文件的空壳章节。

### 18.3 状态

```text
Draft
Waiting Source
Waiting Clarification
Ready for Technical Review
Review Changes Requested
Ready for Development
Sync Drift
Blocked
```

只有以下条件同时满足，才能标记 `Ready for Development`：

- Source Completeness Gate 通过。
- Clarification Gate 通过。
- Reviewability Gate 通过。
- Technical Review 已确认。
- 本地快照与确认的飞书 Revision 一致。

---

## 19. 最终本地输出结构

```text
{confirmed-frontend-project-root}/
└── docs/
    └── frontend-design/
        └── {feature-name}/
            └── {YYYY-MM-DD[-vN]}/
                ├── source-manifest.md
                ├── clarification.md
                ├── user-flow.md
                ├── state-machine.md
                ├── sequence-diagram.md
                ├── frontend-development-plan.md
                ├── sync-manifest.json
                └── assets/
                    ├── prototype/
                    │   └── ... 仅 offline-media 模式生成
                    └── diagrams/
                        └── UF-xx / SM-xx / SQ-xx ... 仅 offline-media 模式生成
```

### 19.1 `frontend-development-plan.md` 顶部必须包含

```markdown
Status: Ready for Development | Blocked | Sync Drift

## Review Source

- Feishu Document: <URL>
- Feishu Revision: <revision-id>
- Synced At: <timestamp>
- Export Mode: cloud-media | offline-media
```

### 19.2 `source-manifest.md` 最低内容

- 已确认项目、Feature、Version 和输出目录。
- PRD、Prototype、API 来源表。
- Prototype Catalog。
- 访问状态和证据位置。
- Source Completeness Gate 结果。

---

## 20. Plugin 运行状态机

```text
INIT
  ↓
DISCOVERING_PROJECT
  ↓
WAITING_PROJECT_CONFIRMATION
  ↓
RESOLVING_FEATURE_VERSION
  ↓
WAITING_VERSION_CONFIRMATION
  ↓
COLLECTING_SOURCE_EVIDENCE
  ├── source incomplete ──→ WAITING_SOURCE
  └── source complete
  ↓
ANALYZING_REQUIREMENTS
  ├── ambiguity ─────────→ WAITING_CLARIFICATION
  └── clear
  ↓
GENERATING_USER_FLOW
  ↓
GENERATING_STATE_MACHINE
  ↓
GENERATING_SEQUENCE_DIAGRAM
  ↓
GENERATING_FRONTEND_PLAN
  ↓
PUBLISHING_FEISHU_REVIEW_DOC
  ↓
EXPORTING_LOCAL_SNAPSHOT
  ├── drift/conflict ────→ SYNC_DRIFT
  └── synchronized
  ↓
VALIDATING_REVIEWABILITY
  ├── failed ────────────→ BLOCKED
  └── passed
  ↓
READY_FOR_TECHNICAL_REVIEW
  ├── changes requested ─→ ANALYZING_REQUIREMENTS
  └── approved
  ↓
READY_FOR_DEVELOPMENT
```

---

## 21. Review 修改闭环

Review 修改继续使用同一 Feature/Version：

```text
Feishu Review Comment
    ↓
判断是文字修正、证据补充还是业务决策变化
    ├── 文字修正 → 更新飞书 Plan
    ├── 证据补充 → Source Evidence Manager
    └── 业务变化 → Requirement Clarification
                       ↓
                  重新生成受影响产物
    ↓
更新飞书 Revision
    ↓
重新导出本地快照
    ↓
重新运行 Reviewability Gate
```

不得因为一次 Review 修改自动创建新版本目录。

---

## 22. 异常与降级策略

### 22.1 lark-cli 不可用

- 明确报告飞书发布能力不可用。
- 不得假装图片已经持久化。
- 可以生成本地 Draft，但状态必须为 `Waiting Source` 或 `Blocked`。
- 用户明确允许时，可以使用其他飞书接口作为降级路径，并记录原因。

### 22.2 飞书认证或权限失败

- 停止重复写入。
- 保留本地临时分析结果，不标记 Ready。
- 要求用户完成认证、授权或提供可写文档。
- 不得自动扩大文档公开权限。

### 22.3 Figma 无法访问

- 记录原链接和访问错误。
- 请求用户提供访问权限、具体 Node 链接或截图。
- 在关键页面证据缺失时阻塞 Source Gate。

### 22.4 飞书图片在本地无法渲染

- 本地 Plan 仍保留 `PT-xx`、页面名称、状态和飞书 Block 链接。
- 如 Reviewer 需要脱离飞书查看，切换为 `offline-media` 导出。
- 不使用临时签名 URL 作为长期修复。

### 22.5 同步时发现本地修改

- 生成飞书 Revision 与本地文件差异。
- 状态标记为 `Sync Drift`。
- 等待开发者决定保留本地修改、回写飞书或丢弃本地修改。
- 未确认前不得覆盖。

---

## 23. 全局禁止规则

所有 Skill 必须遵守：

- 不得猜测未定义的业务规则。
- 不得在 PRD、Prototype、API 冲突时自行选择其中一个。
- 不得自行决定新增或修改后端 API。
- 不得自行改变原型交互。
- 不得未经确认选择目标前端项目和版本目录。
- 不得在项目与版本确认前创建正式飞书文档或本地版本产物。
- 不得将会话附件作为唯一原型证据。
- 不得用 Figma 文件首页代替具体页面证据。
- 不得使用临时图片 URL 作为长期文档引用。
- 不得在关键来源缺失或业务歧义未解决时标记 Ready。
- 不得在飞书与本地内容发生冲突时静默覆盖。
- 不得未经授权改变飞书权限或公开范围。
- 不得为了让图完整而虚构服务、数据库、状态或交互。
- 不得覆盖历史独立版本。
- 不得把“内部 ID 可追踪”误当成“Reviewer 可以理解”。

---

## 24. 与 Coding Agent 的关系

```text
PRD + Prototype + API
          ↓
Source Evidence Package
          ↓
Clarification + Three Models
          ↓
Feishu Frontend Development Plan
          ↓
Technical Review
          ↓
Confirmed Feishu Revision
          ↓
Local Engineering Snapshot
          ↓
Coding Agent
          ↓
Frontend Source Code
```

Coding Agent 使用：

- `frontend-development-plan.md` 理解方案和任务。
- `source-manifest.md` 定位原始证据。
- `clarification.md` 获取最高优先级业务决策。
- 三个图理解流程、状态和 API 时序。
- `sync-manifest.json` 验证本地快照对应的飞书 Revision。

如果状态为 `Blocked`、`Waiting Clarification` 或 `Sync Drift`，Coding Agent 不得开始实现。

---

## 25. V5 核心设计结论

V5 最终确定以下原则：

1. 项目路径不能猜着写。
2. 业务需求不能猜着做。
3. 功能版本不能直接覆盖。
4. AI 可以推荐，但关键决策必须由开发者确认。
5. 任何方案依据不得只存在于会话上下文中。
6. 会话图片和 Figma 截图必须固化为稳定的原型证据。
7. 飞书是面向人类的主要 Review 载体，且优先使用 `lark-cli`。
8. 本地 Markdown 是指定飞书 Revision 的工程快照。
9. 飞书在线文档必须显式导出，不能依赖普通 Drive 目录同步。
10. 最终 Plan 必须让未参与当前会话的开发者或产品经理理解背景、范围、原型、决策和实施方案。

最终目标不是“生成一份格式完整的 Plan”，而是：

> 生成一个脱离当前会话后仍然可理解、可访问、可评审、可追踪并可交给 Coding Agent 执行的 Frontend Design Package。
