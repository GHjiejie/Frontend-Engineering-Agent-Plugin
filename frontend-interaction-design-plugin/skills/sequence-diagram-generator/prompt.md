# Sequence Diagram Output Contract

Write `frontend-design/<feature-name>/sequence-diagram.md` in this section order:

1. `# <功能名称>前后端交互时序`
2. `## 输入与覆盖范围`
3. `## API 清单`
4. `## Flow / State / API 映射`
5. One `## SQ-xx <场景名称>` section per meaningful interaction
6. `## API 契约缺口`
7. `## 待确认项`
8. `## 下游交接`

Required tables:

```markdown
| API ID | Method | Path | 用途 | 请求摘要 | 成功响应 | 已声明错误 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |

| Sequence ID | Flow ID | State ID / transition | API ID | 触发动作 | 完成后的 UI 状态 |
| --- | --- | --- | --- | --- | --- |
```

For each sequence, include preconditions, a Mermaid `sequenceDiagram`, request/response notes, and state-transition effects. Use `alt`, `else`, and `opt` for real branches. Keep participant names stable across diagrams.

Never display secrets or fabricate backend internals. If a required contract detail is absent, reference an `API-GAP-xx` item instead of filling it with a plausible value.
