# Frontend Engineering Agent Plugin 架构设计文档（最终版）

版本：v1.0
定位：长期驻留型前端工程 Agent
目标：从“一次性代码生成”升级为“持续理解、持续演进、持续维护前端项目的工程代理”。

---

# 1. 产品定位

## 1.1 核心目标

该 Plugin 不只是帮助开发一个功能，而是帮助 AI 长期参与一个前端项目。

它需要具备：

* 理解项目当前状态；
* 理解项目历史演进；
* 理解业务领域知识；
* 根据需求生成 Feature；
* 根据 Feature 实施代码；
* 验证实现是否符合预期；
* 将新的知识沉淀回项目。

最终形成：

```
项目代码
    +
项目历史
    +
业务知识
    +
工程决策

        ↓

Frontend Engineering Knowledge Base

        ↓

AI持续参与项目开发
```

---

# 2. 核心设计理念

整个系统围绕四个核心对象：

```
Project Memory

        +

Domain Memory

        +

Feature Entity

        +

Execution Pipeline
```

---

# 3. 总体架构

```
                    User Request


                         |
                         |

              Frontend Engineering Agent


                         |

              ┌──────────────────┐
              │   Orchestrator   │
              └──────────────────┘


                         |


 ┌──────────────────────────────────────────┐
 │                                          │
 │              Knowledge Layer              │
 │                                          │
 │  Project Memory     Domain Memory        │
 │                                          │
 │  工程知识             业务知识            │
 │                                          │
 └──────────────────────────────────────────┘


                         |


 ┌──────────────────────────────────────────┐
 │                                          │
 │          Development Pipeline             │
 │                                          │
 │ Analysis                                 │
 │ Design                                   │
 │ Implementation                           │
 │ Review                                   │
 │                                          │
 └──────────────────────────────────────────┘


                         |


                Repository Update


                         |


                Memory Update

```

---

# 4. 核心模块划分

整个 Plugin 分为：

```
1. Orchestrator

2. Memory System

3. Domain System

4. Feature Lifecycle System

5. Development Skills

6. Maintenance System
```

---

# 5. Orchestrator

## 职责

负责整个流程调度。

它不负责：

* 分析代码；
* 写代码；
* 生成页面。

它只负责：

* 状态管理；
* Skill 调度；
* Gate 控制；
* Artifact 管理。

---

## 状态机

```
NEW


 ↓


CONTEXT_LOADING


 ↓


ANALYZING


 ↓


FEATURE_CONTRACT_READY


 ↓


DESIGN_READY


 ↓


IMPLEMENTING


 ↓


VERIFYING


 ↓


MEMORY_UPDATING


 ↓


COMPLETED

```

异常：

```
BLOCKED

CONFLICT

NEED_HUMAN_REVIEW

FAILED

```

---

# 6. Memory System（项目记忆系统）

## 定位

解决：

> AI 下一次进入项目时，不需要重新学习整个项目。

---

## 目录设计

```
docs/frontend-ai/


project-memory/


├── project-context.yaml

├── project-index.json

├── architecture-map.yaml

├── feature-registry.yaml

├── evolution-log.jsonl

├── decisions/

└── memory-index.json

```

---

# 6.1 project-context.yaml

## 职责

描述项目基础信息。

来源：

* package.json
* tsconfig
* vite.config
* AGENTS.md
* README

内容：

```yaml
framework:

 Vue3


language:

 TypeScript


ui:

 ElementPlus


state:

 Pinia


build:

 Vite


rules:

 component-first:
   true

 style-token:
   true

```

---

# 6.2 project-index.json

## 职责

项目索引。

记录：

* 页面；
* 路由；
* 组件；
* API；
* Store；
* Composable。

例如：

```json
{
 "routes":[
   "/customer"
 ],

 "components":[
   "BaseTable"
 ],

 "apis":[
   "customerApi"
 ]
}
```

用途：

快速定位代码。

---

# 6.3 architecture-map.yaml

## 职责

描述代码架构。

例如：

```yaml

layers:

view:

 src/views


component:

 src/components


api:

 src/api


state:

 src/store

```

用途：

避免 AI 随意创建代码结构。

---

# 6.4 evolution-log.jsonl

## 职责

记录项目演进。

区别：

Git：

```
改了什么代码
```

Evolution：

```
增加了什么能力
为什么增加
影响什么功能
```

例如：

```json
{
"type":

"feature-added",

"feature":

"customer-import",

"impact":

[
"customer-management"
]
}

```

---

# 6.5 Decision Memory

目录：

```
decisions/


ADR-001-api-layer.md

ADR-002-state-management.md

```

记录：

为什么这样设计。

例如：

```
为什么不用Pinia保存页面临时状态？

原因：

页面状态生命周期短。

决定：

使用Composable。

```

---

# 7. Domain Memory（业务知识）

## 目标

解决：

> AI懂代码，但是不懂业务。

目录：

