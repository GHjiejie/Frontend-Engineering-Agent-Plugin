Frontend Interaction Design Plugin 架构设计方案（V4）

1. 文档目的

本文档定义一个用于前端需求分析与开发方案生成的 Plugin。

该 Plugin 面向真实前端研发流程，输入产品 PRD、前端原型和后端 API 文档，在人工确认关键工程路径和业务歧义后，生成当前业务功能对应的：

User Flow（用户流程图）
State Machine（前端状态机图）
Sequence Diagram（前后端时序图）
Frontend Development Plan（前端开发方案）

Plugin 的核心原则是：

> AI 负责分析、发现问题和提出建议；涉及工程路径、业务规则和版本选择的关键决策必须由开发者确认。

***
2. Plugin 定位

建议名称：

frontend-interaction-design

核心职责：

Product PRD
    +
Prototype
    +
Backend API
    ↓
需求一致性检查
    ↓
开发者澄清
    ↓
交互建模
    ↓
前端开发方案
    ↓
Technical Review

Plugin 不负责：

自动生成业务代码
自动修改前端源码
自动提交 Git Commit / Pull Request
自行修改产品需求
自行修改后端 API
在存在关键歧义时自行做业务决策

代码生成应由后续 Coding Agent / Coding Skill 消费本 Plugin 的输出。

***
3. 输入资源

Plugin 的核心输入包括：

1. Product PRD
2. Prototype
3. Backend API / API PRD / OpenAPI

其中原型可以是：

Figma
Axure
页面截图
原型图片
其他可解析 UI 原型

后端接口资料可以是：

OpenAPI
Swagger
API PRD
接口 Markdown
后端提供的接口说明

***
4. 总体架构

                         Plugin Start
                              │
                              ▼
                 Frontend Project Discovery
                              │
                              ▼
                  推断当前目标前端项目
                              │
                              ▼
                 ┌──────────────────────┐
                 │ Human Gate #1        │
                 │ 前端项目人工确认      │
                 └──────────┬───────────┘
                            │
                            ▼
                  锁定 frontend-project-root
                            │
                            ▼
                       Feature识别
                            │
                            ▼
                       Version识别
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Human Gate #2        │
                 │ 版本目录人工确认      │
                 └──────────┬───────────┘
                            │
                            ▼
              Requirement Clarification Skill
                            │
                   ┌────────┴────────┐
                   │                 │
                 无歧义             有歧义
                   │                 │
                   │                 ▼
                   │          Clarification Questions
                   │                 │
                   │                 ▼
                   │        ┌────────────────────┐
                   │        │ Human Gate #3      │
                   │        │ 业务歧义人工确认    │
                   │        └─────────┬──────────┘
                   │                  │
                   └──────────────────┘
                            │
                            ▼
                  User Flow Generator
                            │
                            ▼
                State Machine Generator
                            │
                            ▼
               Sequence Diagram Generator
                            │
                            ▼
                Frontend Plan Generator
                            │
                            ▼
                 Frontend Design Package
                            │
                            ▼
                     Technical Review
                            │
                            ▼
                       Coding Agent

***
5. Plugin 目录结构

Plugin 自身保持简单，只包含 5 个核心 Skill：

frontend-interaction-design/
├── README.md
├── plugin.yaml
│
└── skills/
    ├── requirement-clarification/
    │   ├── SKILL.md
    │   └── examples/
    │
    ├── user-flow-generator/
    │   ├── SKILL.md
    │   └── examples/
    │
    ├── state-machine-generator/
    │   ├── SKILL.md
    │   └── examples/
    │
    ├── sequence-diagram-generator/
    │   ├── SKILL.md
    │   └── examples/
    │
    └── frontend-plan-generator/
        ├── SKILL.md
        └── examples/

说明：

Frontend Project Discovery 属于 Plugin 编排逻辑，不单独拆成 Skill。
Feature / Version 识别属于 Plugin 编排逻辑，不单独拆成 Skill。
Human Gate 属于流程控制，不单独拆成 Skill。
第一版不增加 Code Generator、Test Generator 等无关能力。

***
6. Frontend Project Discovery

在创建任何文件之前，Plugin 必须首先识别当前需求对应的前端项目。

6.1 判断依据

可以综合：

