# Sequence Diagram Output Contract

Write `<confirmed-frontend-project-root>/docs/frontend-design/<feature-name>/<confirmed-version>/sequence-diagram.md` in this section order:

1. `# <功能名称>前后端交互时序`
2. `## 已确认运行上下文`
3. `## 输入、覆盖范围与澄清 Gate`
4. `## API 清单`
5. `## Flow / State / API 映射`
6. One `## SQ-xx <场景名称>` section per meaningful interaction
7. `## API 契约依据`
8. `## 澄清决策引用`
9. `## 下游交接`

Required tables:

```markdown
| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |

| API ID | Method | Path | 用途 | 请求摘要 | 成功响应 | 已声明错误 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |

| Sequence ID | Flow ID | State ID / transition | API ID | 触发动作 | 完成后的 UI 状态 |
| --- | --- | --- | --- | --- | --- |

| Sequence / branch | 来源或 CL ID | 已确认行为 |
| --- | --- | --- |
```

For each sequence, include preconditions, a Mermaid `sequenceDiagram`, request/response notes, and state-transition effects. Use `alt`, `else`, and `opt` for real branches. Keep participant names stable across diagrams.

Never display secrets, fabricate databases or backend internals, or emit an incomplete sequence around a consequential API gap. Return the gap to `requirement-clarification` in the same version and wait for confirmation before writing this artifact. Never write outside the confirmed directory.