```
domain-memory/


├── business-domain.yaml

├── entity-model.yaml

└── business-rule.yaml

```

---

例如：

customer.yaml

```yaml

entity:

 Customer:


status:


 ACTIVE:

  description:
   正常


 LOCKED:

  description:
   被锁定



rules:


locked:

 cannotEdit:
   true

```

---

# 8. Feature Lifecycle System

这是整个系统核心。

Feature 不再是一次任务。

而是一个长期存在的实体。

---

## Feature Entity

目录：

```
features/


customer-import/


feature.yaml

contract.yaml

implementation.yaml

history.yaml

```

---

结构：

```yaml

feature:


id:

 customer-import


domain:

 customer


status:

 released


createdAt:


updatedAt:


requirements:


ui:


api:


interaction:


implementation:


decisions:


history:


validation:

```

---

生命周期：

```
PROPOSED


 ↓


ANALYZING


 ↓


DESIGNED


 ↓


IMPLEMENTING


 ↓


RELEASED


 ↓


DEPRECATED

```

---

# 9. Skill 设计

保持 4 个 Skill。

不继续拆。

---

# Skill 1：frontend-analysis

## 定位

项目理解 + 需求分析。

这是核心 Skill。

---

流程：

```
Step 1

加载 Memory


Step 2

检测项目变化


Step 3

解析需求


Step 4

解析 API


Step 5

解析 UI


Step 6

分析交互


Step 7

匹配已有能力


Step 8

生成 Feature Contract

```

---

输出：

```
feature.yaml

feature-contract.yaml

risk-report.md

```

---

# Skill 2：frontend-design

## 定位

技术方案设计。

输入：

```
feature-contract.yaml
```

输出：

```
implementation-plan.yaml
```

---

负责：

* 页面拆分；
* 组件设计；
* API层设计；
* 状态设计；
* 测试设计。

---

# Skill 3：frontend-implementation

## 定位

代码执行。

流程：

```
检查Git状态

↓

检测用户修改

↓

执行Implementation Plan

↓

代码修改

↓

测试

↓

生成Change Log

↓

更新Memory

```

---

负责：

* Vue代码；
* TypeScript；
* API调用；
* 组件；
* 测试。

---

# Skill 4：frontend-review

## 定位

质量保证。

检查：

## Feature覆盖

需求是否完成。

---

## UI覆盖

原型是否实现。

---

## API覆盖

接口是否正确。

---

## Interaction覆盖

按钮：

```
点击

↓

调用接口

↓

成功

↓

失败

```

是否完整。

---

## Architecture检查

是否违反：

* 项目规范；
* 架构规则；
* Decision Memory。

---

输出：

```
review-report.md
```

---

# 10. Memory Maintainer（后续阶段）

不是第一版 Skill。

定位：

后台维护 Agent。

职责：

## 1. 自动发现变化

Git:

```
commit

↓

change analyzer

↓

evolution event

```

---

## 2. 架构漂移检测

例如：

发现：

```
src/api

出现大量直接axios

```

提示：

违反：

API Layer Decision。

---

## 3. 重复能力检测

发现：

```
CustomerTable.vue

CustomerListTable.vue

CustomerBaseTable.vue

```

提示：

组件重复。

---

# 11. Repository 文档结构

最终：

```
docs/frontend-ai/


├── project-memory/

│
├── domain-memory/

│
├── features/

│   └── customer-import/

│       ├── feature.yaml
│       ├── contract.yaml
│       ├── implementation.yaml
│       └── history.yaml


├── decisions/

│
└── reports/

```

---

# 12. 数据流

完整链路：

```
用户需求


    ↓


frontend-analysis


    ↓


Feature Entity


    ↓


Feature Contract


    ↓


frontend-design


    ↓


Implementation Plan


    ↓


frontend-implementation


    ↓


Code


    ↓


frontend-review


    ↓


Release


    ↓


Update Memory


    ↓


下一次迭代

```

---

# 13. 第一版本实现范围（MVP）

必须实现：

## Memory

✅ project-context
✅ project-index
✅ feature-registry
✅ evolution-log
✅ decisions

---

## Domain

✅ business-domain.yaml

---

## Feature

✅ Feature Entity
✅ Feature Contract

---

## Skills

✅ frontend-analysis
✅ frontend-design
✅ frontend-implementation
✅ frontend-review

---

暂不实现：

❌ Vector Database
❌ 自动后台扫描
❌ 架构漂移检测
❌ 自动重构建议

---

# 最终定位

这个 Plugin 最终不是：

```
AI帮你写Vue页面
```

而是：

```
一个长期驻留前端项目中的工程伙伴
```

它拥有：

```
工程记忆

+
业务记忆

+
功能生命周期

+
技术决策历史

+
代码执行能力

```

最终目标：

> 让 AI 从“第一次进入项目的新人”，逐渐成长为“熟悉这个项目的高级前端工程师”。