- 当前 Working Directory
- package.json
- src/
- vite.config.*
- webpack.config.*
- 前端 Framework 依赖
- 项目已有页面和路由
- PRD 中的系统名称
- 原型中的系统名称

例如：

workspace/
├── console-ui/
│   ├── package.json
│   ├── src/
│   └── vite.config.ts
│
├── console-backend/
│   └── go.mod
│
└── deployment/

Plugin 可以推断：

frontend-project-root = workspace/console-ui

但不得直接写入。

***
7. Human Gate #1：前端项目确认

Plugin 必须将判断结果展示给开发者：

检测到当前需求最可能对应：

console-ui

目标项目路径：
<workspace>/console-ui

计划在该项目 docs 下生成前端设计文档。

是否确认？

开发者确认后，锁定：

{frontend-project-root}

本次任务后续所有 Skill 均使用该路径，不再自行重新判断。

如果无法可靠判断，则直接要求用户选择，不得猜测。

***
8. Feature 目录模型

所有文档均按业务功能进行组织。

例如：

customer-management
order-management
user-management
role-permission-management

禁止按文档类型组织：

user-flow/
state-machine/
sequence-diagram/

正确模型：

Feature
    ↓
Version
    ↓
Design Documents

***
9. Version 目录模型

由于同一功能会持续迭代，因此每次独立需求迭代都应生成一个版本目录。

统一目录规范：

{frontend-project-root}/
└── docs/
    └── frontend-design/
        └── {feature-name}/
            └── {YYYY-MM-DD[-vN]}/

例如：

console-ui/
└── docs/
    └── frontend-design/
        └── customer-management/
            ├── 2026-08-10/
            ├── 2026-08-25/
            └── 2026-09-03/

***
10. 版本生成规则

10.1 默认格式

YYYY-MM-DD

例如：

2026-08-10/

10.2 同一天多个独立版本

使用：

2026-08-10/
2026-08-10-v2/
2026-08-10-v3/

不推荐使用秒级时间戳作为默认版本名。

10.3 什么情况下创建新版本

创建新版本：

产品发布新的 PRD 迭代
原型发生影响功能行为的明显变化
后端 API 发生影响当前功能的重大变化
已完成方案进入下一轮独立需求迭代
用户明确要求创建新版本

不创建新版本：

当前需求澄清
开发者回答 clarification 问题
当前方案 Review 修改
同一轮设计中的图表修正
文档文字修正

这些修改都继续更新当前版本目录，由 Git 记录细粒度历史。

***
11. Human Gate #2：版本确认

如果 Feature 已存在历史版本：

docs/frontend-design/customer-management/
├── 2026-07-20/
└── 2026-08-01/

Plugin 应判断当前需求是：

A. 继续修改当前版本
B. 创建新的需求版本

Plugin 可以推荐，但必须由开发者确认。

例如：

检测到 customer-management 已存在历史版本。

最新版本：
2026-08-01

当前输入包含新的 PRD / 原型变更，
推测属于新的功能迭代。

计划创建：

docs/frontend-design/customer-management/2026-08-10/

是否确认？

***
12. Skill 1：Requirement Clarification

12.1 职责

对以下三类输入进行一致性检查：

Product PRD
Prototype
Backend API

识别：

缺失
冲突
歧义
未定义交互
API 与 UI 不匹配
API 与 PRD 不匹配
原型与 PRD 不匹配
关键业务规则缺失

***
12.2 核心原则

> 当歧义会影响用户流程、前端状态、API 调用或开发实现时，禁止自行推断。

必须询问开发者。

***
12.3 示例：原型与 API 冲突

原型：

批量删除

API：

DELETE /customers/{id}

不得自行决定：

循环调用 DELETE

必须询问：

当前原型支持批量删除，但后端只提供单条删除接口。

请确认：

A. 前端循环调用单条删除接口
B. 后端新增批量删除接口
C. 当前版本不实现批量删除
D. 其他

***
13. Human Gate #3：业务歧义确认

Requirement Clarification Skill 发现关键歧义后：

发现问题
    ↓
提出问题
    ↓
等待开发者确认
    ↓
记录 Decision
    ↓
重新检查
    ↓
仍有关键歧义 → 继续询问
    ↓
全部 Clear
    ↓
进入正式图表生成

只有所有阻塞开发的关键问题都被确认后，才能继续生成正式开发方案。

