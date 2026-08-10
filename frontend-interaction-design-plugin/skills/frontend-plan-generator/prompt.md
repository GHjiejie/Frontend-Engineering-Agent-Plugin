# Frontend Development Plan Output Contract

Write `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/frontend-development-plan.md` in this section order:

1. `# <Feature> Frontend Development Plan`
2. `Status: Ready for Development | Blocked`
3. `## 已确认运行上下文`
4. `## 1. 功能背景与目标`
5. `## 2. 本次开发范围`
6. `## 3. 页面与交互实现`
7. `## 4. User Flow 摘要`
8. `## 5. 状态设计`
9. `## 6. API 使用方案`
10. `## 7. API 与交互 Mapping`
11. `## 8. 异常与边界状态`
12. `## 9. 关键开发决策`
13. `## 10. 开发任务拆分`
14. `## 11. 已确认事项`
15. `## 12. 未解决问题`
16. `## 追踪矩阵`
17. `## Technical Review 清单`

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
| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |

| 状态域 | 数据/状态 | 所有者 | 初始值 | 变化事件 | 重置条件 | 关联 State ID |
| --- | --- | --- | --- | --- | --- | --- |

| 场景 | API ID | Method / Path | 触发时机 | 请求摘要 | 成功处理 | 失败处理 | 关联 Sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |

| Task ID | 任务 | 输入 | 交付物 | 依赖 | 验收标准 |
| --- | --- | --- | --- | --- | --- |

| 需求/来源 | Clarification | User Flow | State | Sequence / API | Task |
| --- | --- | --- | --- | --- | --- |
```

Development tasks may describe page structure, API adapters, list behavior, dialogs, validation, tests, integration, and review. They must not contain generated source code or authorization for repository changes. If any blocking issue remains, set `Status: Blocked`; do not mark the package `Ready for Development`. Never write outside the confirmed version directory or overwrite another independent version.
