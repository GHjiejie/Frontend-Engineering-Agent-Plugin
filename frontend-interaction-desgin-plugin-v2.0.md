# Frontend Interaction & Development Design Plugin 架构设计方案（V2）

## 1. Plugin概述

## 1.1 Plugin名称

```text
frontend-interaction-design-plugin
```

---

## 1.2 Plugin定位

该 Plugin 用于将：

* 产品 PRD
* 前端原型（Figma / Axure / 图片）
* 后端接口 PRD / OpenAPI

转换为：

> 前端开发人员可评审、可实现的交互设计与开发方案。

核心目标：

解决：

```
产品需求
    ↓
前端理解
    ↓
交互设计
    ↓
开发方案
    ↓
代码实现
```

之间的信息断层。

---

# 2. 核心设计原则

## 2.1 禁止 AI 自行补全业务决策

这是 V2 最大改进。

规则：

> 当 PRD、原型、API 存在冲突、缺失或歧义时，AI 必须暂停生成，并主动向用户提出澄清问题。

禁止：

* 自己猜交互
* 自己选择接口
* 自己决定业务规则

---

例如：

PRD：

> 点击新增用户

原型：

有新增按钮

API：

提供：

```
POST /users
```

但是不知道：

新增是：

* 弹窗
* 新页面
* Drawer

AI必须询问：

```
点击新增用户后的交互形式是什么？

A. 弹窗
B. 独立页面
C. Drawer
D. 其他
```

---

# 3. 整体架构

新版流程：

```text
                    输入


             Product PRD

                  +

              Prototype

                  +

            Backend API



                    |

                    v


        Requirement Clarification Skill


                    |

          +---------+---------+

          |                   |

          |                   |

       无歧义              存在歧义


          |                   |

          |                   |

          v                   v


  Interaction Generator    clarification.md


          |                   |

          |              等待用户确认

          |                   |

          +---------<---------+


                    |

                    v


          User Flow Generator


                    |

                    v


        State Machine Generator


                    |

                    v


      Sequence Diagram Generator


                    |

                    v


     Frontend Development Plan Generator


                    |

                    v


          Frontend Design Docs

```

---

# 4. Plugin目录结构

```text
frontend-interaction-design-plugin/


├── plugin.yaml
│
├── README.md
│
└── skills/
│
│
├── requirement-clarification-generator/
│
│   ├── SKILL.md
│   ├── prompt.md
│   └── examples/
│
│
├── user-flow-generator/
│
│   ├── SKILL.md
│   ├── prompt.md
│   └── examples/
│
│
├── state-machine-generator/
│
│   ├── SKILL.md
│   ├── prompt.md
│   └── examples/
│
│
├── sequence-diagram-generator/
│
│   ├── SKILL.md
│   ├── prompt.md
│   └── examples/
│
│
└── frontend-plan-generator/
│
    ├── SKILL.md
    ├── prompt.md
    └── examples/

```

---

# 5. Skill设计

---

# Skill 1：Requirement Clarification Generator

## 职责

分析输入资料：

* PRD
* 原型
* API

发现：

* 冲突
* 缺失
* 不确定行为

---

## 输入

```text
product-prd

prototype

backend-api

```

---

## 检查内容

## 1. 原型与PRD冲突

例如：

PRD：

```
删除用户
```

原型：

```
批量删除按钮
```

问题：

```
是否支持批量删除？
```

---

## 2. 原型与API冲突

例如：

页面：

```
批量导入
```

API：

只有：

```
POST /user
```

问题：

```
是否需要新增批量导入接口？
```

---

## 3. 业务规则缺失

例如：

删除：

不知道：

* 是否二次确认
* 是否权限控制

---

## 输出

如果存在问题：

生成：

```
frontend-design/{feature-name}/clarification.md
```

例如：

