# Frontend Engineering Knowledge Agent Plugin 架构设计文档

版本：v2.0
状态：Architecture Proposal
目标：构建一个长期驻留在前端项目中的工程知识代理（Frontend Engineering Knowledge Agent）

修订：v2.1 将“用户提供的原型与点击交互效果”提升为 `frontend-analysis` 对所有用户可见变更的强制输入门槛。

---

# 1. 背景与目标

## 1.1 背景

当前 AI Coding Agent 普遍采用：

```text
用户需求
    ↓
LLM理解
    ↓
修改代码
    ↓
完成
```

这种模式存在长期问题：

* AI 每次进入项目都像新人；
* 不知道历史设计原因；
* 不知道以前修复过什么 Bug；
* 不知道哪些人工修改必须保留；
* 不知道业务规则；
* 容易重复犯错。

因此，本 Plugin 的目标不是简单生成代码，而是：

> 建立一个持续理解项目、记录项目演进、参与工程决策的前端工程代理。

---

# 2. 核心理念

整个系统围绕：

```text
Engineering Knowledge System
```

构建。

核心组成：

```text
Project Memory

+

Domain Memory

+

Engineering Entity

+

Memory Runtime

+

Development Pipeline

```

---

# 3. 总体架构

```text

                         User


                          │


                          ▼


                ┌────────────────┐
                │  Orchestrator  │
                └────────────────┘


                          │


        ┌─────────────────┴─────────────────┐


        │                                   │


        ▼                                   ▼


 Memory Runtime                     Development Pipeline


        │                                   │


 ┌──────┴─────────┐                ┌────────┴────────┐
 │                │                │                 │

Memory Store   Memory Router    Analysis          Design


Schema         Context Builder  Implementation    Review


Sync Service

 │


 ▼


Engineering Knowledge


 ┌────────┬────────┬────────┬────────┬────────┐

 │        │        │        │        │

Project Domain Feature Bug Change Decision


```

---

# 4. 系统模块划分

最终系统包含：

| 模块                 | 类型             | 职责      |
| ------------------ | -------------- | ------- |
| Orchestrator       | Runtime        | 流程控制    |
| Memory Runtime     | Infrastructure | 知识检索和管理 |
| Knowledge Storage  | Data           | 知识存储    |
| Engineering Entity | Model          | 工程对象模型  |
| Development Skills | Workflow       | 开发流程    |
| Memory Sync        | Service        | 知识同步    |

---

# 5. Orchestrator

## 5.1 职责

Orchestrator 是整个 Agent 的控制中心。

负责：

* 工作流调度；
* 状态管理；
* Skill 调用；
* Human Gate；
* Artifact 管理。

不负责：

* 写代码；
* 分析业务；
* 修改文件。

---

# 5.2 状态机

```text

INIT


 ↓


MEMORY_SYNC


 ↓


CONTEXT_BUILD


 ↓


ANALYSIS


 ↓


APPROVAL_REQUIRED


 ↓


DESIGN


 ↓


IMPLEMENTATION


 ↓


REVIEW


 ↓


MEMORY_UPDATE


 ↓


COMPLETED


```

异常状态：

```text

BLOCKED

CONFLICT

FAILED

WAITING_HUMAN

```

---

# 6. Memory Runtime

## 6.1 定位

Memory Runtime 是 Agent 的长期记忆系统。

目标：

解决：

> 每次进入项目不重新学习。

---

## 6.2 核心组件

```text

Memory Runtime


├── Memory Router

├── Context Builder

├── Memory Sync

├── Query Engine

└── Cache


```

---

# 6.3 Memory Router

## 职责

根据当前任务寻找相关知识。

输入：

```yaml
task:

type:

bug


target:

CustomerList.vue


domain:

customer

```

输出：

相关知识：

```text
Feature:

customer-management


Bug:

BUG-001


Decision:

ADR-012


Domain:

customer.yaml

```

---

# 6.4 Retrieval Strategy

采用三层检索。

## Layer 1：Explicit Retrieval

最高优先。

依据：

* feature id；
* bug id；
* file path；
* route；
* symbol。

---

## Layer 2：Structural Retrieval

依据：

代码关系。

例如：

```text

CustomerList.vue

↓

useCustomerList

↓

customerApi

↓

customer-domain

```

---

## Layer 3：Semantic Retrieval

未来支持：

* Embedding；
* Vector Search。

