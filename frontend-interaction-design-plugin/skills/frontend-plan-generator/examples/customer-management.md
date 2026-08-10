# 客户管理前端开发方案（节选）

## 1. 功能概述

本期支持客户列表查询与新增客户。删除能力不在当前已确认范围内。

## 2. 页面与组件设计

```text
CustomerPage
├── CustomerSearchArea
├── CustomerTable
└── CustomerCreateDialog
```

- `CustomerPage`：协调列表查询、刷新与页面级反馈。
- `CustomerCreateDialog`：负责字段输入、前端校验、提交反馈和取消。

## 3. 状态设计

| 状态域 | 数据/状态 | 所有者 | 初始值 | 变化事件 | 重置条件 | 关联 State ID |
| --- | --- | --- | --- | --- | --- | --- |
| 客户列表 | customers、loading、error | CustomerPage | 空列表、idle | LOAD、RESOLVE、REJECT | 离开页面 | SM-01 |
| 创建弹窗 | opened、form、submitting、error | CustomerCreateDialog | closed、空表单 | OPEN、SUBMIT、RESOLVE、REJECT、CANCEL | 成功或取消 | SM-02 |

## 4. API 调用方案

| 场景 | API ID | Method / Path | 触发时机 | 请求摘要 | 成功处理 | 失败处理 | 关联 Sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 创建客户 | API-01 | POST `/customers` | 有效表单提交 | `name`, `email` | 关闭弹窗并刷新列表 | 保留输入并显示合同声明的错误 | SQ-01 |
| 刷新列表 | API-02 | GET `/customers` | 页面加载、创建成功 | 分页参数 | 更新列表或空态 | 显示可重试错误 | SQ-01 |

## 5. 交互与异常处理

- 无效表单不调用 API，错误显示在对应字段附近。
- 提交期间禁用重复提交。
- 400、409、500 按 API PRD 的语义展示反馈；未声明错误使用通用可恢复提示。
- 幂等策略属于 `API-GAP-01`，联调前需要后端确认。

## 6. 开发任务拆分

| Task ID | 任务 | 输入 | 交付物 | 依赖 | 验收标准 |
| --- | --- | --- | --- | --- | --- |
| FE-01 | 页面结构与列表状态 | PRD、原型、SM-01 | 页面结构和状态接线 | — | 加载、空、成功、错误状态可独立验收 |
| FE-02 | 客户 API 适配 | API-01、API-02 | 类型化请求/响应边界 | — | 请求字段与响应映射符合合同 |
| FE-03 | 创建弹窗交互 | UF-01、SM-02 | 表单、校验和反馈行为 | FE-02 | 成功、失败、取消、重复提交均符合模型 |
| FE-04 | 联调与交互测试 | SQ-01 | 场景验证结果 | FE-01、FE-03 | 主流程与错误分支全部通过 |

## 7. 追踪矩阵

| 需求/来源 | User Flow | State | Sequence / API | Task |
| --- | --- | --- | --- | --- |
| PRD：新增客户 | UF-01 | SM-01、SM-02 | SQ-01 / API-01、API-02 | FE-01～FE-04 |

## 8. 风险、假设与待确认项

- 阻塞项：确认 API-GAP-01 的重复提交策略。

## 9. 前端 Review 清单

- [ ] 用户流程、状态和 API 映射一致
- [ ] 空态、失败、重试和取消均有可见反馈
- [ ] 未把待确认项实现为默认行为
