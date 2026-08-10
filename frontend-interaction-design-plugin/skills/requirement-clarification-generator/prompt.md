# Requirement Clarification Output Contract

Write `frontend-design/<feature-name>/clarification.md` in this exact section order:

1. `# <功能名称>需求澄清`
2. `Status: Cleared | Waiting Confirmation | Resolved`
3. `Gate: PASS | BLOCKED`
4. `## 输入与版本`
5. `## 一致性检查摘要`
6. `## 澄清问题`
7. `## 已确认决策`
8. `## Gate 结果与下游交接`

Use these tables:

```markdown
| 来源 | 定位/版本 | 已确认范围 |
| --- | --- | --- |

| 检查维度 | 结果 | 证据 |
| --- | --- | --- |

| ID | 类别 | 场景与证据 | 问题 | 前端影响 | 状态 |
| --- | --- | --- | --- | --- | --- |

| ID | 用户确认的决策 | 决策来源 | 影响范围 |
| --- | --- | --- | --- |
```

Allowed question states are `Open`, `Resolved`, and `Reopened`. An empty question table is valid only with `Status: Cleared` and `Gate: PASS`. Any `Open` or `Reopened` item requires `Status: Waiting Confirmation` and `Gate: BLOCKED`.

Ask the user focused questions after writing a blocked artifact. Do not generate speculative answers, downstream diagrams, implementation tasks, or source code.
