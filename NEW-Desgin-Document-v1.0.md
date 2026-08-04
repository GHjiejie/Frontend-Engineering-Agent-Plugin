下面我按照一个**可落地实现的 Claude Code / Codex Plugin 架构**来设计。

这个 Plugin 的目标不是直接写代码，而是：

> 将「产品需求 → 前端需求规格 → UI交互 → API绑定 → 技术方案 → 开发文档」自动化。

因此它应该是一个**多阶段 Agent Pipeline**。

---

# 一、Plugin 总体架构

```text
┌─────────────────────────────────────────────┐
│          Frontend Spec Generator Plugin      │
└─────────────────────────────────────────────┘


                 用户输入
                    |
                    |
        ┌───────────▼───────────┐
        │   Project Context      │
        │   项目上下文采集        │
        └───────────┬───────────┘
                    |
                    |
                    v


        ┌───────────────────────┐
        │ Skill 1               │
        │ Requirement Analyzer  │
        │ 需求分析器             │
        └───────────┬───────────┘
                    |
                    v


        ┌───────────────────────┐
        │ Skill 2               │
        │ Requirement Clarifier │
        │ 需求澄清器             │
        └───────────┬───────────┘
                    |
                    |
          PRD确认完成
                    |
                    v


        ┌───────────────────────┐
        │ Skill 3               │
        │ API Analyzer          │
        │ 接口分析器             │
        └───────────┬───────────┘
                    |
                    v


        ┌───────────────────────┐
        │ Skill 4               │
        │ UI Prototype Parser   │
        │ 原型解析器             │
        └───────────┬───────────┘
                    |
                    |
                    v


        ┌───────────────────────┐
        │ Skill 5               │
        │ Interaction Designer  │
        │ 交互设计器             │
        └───────────┬───────────┘
                    |
                    |
                    v


        ┌───────────────────────┐
        │ Skill 6               │
        │ Flow Generator        │
        │ 流程/时序生成器        │
        └───────────┬───────────┘
                    |
                    |
                    v


        ┌───────────────────────┐
        │ Skill 7               │
        │ Frontend Spec Writer  │
        │ 开发规格文档生成       │
        └───────────┬───────────┘
                    |
                    |
                    v


        ┌───────────────────────┐
        │ Skill 8               │
        │ Change Tracker        │
        │ 变更记录               │
        └───────────────────────┘

```

---

# 二、Plugin目录结构

建议：

```
frontend-spec-plugin/


├── plugin.json


├── skills/

│
├── project-context-loader/

│   └── SKILL.md
│
├── requirement-analyzer/

│   └── SKILL.md
│
├── requirement-clarifier/

│   └── SKILL.md
│
├── api-analyzer/

│   └── SKILL.md
│
├── ui-parser/

│   └── SKILL.md
│
├── interaction-designer/

│   └── SKILL.md
│
├── flow-generator/

│   └── SKILL.md
│
├── frontend-spec-generator/

│   └── SKILL.md
│
└── change-tracker/

    └── SKILL.md



├── templates/


├── schemas/


└── docs/

    ├── architecture.md

    └── workflow.md

```

---

# 三、各 Skill 职责设计

---

# Skill 1：project-context-loader

## 名称

项目上下文加载器

## 输入

开发项目：

```
console-ui
```

读取：

```
package.json

vite.config.ts

src目录

AGENTS.md

README.md

API目录

components目录

```

---

## 输出

```
project-context.json
```

例如：

```json
{
 "framework":"Vue3",

 "language":"typescript",

 "ui":"Element Plus",

 "state":"Pinia",

 "style":"scss",

 "rules":[
   "禁止any",
   "script setup"
 ]
}
```

---

## 作用

保证后续生成方案符合项目。

---

# Skill 2：requirement-analyzer

## 作用

理解PRD。

输入：

```
*.md
*.docx
产品文档
```

---

分析：

## 页面

例如：

```
客户管理

 ├ 客户列表

 ├ 客户组

 └ 客户详情

```

## 功能点

例如：

```
新增客户组

删除客户组

搜索客户

分页查询

```

---

输出：

```
requirement-analysis.json
```

结构：

```json
{

page:"customer-group",

features:[

{
name:"create",

actor:"user",

action:"create group"

}

]

}

```

---

# Skill 3：requirement-clarifier

## 作用

发现PRD缺陷。

例如：

PRD:

> 删除客户

模型发现：

```
问题:

1. 是否需要确认？

2. 删除失败如何处理？

3. 删除后列表是否刷新？

4. 是否需要权限判断？

```

