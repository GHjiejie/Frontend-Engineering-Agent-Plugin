# Frontend Development Plan Output Contract

Write `frontend-design/<feature-name>/frontend-development-plan.md` in this section order:

1. `# <功能名称>前端开发方案`
2. `## 1. 功能概述与澄清 Gate`
3. `## 2. 页面与组件设计`
4. `## 3. 状态设计`
5. `## 4. API 调用方案`
6. `## 5. 交互与异常处理`
7. `## 6. 开发任务拆分`
8. `## 7. 追踪矩阵`
9. `## 8. 已确认决策与约束`
10. `## 9. 前端 Review 清单`

Include a semantic page tree:

```text
FeaturePage
├── SearchArea
├── ResultTable
├── EditDialog
└── ConfirmDialog
```

Include these tables:

```markdown
| 状态域 | 数据/状态 | 所有者 | 初始值 | 变化事件 | 重置条件 | 关联 State ID |
| --- | --- | --- | --- | --- | --- | --- |

| 场景 | API ID | Method / Path | 触发时机 | 请求摘要 | 成功处理 | 失败处理 | 关联 Sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |

| Task ID | 任务 | 输入 | 交付物 | 依赖 | 验收标准 |
| --- | --- | --- | --- | --- | --- |

| 需求/来源 | Clarification | User Flow | State | Sequence / API | Task |
| --- | --- | --- | --- | --- | --- |
```

Development tasks may describe page structure, API adapters, list behavior, dialogs, validation, tests, integration, and review. They must not contain unresolved decisions, generated source code, or authorization for repository changes. If any required table cell depends on an unconfirmed choice, block the gate instead of completing the plan.
