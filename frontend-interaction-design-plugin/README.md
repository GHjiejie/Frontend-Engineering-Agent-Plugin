# Frontend Interaction Design Plugin

将产品 PRD、前端原型和后端 API 契约转换为可评审、可版本管理的前端交互设计文档。V2 在所有建模之前增加需求澄清 Gate，禁止 AI 自行补全业务决策。

## 输入与输出

输入：

- 产品 PRD
- Figma、Axure、截图或文字形式的前端原型
- 后端 API PRD、OpenAPI 或等价接口契约

输出到 `frontend-design/<feature-name>/`：

1. `clarification.md`
2. `user-flow.md`
3. `state-machine.md`
4. `sequence-diagram.md`
5. `frontend-development-plan.md`

## 严格流水线

`requirement-clarification-generator` → `user-flow-generator` → `state-machine-generator` → `sequence-diagram-generator` → `frontend-plan-generator`

`clarification.md` 始终生成：

- 没有问题时为 `Cleared`。
- 存在未决问题时为 `Waiting Confirmation`，流水线立即暂停。
- 用户确认全部问题后更新为 `Resolved`，流水线才可继续。

后续三个技能负责交互建模，最后一个技能只汇总已确认的输入并形成开发方案。每个技能只写自己的 Markdown 产物；任何阶段发现新的歧义，都必须返回澄清 Skill 并重新阻塞流水线。

## 使用示例

- “先检查这个 PRD、Figma 原型和 OpenAPI 是否存在冲突。”
- “澄清全部问题后，根据已确认决策生成用户流程。”
- “根据已确认的用户流程和原型补齐页面状态机。”
- “把用户流程、状态模型和 OpenAPI 映射成前后端时序图。”
- “用这些已确认的产物生成前端开发方案。”
- “从 PRD、原型和 API 开始，生成完整的前端交互设计包。”

## 边界

插件只分析和生成设计文档，不生成应用代码，不修改代码仓库，不创建业务组件，也不提交 PR。信息缺失、冲突或存在多种合理解释时，必须生成澄清问题并暂停，不能把推测写成已确认事实。

当前 Codex 插件规范使用 `.codex-plugin/plugin.json`；它对应架构设计中的 `plugin.yaml` 角色。