MVP 不依赖。

---

# 6.5 Task Context Builder

Memory Router 返回的信息不能直接交给 Skill。

需要生成：

```text
runtime/task-context.yaml

```

作为 Agent 工作上下文。

示例：

```yaml

task:


type:

bug



goal:

修复客户列表分页问题



constraints:


- 不修改公共Table组件



affectedEntities:


feature:

customer-management


bugs:

BUG-003



files:


- CustomerList.vue



rules:


- filter change resets page



nonGoals:


- 不进行组件重构

```

---

# 7. Knowledge Storage

目录：

```text
docs/frontend-ai/


memory/


├── project/

├── domain/

├── feature/

├── bug/

├── change/

├── decision/

├── schema/

└── index/

```

---

# 8. Project Memory

## 职责

记录工程事实。

目录：

```text
memory/project/

```

---

## 文件

### project-context.yaml

描述：

项目是什么。

例如：

```yaml

framework:

 Vue3


language:

 TypeScript


build:

 Vite


ui:

 ElementPlus


state:

 Pinia

```

---

### architecture-map.yaml

描述：

架构结构。

例如：

```yaml

layers:


view:

 src/views


api:

 src/api


component:

 src/components


store:

 src/store

```

---

### constitution.yaml

新增。

描述：

项目必须遵守的规则。

例如：

```yaml

architecture:


api:

must_use_service_layer:true


state:


page_state:

use_composable


component:


reuse_existing:true

```

---

# 9. Domain Memory

## 职责

业务知识。

目录：

```text
memory/domain/

```

例如：

```text
customer.yaml

permission.yaml

billing.yaml

```

---

示例：

```yaml

entity:

Customer:



status:


ACTIVE:

正常客户


LOCKED:

锁定客户



rules:


locked_customer:


cannot_edit:true

```

---

# 10. Engineering Entity System

统一工程对象模型。

```text

Engineering Entity


├── Feature

├── Bug

├── Change

├── Decision

└── Component(optional)


```

---

# 11. Feature Entity

描述：

功能生命周期。

目录：

```text
memory/feature/

customer-management/

```

结构：

```text
feature.yaml

contract.yaml

implementation.yaml

history.yaml

```

---

示例：

```yaml

feature:


id:

customer-management



domain:

customer



status:

released



requirements:


ui:


api:


interaction:


files:


history:

```

---

# 12. Bug Entity

描述：

Bug 生命周期。

目录：

```text
memory/bug/

BUG-001/

```

---

结构：

```text

bug.yaml

analysis.yaml

fix.yaml

history.yaml

```

---

示例：

```yaml

bug:


id:

BUG-001



title:

分页错误



relatedFeature:

customer-management



rootCause:


type:

logic-error



fix:


files:


- CustomerList.vue



decision:


filter-reset-page

```

---

# 13. Change Entity

新增核心对象。

原因：

Feature/Bug描述结果。

Change描述：

> 一次工程变化。

---

示例：

```yaml

change:


id:

CHG-001



type:

bug-fix



source:

git



commit:

a81bc



files:


- CustomerList.vue



related:


bug:

BUG-001



description:

reset page after filter change

```

---

关系：

```text

Feature

   │

   │

 Change

   │

 ├── Bug

 └── Decision


```

---

# 14. Decision Entity

记录：

为什么这么设计。

目录：

```text
memory/decision/

```

示例：

ADR：

```markdown

# ADR-012


## Context

列表页面状态管理问题。


## Decision

使用Composable。


## Reason

页面生命周期短。


```

---

# 15. Component Knowledge

MVP：

作为 Project Index。

未来升级：

Component Entity。

记录：

* 组件用途；
* 使用位置；
* Props；
* Owner；
* 历史。

---

# 16. Memory Governance

所有 Memory Entity 必须包含：

```yaml

metadata:


source:


- human

- ai

- git

- inferred



confidence:


high



lastVerified:


2026-08-01



verifiedBy:

human

```

---

目的：

避免：

错误知识长期污染 Agent。

---

# 17. Development Pipeline

保持四个 Skill。

---

# Skill 1：frontend-analysis

职责：

理解变化。

支持：

* Feature；
* Bug；
* Refactor。

输入：

```text
Task Context

+

Human-provided Prototype

+

Click / Action Interaction Effects

```

输出：

```text
Change Contract

```

---

分析：

