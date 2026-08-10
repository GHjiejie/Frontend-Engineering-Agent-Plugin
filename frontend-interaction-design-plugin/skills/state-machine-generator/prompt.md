# State Machine Output Contract

Write `<confirmed-output-directory>/state-machine.md` in this order:

1. `# <功能名称>状态模型`
2. `## 已确认运行上下文`
3. `## 输入、证据与 Gate 状态`
4. `## 状态机清单`
5. One `## SM-xx <页面或组件>` per stateful surface
6. `## 跨状态约束`
7. `## 证据与澄清决策引用`
8. `## 下游交接`

Required tables:

```markdown
| State ID | 页面/组件 | Flow IDs | Prototype IDs | 初始状态 | 关键终态/恢复态 |
| --- | --- | --- | --- | --- | --- |

| 当前状态 | 事件 | Guard | 下一状态 | 可见反馈 | Source / Flow / CL |
| --- | --- | --- | --- | --- | --- |

| State / Transition | Evidence ID | Confirmed Behavior |
| --- | --- | --- |
```

For each state machine include state definitions, rendered UI, data ownership and reset rules, a transition table, and Mermaid `stateDiagram-v2`. Do not write framework stores, reducers, code, guessed API behavior, or unresolved transitions.