***
14. clarification.md

所有开发者确认过的关键业务决策必须记录：

docs/frontend-design/{feature-name}/{version}/clarification.md

推荐结构：

# Requirement Clarification

## Q1 批量删除

### Context
原型存在批量删除按钮，但后端只提供单条删除 API。

### Developer Decision
当前版本不实现批量删除。

### Final Decision
本版本从 User Flow、State Machine 和 Sequence Diagram 中移除批量删除流程。

### Status
Resolved

clarification.md 是后续所有 Skill 的高优先级事实来源。

***
15. 信息优先级原则

当原始资料发生冲突时，不允许简单规定：

PRD 永远优先
API 永远优先
Prototype 永远优先

因为任意一方都可能不是最新版。

正确优先级：

Developer Confirmed Decision
            ↓
        Highest Priority

如果：

Product PRD ≠ Prototype ≠ Backend API

则：

发现冲突
    ↓
开发者确认
    ↓
Confirmed Decision
    ↓
后续所有 Skill 使用该 Decision

***
16. Skill 2：User Flow Generator

输入

Product PRD
Prototype
Confirmed Clarifications

输出

user-flow.md

职责：

> 描述当前 Feature 中用户如何操作系统。

主要回答：

用户做什么？

推荐使用 Mermaid Flowchart。

***
17. Skill 3：State Machine Generator

输入

User Flow
Prototype
Confirmed Clarifications

输出

state-machine.md

职责：

> 描述前端 UI 和交互状态如何变化。

主要回答：

页面怎么变化？

至少覆盖当前功能实际涉及的：

loading
empty
data
error
submitting
success
failed
disabled
dialog open / close

不得为了完整而制造 PRD 中不存在的业务状态。

***
18. Skill 4：Sequence Diagram Generator

输入

User Flow
State Machine
Backend API
Confirmed Clarifications

输出

sequence-diagram.md

职责：

> 描述用户行为对应的前后端数据交互。

主要回答：

谁在什么时候调用谁？

至少描述：

用户动作
Browser / Frontend
Backend / BFF
已明确的下游服务
API 请求
API 返回
前端状态变化

如果 API 文档没有暴露数据库或内部服务细节，不得自行编造 Database / Service 调用。

***
19. Skill 5：Frontend Plan Generator

输入

Product PRD
Prototype
Backend API

clarification.md
user-flow.md
state-machine.md
sequence-diagram.md

输出

frontend-development-plan.md

职责：

> 将所有已经确认的信息汇总成当前 Feature 可以 Review 和执行的前端开发方案。

它不负责写业务代码。

***
20. Frontend Development Plan 结构

推荐固定结构：

# {Feature} Frontend Development Plan

1. 功能背景与目标
2. 本次开发范围
3. 页面与交互实现
4. User Flow 摘要
5. 状态设计
6. API 使用方案
7. API 与交互 Mapping
8. 异常与边界状态
9. 关键开发决策
10. 开发任务拆分
11. 已确认事项
12. 未解决问题

如果存在阻塞开发的：

未解决问题

则不得标记为：

Ready for Development

***
21. 最终输出结构

完整示例：

console-ui/
├── src/
├── package.json
├── ...
│
└── docs/
    └── frontend-design/
        │
        ├── customer-management/
        │   │
        │   ├── 2026-08-10/
        │   │   ├── clarification.md
        │   │   ├── user-flow.md
        │   │   ├── state-machine.md
        │   │   ├── sequence-diagram.md
        │   │   └── frontend-development-plan.md
        │   │
        │   └── 2026-09-03/
        │       ├── clarification.md
        │       ├── user-flow.md
        │       ├── state-machine.md
        │       ├── sequence-diagram.md
        │       └── frontend-development-plan.md
        │
        └── order-management/
            └── 2026-08-16/
                ├── clarification.md
                ├── user-flow.md
                ├── state-machine.md
                ├── sequence-diagram.md
                └── frontend-development-plan.md

***
22. Plugin 运行状态机

INIT
 │
 ▼
DISCOVERING_PROJECT
 │
 ▼
WAITING_PROJECT_CONFIRMATION
 │
 │ 用户确认
 ▼
RESOLVING_FEATURE
 │
 ▼
RESOLVING_VERSION
 │
 ▼
WAITING_VERSION_CONFIRMATION
 │
 │ 用户确认
 ▼
