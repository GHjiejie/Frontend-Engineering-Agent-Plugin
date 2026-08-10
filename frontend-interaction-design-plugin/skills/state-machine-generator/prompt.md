# State Machine Output Contract

Write `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/state-machine.md` in this section order:

1. `# <功能名称>状态模型`
2. `## 已确认运行上下文`
3. `## 输入、覆盖范围与澄清 Gate`
4. `## 状态机清单`
5. One `## SM-xx <页面或组件>` section per stateful surface
6. `## 跨状态约束`
7. `## 澄清决策引用`
8. `## 下游交接`

Required inventory:

```markdown
| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |

| State ID | 页面/组件 | 关联 Flow | 初始状态 | 关键终态/恢复态 |
| --- | --- | --- | --- | --- |
```

For each state machine, include scope and linked evidence, state definitions with rendered UI, a transition table, a Mermaid `stateDiagram-v2`, and data preservation/retry rules.

Use this transition shape:

```markdown
| 当前状态 | 事件 | Guard | 下一状态 | 可见反馈 | 来源 |
| --- | --- | --- | --- | --- | --- |

| State / transition | CL ID | 已确认决策 |
| --- | --- | --- |
```

Use concise Mermaid aliases when localized labels contain punctuation. Avoid unresolved transitions, implementation-specific store names, framework code, reducers, components, or unconfirmed API behavior. Model only states actually required by evidence. Route new uncertainty back to the same version's `clarification.md` instead of writing a pending state, and never write outside the confirmed directory.
