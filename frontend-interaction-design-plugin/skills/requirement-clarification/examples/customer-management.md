# 客户管理需求澄清（生命周期示例）

## Preflight confirmation

在创建文件前向开发者确认：

```text
Frontend Project Root: /workspace/console-ui
Feature: customer-management
Action: Create a new iteration
Version: 2026-08-10
Output: /workspace/console-ui/docs/frontend-design/customer-management/2026-08-10
```

## Waiting Confirmation

```markdown
# 客户管理需求澄清

Status: Waiting Confirmation
Gate: BLOCKED

## 已确认运行上下文

| 项目 | 已确认值 | 确认依据 |
| --- | --- | --- |
| Frontend Project Root | `/workspace/console-ui` | Developer confirmation |
| Feature | `customer-management` | Developer confirmation |
| Version | `2026-08-10` | Developer confirmation |
| Output Directory | `/workspace/console-ui/docs/frontend-design/customer-management/2026-08-10` | Derived from confirmed values |

## 澄清问题

| ID | 类别 | 场景与证据 | 问题 | 前端影响 | 状态 |
| --- | --- | --- | --- | --- | --- |
| CL-01 | Prototype ↔ API conflict | 原型支持批量删除；API 仅提供单条删除 | 当前版本如何处理批量删除？ | 决定选择态、确认文案和 API 调用 | Open |
| CL-02 | 业务规则缺失 | PRD 和原型均未说明删除确认 | 删除前是否需要二次确认？ | 决定确认弹窗及取消流程 | Open |
| CL-03 | API 规则缺失 | 创建 API 未声明幂等机制 | 前端如何处理重复提交与自动重试？ | 决定提交锁定和重试行为 | Open |
| CL-04 | Prototype behavior missing | 原型未说明提交中是否可关闭 | 提交中是否允许取消或关闭弹窗？ | 决定状态转换和迟到响应处理 | Open |

## Gate 结果与下游交接

- Gate 为 BLOCKED；不得生成 `user-flow.md`。
```

## Resolved

```markdown
Status: Resolved
Gate: PASS

## 已确认决策

| ID | Developer Decision | Final Decision | 决策来源 | 影响范围 | 状态 |
| --- | --- | --- | --- | --- | --- |
| CL-01 | 当前版本不实现批量删除 | 从所有下游流程移除批量删除 | Developer confirmation | User Flow、State、Sequence、Plan | Resolved |
| CL-02 | 删除前必须二次确认 | 取消时不调用 API | Developer confirmation | User Flow、State、Sequence | Resolved |
| CL-03 | 禁用重复提交且不自动重试 | 提交中锁定按钮，失败后由用户显式重试 | Developer confirmation | State、Sequence、Plan | Resolved |
| CL-04 | 提交中禁止取消和关闭 | 等待请求完成后再转换状态 | Developer confirmation | User Flow、State、Sequence | Resolved |

## Gate 结果与下游交接

- 三个人工 Gate 均已通过；下游固定写入已确认的 `2026-08-10` 目录并引用 CL-01～CL-04。
```