ANALYZING_REQUIREMENTS
 │
 ├─────存在歧义─────► WAITING_CLARIFICATION
 │                       │
 │                       │ 用户回答
 │                       ▼
 │                ANALYZING_REQUIREMENTS
 │
 │ 无阻塞歧义
 ▼
GENERATING_USER_FLOW
 │
 ▼
GENERATING_STATE_MACHINE
 │
 ▼
GENERATING_SEQUENCE_DIAGRAM
 │
 ▼
GENERATING_FRONTEND_PLAN
 │
 ▼
READY_FOR_REVIEW
 │
 ▼
COMPLETED

***
23. Human-in-the-loop 模型

整个 Plugin 至少存在三个关键人工 Gate：

Gate #1
确认目标前端项目

Gate #2
确认当前 Feature 的版本目录

Gate #3
确认 PRD / Prototype / API 的业务歧义

核心思想：

> Machine discovers; developer decides.

***
24. 全局禁止规则

所有 Skill 必须遵守：

不得猜测未定义的业务规则。
不得在 PRD、Prototype、API 冲突时自行选择其中一个。
不得自行决定新增后端 API。
不得自行改变原型交互。
不得自行决定产品行为。
不得未经用户确认选择目标前端项目。
不得未经用户确认创建新的版本目录。
不得在项目确认前写入 docs/frontend-design。
不得在关键歧义未解决时生成 Ready for Development 方案。
开发者明确确认的 Decision 优先于模型推测和原始冲突资料。
后续所有 Skill 必须消费已确认的 clarification。
不得覆盖历史独立版本的设计文档。
同一轮需求澄清和 Review 不应频繁创建新版本。
不得为了让图“更完整”而虚构不存在的服务、数据库、状态或交互。

***
25. Review 模型

最终团队 Review 的主要入口：

frontend-development-plan.md

辅助依据：

clarification.md
user-flow.md
state-machine.md
sequence-diagram.md

角色关注点：

产品：
User Flow + Clarification

前端：
State Machine + Frontend Development Plan

后端：
Sequence Diagram + API Mapping

Reviewer：
Frontend Development Plan + 三个图 + Clarification

***
26. 与后续 Coding Agent 的关系

本 Plugin：

负责“想清楚”

Coding Agent：

负责“写进去”

完整链路：

Product PRD
+
Prototype
+
Backend API
        ↓
Frontend Interaction Design Plugin
        ↓
Clarification
        ↓
Three Diagrams
        ↓
Frontend Development Plan
        ↓
Technical Review
        ↓
Coding Agent
        ↓
Frontend Source Code

因此：

> 三个图是交互分析模型，Frontend Development Plan 是开发与 Review 的主要交付物。

***
27. 最终架构总结

                           INPUT
                             │
                 ┌───────────┼───────────┐
                 │           │           │
              Product     Prototype     API
                PRD
                 └───────────┼───────────┘
                             │
                             ▼
                  Frontend Project Discovery
                             │
                             ▼
                       HUMAN GATE #1
                       确认前端项目
                             │
                             ▼
                       Feature Resolve
                             │
                             ▼
                       Version Resolve
                             │
                             ▼
                       HUMAN GATE #2
                       确认版本目录
                             │
                             ▼
                 Requirement Clarification
                             │
                             ▼
                       HUMAN GATE #3
                       确认业务歧义
                             │
                             ▼
                        User Flow
                             │
                             ▼
                      State Machine
                             │
                             ▼
                    Sequence Diagram
                             │
                             ▼
                Frontend Development Plan
                             │
                             ▼
                         REVIEW
                             │
                             ▼
                       Coding Agent

最终输出规范：

{confirmed-frontend-project-root}/
└── docs/
    └── frontend-design/
        └── {feature-name}/
            └── {YYYY-MM-DD[-vN]}/
                ├── clarification.md
                ├── user-flow.md
                ├── state-machine.md
                ├── sequence-diagram.md
                └── frontend-development-plan.md

***
28. V4 核心设计结论

本版本最终确定四个核心原则：

1. 项目路径不能猜着写
2. 业务需求不能猜着做
3. 功能版本不能直接覆盖
4. AI 可以推荐，但关键决策必须由开发者确认

这四条应作为整个 Plugin 的最高级全局约束。