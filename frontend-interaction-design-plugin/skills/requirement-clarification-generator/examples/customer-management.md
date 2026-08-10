# 客户管理需求澄清（生命周期示例）

## Waiting Confirmation

```markdown
# 客户管理需求澄清

Status: Waiting Confirmation
Gate: BLOCKED

## 澄清问题

| ID | 类别 | 场景与证据 | 问题 | 前端影响 | 状态 |
| --- | --- | --- | --- | --- | --- |
| CL-01 | PRD ↔ 原型冲突 | PRD 只描述单个删除；原型含批量删除按钮 | 本期是否支持批量删除？ | 决定选择态、确认文案和 API 调用方式 | Open |
| CL-02 | 业务规则缺失 | PRD 和原型均未说明删除确认 | 删除前是否需要二次确认？ | 决定是否存在确认弹窗及取消流程 | Open |
| CL-03 | API 规则缺失 | 创建 API 未声明幂等机制 | 前端应如何处理重复提交与自动重试？ | 决定提交锁定和重试行为 | Open |
| CL-04 | 原型行为缺失 | 原型未说明提交中是否可取消 | 提交中是否允许关闭创建弹窗？ | 决定状态转换和迟到响应处理 | Open |

## Gate 结果与下游交接

- Gate 为 BLOCKED；不得生成 user-flow.md。
```

## Resolved

```markdown
# 客户管理需求澄清

Status: Resolved
Gate: PASS

## 已确认决策

| ID | 用户确认的决策 | 决策来源 | 影响范围 |
| --- | --- | --- | --- |
| CL-01 | V2 仅支持单个删除；隐藏批量删除入口 | 用户确认 | User Flow、页面元素、API 映射 |
| CL-02 | 删除前必须二次确认，取消不调用 API | 用户确认 | User Flow、State Machine、Sequence |
| CL-03 | 提交中禁用重复提交，不自动重试；后端不提供幂等键 | 用户确认 | State Machine、Sequence、开发任务 |
| CL-04 | 提交中禁用取消和关闭；等待请求完成后再转换状态 | 用户确认 | State Machine、Sequence、异常处理 |

## Gate 结果与下游交接

- Gate 为 PASS；下游产物必须引用 CL-01～CL-04。
```