```markdown
# Requirement Clarification


## Question 1

场景:

页面存在批量删除按钮


问题:

当前API只支持单个删除


请确认:

A. 前端循环调用

B. 后端增加批量接口

C. 删除功能暂不支持


Status:

Waiting Confirmation

```

---

# Skill 2：User Flow Generator

## 职责

生成：

> 用户操作流程

---

## 输入

```
PRD

Prototype

clarification结果

```

---

## 输出

```
frontend-design/{feature-name}/user-flow.md
```

内容：

```markdown
用户进入客户管理

↓

点击新增

↓

打开弹窗

↓

填写信息

↓

提交

↓

成功

```

包含：

Mermaid Flowchart。

---

# Skill 3：State Machine Generator

## 职责

生成：

> 页面状态模型

---

## 输入：

```
user-flow

prototype

```

---

## 输出：

```
state-machine.md
```

---

内容：

包括：

页面状态：

```
loading

empty

data

error

```

组件状态：

```
dialog

closed

opened

submitting

success

failed

```

---

# Skill 4：Sequence Diagram Generator

## 职责：

生成：

> 前后端调用时序

---

## 输入：

```
user-flow

state-machine

backend-api

```

---

## 输出：

```
sequence-diagram.md
```

包含：

Mermaid Sequence Diagram。

---

# Skill 5：Frontend Development Plan Generator

## 职责：

生成：

> 前端开发实施方案

---

## 输入：

```
PRD

Prototype

API


+

user-flow

state-machine

sequence-diagram

```

---

## 输出：

```
frontend-development-plan.md
```

---

# 内容结构

## 1. 功能概述

```markdown
实现客户管理功能：

- 查询客户
- 创建客户
- 删除客户

```

---

## 2. 页面结构

```text
CustomerPage

├── Search

├── Table

├── CreateDialog

└── DeleteConfirm

```

---

## 3. 状态设计

```ts
CustomerState

{
 loading

 data

 selectedCustomer

 error
}

```

---

## 4. API使用方案

```
页面加载

GET /customers


新增

POST /customers


删除

DELETE /customers/{id}

```

---

## 5. 异常处理

```
网络错误

权限不足

空数据

提交失败

```

---

## 6. 开发任务拆分

```
页面结构

API封装

列表开发

弹窗开发

联调

```

---

# 6. 最终输出目录结构

例如功能：

```
客户管理
```

生成：

```text
frontend-design/


└── customer-management/


    ├── clarification.md


    ├── user-flow.md


    ├── state-machine.md


    ├── sequence-diagram.md


    └── frontend-development-plan.md

```

---

# 7. Skill执行依赖关系

```text

                  PRD

                   |

              Prototype

                   |

              Backend API


                   |

                   v


   Requirement Clarification Generator


                   |

        +----------+----------+

        |                     |

        |                     |

     有问题                 无问题


        |                     |

        v                     v


 clarification.md        User Flow Generator


        |                     |

        |                     v

        |             State Machine Generator

        |                     |

        |                     v

        |           Sequence Diagram Generator

        |                     |

        +----------> Frontend Plan Generator


```

---

# 8. 最终Plugin能力模型

```text
Frontend Interaction Design Plugin


输入:

PRD
Prototype
API


能力:


1. 需求一致性检查

        ↓

2. 用户流程建模

        ↓

3. 页面状态建模

        ↓

4. 前后端时序建模

        ↓

5. 前端开发方案生成


输出:

Frontend Design Package

```

---

# 9. 核心价值

这个 Plugin 最终不是一个“画图工具”。

它解决的是：

> 在 AI 生成代码之前，让 AI 和开发者先完成一次类似真实技术评审的过程。

最终流程：

```text
产品提出需求

        ↓

AI分析

        ↓

发现疑问

        ↓

开发者确认

        ↓

生成交互模型

        ↓

生成开发方案

        ↓

进入Coding Agent

```

这个版本比 V1 更接近真实企业研发流程，因为它增加了最关键的工程能力：

**不确定性管理（Uncertainty Management）。**
