# Sequence Diagram Output Contract

Write `<confirmed-output-directory>/sequence-diagram.md` in this order:

1. `# <功能名称>前后端交互时序`
2. `## 已确认运行上下文`
3. `## 输入、证据与 Gate 状态`
4. `## API 清单`
5. `## Flow / State / API 映射`
6. One `## SQ-xx <场景名称>` per meaningful interaction
7. `## API 契约依据`
8. `## 证据与澄清决策引用`
9. `## 下游交接`

Required tables:

```markdown
| API ID | Method | Path | Purpose | Request | Success | Declared Errors | Source / Version |
| --- | --- | --- | --- | --- | --- | --- | --- |

| Sequence ID | Flow ID | State Transition | API ID | Trigger | Resulting UI State |
| --- | --- | --- | --- | --- | --- |

| Sequence / Branch | Source or CL ID | Confirmed Behavior |
| --- | --- | --- |
```

For each sequence include preconditions, Mermaid `sequenceDiagram`, request/response notes, and state effects. Use `alt`, `else`, and `opt` only for evidenced branches. Never display secrets or complete a sequence around an unresolved API gap.
