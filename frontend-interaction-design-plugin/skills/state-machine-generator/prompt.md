# State Machine Output Contract

Write `frontend-design/<feature-name>/state-machine.md` in this section order:

1. `# <功能名称>状态模型`
2. `## 输入、覆盖范围与澄清 Gate`
3. `## 状态机清单`
4. One `## SM-xx <页面或组件>` section per stateful surface
5. `## 跨状态约束`
6. `## 澄清决策引用`
7. `## 下游交接`

Required inventory:

```markdown
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

Use concise Mermaid aliases when localized labels contain punctuation. Avoid unresolved transitions, implementation-specific store names, framework code, reducers, components, or unconfirmed API behavior. Route new uncertainty back to `clarification.md` instead of writing a pending state.
