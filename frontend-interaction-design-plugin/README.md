# Frontend Interaction Design Plugin

将产品 PRD、前端原型和后端 API 契约转换为可评审、可版本管理的前端交互设计文档。V3 在需求澄清之前增加“目标前端项目”和“Feature 版本目录”两个强制人工 Gate：AI 负责发现与推荐，开发者负责关键决策。

## 输入与输出

输入：

- 产品 PRD
- Figma、Axure、截图或文字形式的前端原型
- 后端 API PRD、OpenAPI 或等价接口契约

输出到已确认的版本目录：

```text
<confirmed-frontend-project-root>/
└── docs/frontend-design/<feature-name>/<YYYY-MM-DD[-vN]>/
```

目录内包含：

1. `clarification.md`
2. `user-flow.md`
3. `state-machine.md`
4. `sequence-diagram.md`
5. `frontend-development-plan.md`

## 三个人工 Gate

1. 只读扫描当前工作区，推荐目标前端项目；开发者确认后锁定 `frontend-project-root`。
2. 识别 Feature 与历史版本，推荐继续当前版本或创建 `YYYY-MM-DD[-vN]`；开发者确认后锁定输出目录。
3. 对 PRD、Prototype、API 做一致性检查；所有影响流程、状态、API 或实现的歧义均由开发者确认。

在 Gate #1 和 Gate #2 通过前，不得创建 `docs/frontend-design` 文件。后续 Skill 必须复用锁定的项目、Feature 和版本，不得重新推断。

## 严格流水线

`Project Discovery` → `Human Gate #1` → `Feature / Version Resolve` → `Human Gate #2` → `requirement-clarification` → `Human Gate #3` → `user-flow-generator` → `state-machine-generator` → `sequence-diagram-generator` → `frontend-plan-generator`

`clarification.md` 始终生成：

- 没有问题时为 `Cleared`。
- 存在未决问题时为 `Waiting Confirmation`，流水线立即暂停。
- 用户确认全部问题后更新为 `Resolved`，流水线才可继续。

后续三个技能负责交互建模，最后一个技能只汇总已确认的输入并形成开发方案。每个技能只写自己的 Markdown 产物；任何阶段发现新的歧义，都必须返回澄清 Skill 并重新阻塞流水线。

## 使用示例

- “先识别这个需求对应的前端项目和版本目录，确认后再检查 PRD、Figma 原型和 OpenAPI。”
- “澄清全部问题后，根据已确认决策生成用户流程。”
- “根据已确认的用户流程和原型补齐页面状态机。”
- “把用户流程、状态模型和 OpenAPI 映射成前后端时序图。”
- “用这些已确认的产物生成前端开发方案。”
- “从 PRD、原型和 API 开始，生成完整的前端交互设计包。”

## 边界

插件只分析和生成版本化设计文档，不生成应用代码，不修改前端源码，不创建业务组件，也不提交 Git Commit 或 PR。不得未经确认选择前端项目、创建新版本、覆盖历史独立版本，或把业务推测写成已确认事实。

当前 Codex 插件规范使用 `.codex-plugin/plugin.json`；它对应架构设计中的 `plugin.yaml` 角色。
