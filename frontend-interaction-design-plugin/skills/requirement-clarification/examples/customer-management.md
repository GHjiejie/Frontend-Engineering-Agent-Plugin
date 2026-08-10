# 客户管理需求澄清（V5 生命周期示例）

前置条件：项目、Feature、Version 已确认，`source-manifest.md` 为 `Source Gate: PASS`。

## Waiting Confirmation

```markdown
# 客户管理需求澄清

Status: Waiting Confirmation
Clarification Gate: BLOCKED

## 来源与 Source Gate

| Source ID | Type | Locator / Version | Confirmed Scope | Evidence Location |
| --- | --- | --- | --- | --- |
| PRD-01 | PRD | Customer PRD / v3 | 列表、新建、删除 | 飞书 Review 文档“输入资料” |
| PT-01 | Prototype | Figma Customer List / node 12:34 | 列表默认状态 | 飞书图片 Block |
| PT-02 | Prototype | Figma Create Dialog / node 12:56 | 新建弹窗 | 飞书图片 Block |
| API-01 | API | Customer API / v2 | 查询、创建、单条删除 | API 文档链接 |

## 澄清问题

| ID | 类别 | 场景与证据 | 问题 | 前端影响 | 状态 |
| --- | --- | --- | --- | --- | --- |
| CL-01 | Prototype ↔ API | PT-01 支持批量删除；API-01 只有单条删除 | 当前版本如何处理批量删除？ | 选择态、确认文案和 API 调用 | Open |
| CL-02 | Missing behavior | PRD-01、PT-01 均未定义删除确认 | 删除前是否需要二次确认？ | 弹窗与取消流程 | Open |
| CL-03 | API behavior | API-01 未声明幂等机制 | 如何处理重复提交与自动重试？ | 提交锁定和重试 | Open |
| CL-04 | Prototype behavior | PT-02 未说明提交中关闭行为 | 提交中是否允许取消或关闭？ | 状态转换与迟到响应 | Open |

## Gate 结果与下游交接

- Clarification Gate 为 BLOCKED；不得生成 `user-flow.md`。
```

## Resolved

```markdown
Status: Resolved
Clarification Gate: PASS

## 已确认决策

| ID | Developer Decision | Final Decision | 决策来源 | 影响范围 | 状态 |
| --- | --- | --- | --- | --- | --- |
| CL-01 | 当前版本不实现批量删除 | 下游移除批量删除 | Developer confirmation | UF、SM、SQ、Plan | Resolved |
| CL-02 | 删除前必须二次确认 | 取消时不调用 API | Developer confirmation | UF、SM、SQ | Resolved |
| CL-03 | 禁用重复提交且不自动重试 | 失败后由用户显式重试 | Developer confirmation | SM、SQ、Plan | Resolved |
| CL-04 | 提交中禁止取消和关闭 | 等待请求完成后转换状态 | Developer confirmation | UF、SM、SQ | Resolved |

## Gate 结果与下游交接

- Gates #1–#4 均通过；`user-flow-generator` 在同一版本引用 PT-01、PT-02 和 CL-01～CL-04。
```
