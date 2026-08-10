# Customer Management Frontend Development Plan（节选）

Status: Ready for Development

## 已确认运行上下文

| Frontend Project Root | Feature | Version | Output Directory |
| --- | --- | --- | --- |
| `/workspace/console-ui` | `customer-management` | `2026-08-10` | `/workspace/console-ui/docs/frontend-design/customer-management/2026-08-10` |

## 1. 功能背景与目标

本期支持客户列表查询与新增客户。三个 Human Gate 均已通过；`clarification.md` 为 `Resolved / PASS`。

## 2. 本次开发范围

- 范围内：客户列表加载、空态、错误态和新增客户。
- 范围外：批量删除（CL-01）。

## 3. 页面与交互实现

```text
CustomerPage
├── CustomerSearchArea
├── CustomerTable
└── CustomerCreateDialog
```

## 4. User Flow 摘要

- UF-01：从客户列表打开创建弹窗，提交有效表单，成功后刷新列表；失败时保留输入。

## 5. 状态设计

| 状态域 | 数据/状态 | 所有者 | 初始值 | 变化事件 | 重置条件 | 关联 State ID |
| --- | --- | --- | --- | --- | --- | --- |
| 客户列表 | customers、loading、error | CustomerPage | 空列表、idle | LOAD、RESOLVE、REJECT | 离开页面 | SM-01 |
| 创建弹窗 | opened、form、submitting、error | CustomerCreateDialog | closed、空表单 | OPEN、SUBMIT、RESOLVE、REJECT、CANCEL | 成功或取消 | SM-02 |

## 6. API 使用方案

| 场景 | API ID | Method / Path | 触发时机 | 请求摘要 | 成功处理 | 失败处理 | 关联 Sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 创建客户 | API-01 | POST `/customers` | 有效表单提交 | `name`, `email` | 关闭弹窗并刷新列表 | 保留输入并显示已声明错误 | SQ-01 |
| 刷新列表 | API-02 | GET `/customers` | 页面加载、创建成功 | 分页参数 | 更新列表或空态 | 显示可重试错误 | SQ-01 |

## 7. API 与交互 Mapping

| User Flow | State transition | Sequence | API |
| --- | --- | --- | --- |
| UF-01 | SM-02 opened → submitting → closed/failed | SQ-01 | API-01、API-02 |

## 8. 异常与边界状态

- 无效表单不调用 API，错误显示在对应字段附近。
- 根据 CL-03，提交期间禁用重复提交且不自动重试。
- 根据 CL-04，提交期间禁用取消和关闭；失败后保留输入。

## 9. 关键开发决策

- CL-01：当前版本不实现批量删除。
- CL-03：禁止重复提交和自动重试。
- CL-04：提交中禁止取消或关闭。

## 10. 开发任务拆分

| Task ID | 任务 | 输入 | 交付物 | 依赖 | 验收标准 |
| --- | --- | --- | --- | --- | --- |
| FE-01 | 页面结构与列表状态 | PRD、原型、SM-01 | 页面结构和状态接线 | — | 加载、空、成功、错误状态可独立验收 |
| FE-02 | 客户 API 适配 | API-01、API-02 | 类型化请求/响应边界 | — | 请求与响应映射符合合同 |
| FE-03 | 创建弹窗交互 | UF-01、SM-02 | 表单、校验和反馈行为 | FE-02 | 成功、失败、取消、重复提交符合模型 |
| FE-04 | 联调与交互测试 | SQ-01 | 场景验证结果 | FE-01、FE-03 | 主流程与错误分支全部通过 |

## 11. 已确认事项

- Project、Feature、Version 与输出目录均经开发者确认。
- CL-01～CL-04 已解决并在下游产物中可追踪。

## 12. 未解决问题

- 无阻塞问题。

## 追踪矩阵

| 需求/来源 | Clarification | User Flow | State | Sequence / API | Task |
| --- | --- | --- | --- | --- | --- |
| PRD：新增客户 | CL-03、CL-04 | UF-01 | SM-01、SM-02 | SQ-01 / API-01、API-02 | FE-01～FE-04 |

## Technical Review 清单

- [ ] 项目、Feature、Version 与五个产物路径一致
- [ ] 用户流程、状态和 API 映射一致
- [ ] 所有 CL 决策均可追踪到交互、状态、时序和任务
- [ ] 不存在未确认业务决策或虚构的后端内部细节
