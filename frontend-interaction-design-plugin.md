# Frontend Interaction & Development Design Plugin 架构设计文档

## 1. Plugin概述

### 1.1 Plugin名称

```
frontend-interaction-design-plugin
```

---

## 1.2 Plugin定位

该 Plugin 用于将：

* 产品 PRD
* 前端原型设计（Figma / Axure / 图片）
* 后端 API PRD / OpenAPI

转换为：

> 面向前端开发人员的交互设计与开发方案文档。

核心目标：

**解决产品需求到前端实现之间的信息断层。**

---

## 1.3 Plugin职责范围

### 负责：

✅ 分析产品需求
✅ 分析页面交互
✅ 分析接口调用关系
✅ 生成前端交互模型
✅ 生成前端开发方案

### 不负责：

❌ 自动生成代码
❌ 修改代码仓库
❌ 自动创建组件
❌ 自动提交 PR

代码生成属于后续 Coding Agent。

---

# 2. 整体工作流

整体流程：

```
                 Product PRD

                      |

                      |

                 Prototype

                      |

                      |

              Backend API PRD


                      |

                      v


        Frontend Interaction Plugin


                      |

        +-------------+-------------+

        |             |             |

        v             v             v


   User Flow    State Machine   Sequence Diagram


        |             |             |

        +-------------+-------------+

                      |

                      v


          Frontend Development Plan


                      |

                      v


             Frontend Review


                      |

                      v


             Code Implementation

```

---

# 3. Plugin架构

## 3.1 Plugin目录结构

```
frontend-interaction-design-plugin/


├── plugin.yaml
│
├── README.md
│
└── skills/
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

# 4. Skill设计

---

# Skill 1：User Flow Generator

## 4.1 职责

根据：

* 产品 PRD
* 原型

生成：

> 用户操作流程图。

---

## 4.2 输入

```
product-prd

prototype

```

---

## 4.3 分析内容

识别：

### 页面

例如：

```
客户管理页面

```

### 可交互元素

例如：

```
新增按钮

搜索框

删除按钮

```

### 用户动作

例如：

```
click

input

submit

confirm

cancel

```

---

## 4.4 输出

文件：

```
frontend-design/{feature-name}/user-flow.md

```

内容：

```markdown
# 用户流程


进入客户管理页面

↓

点击新增按钮

↓

打开创建客户弹窗

↓

填写信息

↓

提交

↓

创建成功


```

包含：

Mermaid Flowchart。

---

# Skill 2：State Machine Generator

## 4.5 职责

根据：

* User Flow
* 原型

生成：

> 页面状态模型。

---

## 4.6 输入

```
user-flow.md

prototype

```

---

## 4.7 分析内容

识别：

页面状态：

```
idle

loading

empty

success

error

```

组件状态：

```
dialog:

closed

opened

submitting

success

failed

```

---

## 4.8 输出

文件：

```
frontend-design/{feature-name}/state-machine.md

```

内容：

```markdown
# 页面状态


Customer List


idle

↓

loading

↓

data


data

↓

delete


delete

↓

success/error


```

包含：

Mermaid State Diagram。

---

# Skill 3：Sequence Diagram Generator

## 4.9 职责

根据：

* User Flow
* State Machine
* Backend API PRD

生成：

> 前后端交互时序图。

---

## 4.10 输入

```
user-flow.md

state-machine.md

backend-api

```

---

## 4.11 分析内容

确定：

* 哪个操作调用接口
* 请求参数
* 返回结果
* 页面状态变化

---

## 4.12 输出

文件：

```
frontend-design/{feature-name}/sequence-diagram.md

```

内容：

```mermaid
sequenceDiagram

User->>Browser:
点击提交

Browser->>Backend:
POST /customer

Backend->>DB:
insert

DB-->>Backend:
success

Backend-->>Browser:
success

Browser->>Browser:
refresh

```

---

# Skill 4：Frontend Development Plan Generator

## 4.13 职责

根据：

* PRD
* 原型
* API
* 三个图

生成：

> 前端开发实施方案。

---

## 4.14 输入

```
product-prd

prototype

backend-api

user-flow

state-machine

sequence-diagram

```

---

## 4.15 输出

文件：

```
frontend-design/{feature-name}/frontend-development-plan.md

```

---

# 输出内容设计

## 1. 功能概述

例如：

```
客户管理功能支持：

- 客户列表查询
- 新增客户
- 删除客户

```

---

## 2. 页面设计

例如：

```
CustomerPage


├── SearchArea

├── CustomerTable

├── CustomerDialog

└── DeleteDialog

```

---

## 3. 状态设计

例如：

```
CustomerListState


loading

customers

error

selectedCustomer

```

---

## 4. API调用方案

例如：

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

例如：

```
接口失败

空数据

权限不足

提交失败

```

---

## 6. 开发任务拆分

例如：

```
Task1:

页面结构


Task2:

API封装


Task3:

列表实现


Task4:

新增弹窗


Task5:

联调

```

---

# 5. 最终生成文件结构

假设功能：

```
客户管理

```

生成：

```
frontend-design/


└── customer-management/


    ├── user-flow.md


    ├── state-machine.md


    ├── sequence-diagram.md


    └── frontend-development-plan.md

```

---

# 6. Skill执行顺序

严格Pipeline：

```
                 PRD

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


    Frontend Plan Generator


                  |

                  v


        Frontend Design Docs

```

---

# 7. 设计原则

## 7.1 单一职责

每个 Skill：

只负责一种产物。

---

## 7.2 文档驱动

所有结果：

Markdown保存。

方便：

* Review
* 修改
* Git管理

---

## 7.3 功能隔离

目录以业务功能划分：

正确：

```
customer-management/

```

错误：

```
user-flow/

```

---

## 7.4 人机协作

AI负责：

* 分析
* 推理
* 生成方案

开发者负责：

* Review
* 修改
* 确认

---

# 8. Plugin最终定位

```
             Product Team


                  |

                  |

              PRD + UI


                  |

                  v


=================================

Frontend Interaction Design Plugin

=================================


                  |

                  v


     Interaction Model


     - User Flow

     - State Machine

     - Sequence Diagram



                  |

                  v


     Frontend Development Plan



                  |

                  v


           Coding Agent


                  |

                  v


              Source Code

```

---

# 总结

最终版本：

| 项目      | 设计                                 |
| ------- | ---------------------------------- |
| Plugin  | frontend-interaction-design-plugin |
| Skill数量 | 4个                                 |
| 核心产物    | 4个Markdown文档                       |
| 输入      | PRD + 原型 + API                     |
| 输出目录    | frontend-design/{feature-name}/    |
| 核心价值    | 将产品需求转换成前端可执行方案                    |

这个版本的边界和职责比较清晰：
**前三个 Skill 负责“理解和建模”，第四个 Skill 负责“形成开发方案”。**
后续无论接代码生成 Agent、测试 Agent，还是 Review Agent，都可以直接消费这个 Plugin 的输出。
