# Requirement Clarification Output Contract

Write `<confirmed-output-directory>/clarification.md` in this order:

1. `# <功能名称>需求澄清`
2. `Status: Cleared | Waiting Confirmation | Resolved`
3. `Clarification Gate: PASS | BLOCKED`
4. `## 已确认运行上下文`
5. `## 来源与 Source Gate`
6. `## 一致性检查摘要`
7. `## 澄清问题`
8. `## 已确认决策`
9. `## Gate 结果与下游交接`

Use these tables:

```markdown
| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |

| Source ID | Type | Locator / Version | Confirmed Scope | Evidence Location |
| --- | --- | --- | --- | --- |

| 检查维度 | 结果 | PRD Evidence | Prototype Evidence | API Evidence |
| --- | --- | --- | --- | --- |

| ID | 类别 | 场景与证据 | 问题 | 前端影响 | 状态 |
| --- | --- | --- | --- | --- | --- |

| ID | Developer Decision | Final Decision | 决策来源 | 影响范围 | 状态 |
| --- | --- | --- | --- | --- | --- |
```

Allowed question states are `Open`, `Resolved`, and `Reopened`. Any Open/Reopened item requires `Status: Waiting Confirmation` and `Clarification Gate: BLOCKED`.

Do not repeat source acquisition, invent answers, produce downstream models, or write code. Preserve reviewer notes and resolved history across same-version updates.