* 需求；
* 原型页面、Frame、Node 或标注区域；
* 每个受影响点击或动作的结果；
* loading、success、failure、disabled、permission、validation、cancel/back 等状态；
* API；
* UI；
* 代码影响；
* 历史知识；
* 风险。

强制门槛：

```text
USER_FACING
    ↓
用户提供可检查原型？ ── 否 ──> DRAFT + BLOCKED
    ↓ 是
用户提供完整点击结果？ ── 否 ──> DRAFT + BLOCKED
    ↓ 是
Change Contract READY
    ↓
Analysis Approval Gate
```

纯内部重构只有在能够证明 UI 与交互完全不变时，才允许记录 `uiImpact: NONE`，并必须提供不需要原型的理由和 UI invariant 证据。

---

# Skill 2：frontend-design

职责：

技术方案。

输入：

```text
Change Contract

```

输出：

```text
Implementation Plan

```

包含：

* 文件；
* 组件；
* API；
* 状态；
* 测试；
* 风险。

---

# Skill 3：frontend-implementation

职责：

执行修改。

流程：

```text

检查Git


↓

识别用户修改


↓

生成Patch Proposal


↓

Apply Patch


↓

测试


↓

生成Change Entity


```

---

## Patch Strategy

禁止：

```text
LLM直接修改文件

```

采用：

```text

Plan

↓

Patch

↓

Diff Review

↓

Apply

```

---

# Skill 4：frontend-review

职责：

最终验证。

检查：

## 需求

是否完成。

## Bug

是否解决。

## Regression

是否影响已有功能。

## Architecture

是否违反 Constitution。

## Memory

是否需要更新。

---

# 18. Human Approval Gate

必须存在。

流程：

```text

Analysis


↓

Feature/Bug Contract


↓

Human Approval


↓

Design


↓

Implementation


```

原因：

业务理解错误比代码错误更危险。

---

# 19. Memory Sync Service

负责：

代码变化 → 工程知识。

流程：

```text

Git Commit


↓

Diff Analyzer


↓

Change Entity


↓

Memory Update Proposal


↓

Human Confirm


↓

Persist


```

---

# 20. 用户手动修改处理

流程：

```text

User Change


↓

Git Diff


↓

Memory Sync


↓

Detect


↓

Generate Proposal


↓

Human Confirm


↓

Update Knowledge

```

---

不会自动相信：

代码变化。

因为：

代码变化 ≠ 业务变化。

---

# 21. Schema 管理

目录：

```text
memory/schema/


feature.schema.yaml

bug.schema.yaml

change.schema.yaml

decision.schema.yaml

```

作用：

保证 Memory 格式稳定。

---

# 22. Repository 结构

```text
docs/frontend-ai/


├── memory/


│
├── runtime/


│
├── features/


│
├── bugs/


│
├── changes/


│
├── decisions/


│
├── reports/


└── schema/


```

---

# 23. MVP 实施路线

## Phase 1：知识基础

实现：

* Project Memory
* Feature Entity
* Bug Entity
* Decision Entity
* Change Entity
* Schema
* Memory Router
* Task Context

目标：

让 AI 理解项目。

---

## Phase 2：开发能力

增加：

* Analysis Skill
* Design Skill
* Implementation Skill
* Review Skill
* Human Gate

---

## Phase 3：自动演进

增加：

* Git Analyzer
* Memory Sync
* Architecture Drift Detection
* Semantic Retrieval

---

# 24. 最终定位

该 Plugin 不再是：

```text
AI Coding Assistant
```

而是：

```text
Frontend Engineering Knowledge Operating System
```

它管理：

```text
项目状态

+

业务知识

+

功能历史

+

Bug历史

+

工程决策

+

代码演进

```

最终目标：

让 AI 从：

```text
第一次进入项目的新开发者
```

逐渐成为：

```text
长期维护该项目的高级前端工程师
```

---

# 核心原则总结

1. **Memory 是知识，不是文件。**
2. **Memory 必须有可信度。**
3. **Feature、Bug、Change 都是一等实体。**
4. **代码变化必须转换成工程意义。**
5. **Agent 不应该全量读取项目，而应该检索上下文。**
6. **AI 可以提出修改，但关键节点必须人工确认。**
7. **项目演进历史必须成为下一次开发上下文的一部分。**

这就是最终版 Frontend Engineering Knowledge Agent Plugin 架构。