输出：

```
question-list.md
```

---

开发者回答：

保存：

```
decision-log.md

```

这个文件非常重要。

---

# Skill 4：api-analyzer

## 作用

理解后端能力。

输入：

```
openapi.yaml

swagger.json

proto

```

输出：

```
api-map.json
```

例如：

```json
{
"createCustomerGroup":{

method:"POST",

path:"/groups"

}

}

```

---

同时生成：

```
request-response.md
```

包含：

请求字段：

响应字段：

错误码：

---

# Skill 5：ui-parser

## 作用

理解UI。

输入：

```
Figma

截图

Axure

HTML
```

输出：

```
ui-tree.json
```

例如：

```json
{

page:"CustomerGroup",

components:[


{
type:"button",

name:"新增"

},


{
type:"table",

columns:[

"name",

"status"

]

}


]

}

```

---

识别：

* Button
* Input
* Select
* Table
* Dialog
* Tabs

---

# Skill 6：interaction-designer

这是核心Skill。

负责：

```
UI元素

+

用户动作

+

API

+

状态变化

```

组合。

---

例如：

输入：

```
按钮:

新增客户组


接口:

POST /groups

```

输出：

```
交互流程:

1.
点击按钮

2.
打开Dialog

3.
输入名称

4.
提交

5.
调用API

6.
成功关闭

7.
刷新列表


```

---

生成：

```
interaction-spec.json

```

结构：

```json
{

element:"create-button",

event:"click",

actions:[

"open-dialog",

"submit-form",

"call-api"

]

}

```

---

# Skill 7：flow-generator

负责生成：

## 时序图

例如：

```mermaid

sequenceDiagram

User->>Vue:
click button

Vue->>API:
POST

API->>Backend:
create


Backend-->>API:
success


API-->>Vue:
result


Vue:
refresh table


```

---

同时生成：

## 状态机

例如：

```
列表页面


loading

 |

success

 |

empty

 |

error

```

---

# Skill 8：frontend-spec-generator

最终文档生成。

输出：

```
docs/frontend-spec/customer-group.md
```

模板：

```markdown
# 客户组管理


## 页面说明


## UI结构


## 数据模型


## API


## 页面状态


## 用户交互


### 新增


流程:

xxx


接口:

POST /groups


时序图:


```

## 前端实现方案

组件:

CustomerGroup.vue

API:

customerGroup.ts

Store:

customerGroupStore.ts

```

---

# Skill 9：change-tracker

负责维护：

> 人工修改。


目录：

```

frontend-spec/

generated/

spec.md

manual/

override.md

history/

change-log.json

```


例如：

模型：

```

删除直接调用接口

```


开发：

修改：

```

删除前需要权限检查

````


记录：

```json
{
"time":

"2026-08-04",

"type":

"manual_override",

"section":

"delete-flow"

}

````

---

# 四、最终文件产物

一次完整执行后：

```
frontend-spec/


├── context/

│
├── project-context.json


├── requirement/

│
├── requirement-analysis.json

├── decision-log.md



├── api/

│
├── api-map.json



├── ui/

│
├── ui-tree.json



├── interaction/

│
├── interaction-spec.json



├── flow/

│
├── sequence-diagrams.md



└── document/


    └── frontend-development-spec.md

```

---

# 五、Skill执行顺序

实际运行：

```
init

↓

load-context

↓

analyze-prd

↓

ask-questions

↓

developer-confirm

↓

analyze-api

↓

analyze-ui

↓

design-interaction

↓

generate-flow

↓

generate-spec

↓

developer-start-coding

↓

track-changes

```

---

# 六、未来扩展

这个架构天然可以继续扩展：

## Skill 10：Code Generator

输入：

```
frontend-development-spec.md
```

输出：

```
Vue Component

API Service

Pinia Store

Typescript Type

```

---

## Skill 11：Test Generator

生成：

```
Playwright

Vitest

```

---

## Skill 12：Review Agent

开发完成后：

检查：

```
代码

是否符合spec

接口是否绑定正确

交互是否遗漏

```

---

所以最终这个 Plugin 实际上会演变成：

```
产品经理
    |
    v
PRD

    |
    v

Frontend Spec Agent

    |
    v

前端架构文档

    |
    v

Code Agent

    |
    v

Vue代码

    |
    v

Test Agent

```

这个拆分方式比较符合现在 AI Agent 工程化的设计思路：**每个 Skill 做一个明确职责，产生中间产物，避免一个大 Skill 里面上下文失控。**
