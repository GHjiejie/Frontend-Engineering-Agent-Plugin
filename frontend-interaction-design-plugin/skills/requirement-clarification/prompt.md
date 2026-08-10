# Requirement Clarification Output Contract

After project and version confirmation, write `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/clarification.md` in this exact section order:

1. `# <功能名称>需求澄清`
2. `Status: Cleared | Waiting Confirmation | Resolved`
3. `Gate: PASS | BLOCKED`
4. `## 已确认运行上下文`
5. `## 输入与版本`
6. `## 一致性检查摘要`
7. `## 澄清问题`
8. `## 已确认决策`
9. `## Gate 结果与下游交接`

Use these tables:

```markdown
| 项目 | 已确认值 | 确认依据 |
| --- | --- | --- |
| Frontend Project Root | `/absolute/path` | Developer confirmation |
| Feature | `feature-name` | Developer confirmation |
| Version | `YYYY-MM-DD[-vN]` | Developer confirmation |
| Output Directory | `/absolute/path/docs/frontend-design/feature/version` | Derived from confirmed values |

| 来源 | 定位/版本 | 已确认范围 |
| --- | --- | --- |

| 检查维度 | 结果 | 证据 |
| --- | --- | --- |

| ID | 类别 | 场景与证据 | 问题 | 前端影响 | 状态 |
| --- | --- | --- | --- | --- | --- |

| ID | Developer Decision | Final Decision | 决策来源 | 影响范围 | 状态 |
| --- | --- | --- | --- | --- | --- |
```

Allowed question states are `Open`, `Resolved`, and `Reopened`. An empty question table is valid only with `Status: Cleared` and `Gate: PASS`. Any `Open` or `Reopened` item requires `Status: Waiting Confirmation` and `Gate: BLOCKED`.

Do not write this artifact before project and version confirmation. Do not generate speculative answers, downstream diagrams, implementation tasks, or source code.
