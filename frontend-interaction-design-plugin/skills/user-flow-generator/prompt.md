# User Flow Output Contract

Write `<confirmed-output-directory>/user-flow.md` in this order:

1. `# <功能名称>用户流程`
2. `## 已确认运行上下文`
3. `## 来源与 Gate 状态`
4. `## 参与者与前置条件`
5. `## 页面与交互元素`
6. `## 流程清单`
7. One `## UF-xx <流程名称>` per meaningful goal
8. `## 证据与澄清决策引用`
9. `## 下游交接`

Required tables:

```markdown
| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |

| 页面/容器 | 元素 | 类型 | 支持动作 | PRD / Prototype Evidence |
| --- | --- | --- | --- | --- |

| Flow ID | 用户目标 | 入口 | 成功结果 | 其他结果 | Prototype IDs |
| --- | --- | --- | --- | --- | --- |

| Flow ID / Step | Source or CL ID | Confirmed Behavior |
| --- | --- | --- |
```

For each flow include preconditions, numbered user/UI steps, Mermaid `flowchart TD`, evidence-backed alternatives, and visible terminal states. Do not place assumptions, implementation tasks, guessed endpoints, or unresolved questions in this artifact.
