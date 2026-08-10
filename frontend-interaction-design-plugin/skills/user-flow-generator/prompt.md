# User Flow Output Contract

Write `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/user-flow.md` in the source language unless the user requests another language.

Use this exact section order:

1. `# <功能名称>用户流程`
2. `## 已确认运行上下文`
3. `## 范围、来源与澄清 Gate`
4. `## 参与者与前置条件`
5. `## 页面与交互元素`
6. `## 流程清单`
7. One `## UF-xx <流程名称>` section per meaningful goal
8. `## 澄清决策引用`
9. `## 下游交接`

Required tables:

```markdown
| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |

| 来源 | 定位 | 已确认信息 |
| --- | --- | --- |

| 页面/容器 | 元素 | 类型 | 支持的动作 | 来源 |
| --- | --- | --- | --- | --- |

| Flow ID | 用户目标 | 入口 | 成功结果 | 其他结果 |
| --- | --- | --- | --- | --- |

| Flow ID / 步骤 | 来源或 CL ID | 已确认行为 |
| --- | --- | --- |
```

For each flow, include preconditions, numbered user/UI steps, a Mermaid `flowchart TD`, evidence-backed alternative branches, and the resulting visible UI state.

Use short stable Mermaid node IDs such as `A`, `B`, and `C1`. Quote labels containing punctuation. Do not place unresolved questions, assumptions, implementation tasks, source code, endpoint guesses, or component architecture in this artifact. A newly discovered ambiguity must block generation through the same version's `clarification.md`. Never write outside the confirmed output directory.
