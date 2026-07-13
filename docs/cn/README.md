# Data Platform Delivery & Operating Model — 中文版

> **L1 — Technology-agnostic 顶层框架**
> 一个企业数据平台如何被**创建、交付、迁移、运营和持续管理**的完整 lifecycle 框架。
>
> Status: 🚧 In Progress（权威源 / single source of truth） · Language: 中文叙述 + English terms（最终统一翻译为 EN 版）

← 返回总览：[`/README.md`](../../README.md) · English version: [`docs/en/README.md`](../en/README.md)

---

## 这是什么

这份文档回答一个问题：**不管底层用什么技术，一个企业数据平台如何从「为什么建」走到「如何长期健康地活下去」。**

它**不是**架构蓝图。某个平台「怎么设计」属于各 L2 Playbook 的职责。本文档负责 lifecycle 与方法论，平台选型只是 [Section 2](sections/02-platform-selection.md) 的一个输入变量。

| 这份文档回答 | 这份文档不回答 |
|---|---|
| 平台 lifecycle 怎么走 | 某个平台的具体架构怎么画 |
| 选型决策框架是什么 | 某个平台的 SQL / Spark 怎么写 |
| 横切方法论的权威定义 | 平台特定的实现细节 |

---

## 文档体系：三层结构

本文档是整套体系的 **L1**。L3 横切方法论**内嵌在本文档内**（方案 A），不单独成文。

```text
L1  Data Platform Delivery & Operating Model   ← 本 repo
      technology-agnostic 框架 + 横切方法论容器
      Section 2 = 选型分发路由器
         │
         │  跨 repo 外链分发
         ├──────────────────────┬──────────────────────┐
         ↓                      ↓                      ↓
L2  Snowflake              Databricks             BigQuery
    Lakehouse Playbook     AI/ML Playbook         Analytical Playbook
    (已有 · 独立 repo)     (待写 · 独立 repo)     (未来 · 可选)
    低复杂度近实时分析     AI + ML 为中心          GCP-native serverless
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                          ↓
L3  横切方法论 (内嵌于 L1 Section 3/4/5/6/7)
    Medallion · Governance-as-Code · Ingestion · Migration · Team · Day-2
    被所有 L2 引用，L2 不重复定义
```

---

## 核心原则（Portfolio Constitution）

整套体系长期可维护，靠三条强制规则（完整论述见 [Section 0](sections/00-what-this-document-is.md)）：

1. **L1 定义原则，L2 只写差异。** 任何 technology-agnostic 的方法论只在 L1 定义一次；L2 引用 L1，只补该平台的实现差异，不重讲原理。
2. **横切章节是唯一权威源（single source of truth）。** L1 与某 L2 表述冲突时，以 L1 为准。
3. **跨 repo 引用必须版本锚定。** L2 外链 L1 横切章节时，引用带版本 tag 的稳定锚点（如 `L1@v1.2#governance-as-code`），不链 main 浮动内容。锚点登记表见 [`anchors.md`](anchors.md)。

---

## 章节地图

| # | Section | 角色 | 状态 |
|---|---|---|---|
| 0 | [What This Document Is](sections/00-what-this-document-is.md) | Portfolio 宪法 | ✅ Draft |
| 1 | [Strategic Alignment & Discovery](sections/01-strategic-alignment.md) | L1 正文起点 | ✅ Draft |
| 2 | [Platform Selection & Architecture Decision Framework](sections/02-platform-selection.md) | **枢纽 / 路由器** | ✅ Draft |
| 3 | [Data Modeling & Governance-as-Code](sections/03-modeling-governance.md) | L3 横切 #1 | ✅ Draft |
| 4 | [Ingestion & Pipeline Design](sections/04-ingestion-pipeline.md) | L3 横切 #2 | ✅ Draft |
| 5 | [Migration & Greenfield Strategy](sections/05-migration-greenfield.md) | L3 横切 #3 | ✅ Draft |
| 6 | [Team Topology & Operating Structure](sections/06-team-topology.md) | L3 横切 #4 | ✅ Draft |
| 7 | [Day-2 Operations & Platform Governance](sections/07-day2-operations.md) | L3 横切 #5 | ✅ Draft |

---

## 如何使用

- **理解整体方法论 / 推动新平台 0→1**：从 Section 1 顺序读到 Section 7。
- **已知用哪个平台，只看架构设计**：直接跳对应 L2 Playbook（见 Section 2 末尾[分发映射](sections/02-platform-selection.md#distribution-mapping)）。
- **写 / 维护某个 L2 文档**：先读 Section 3/4（横切方法论），那是不应重复、只应引用的内容；引用锚点见 [`anchors.md`](anchors.md)。

---

## 贯穿全文的核心契约（Cross-Section Contracts）

| 契约对象 | 定义于 | 被引用于 |
|---|---|---|
| **Requirements Profile** | [Section 1](sections/01-strategic-alignment.md#requirements-profile) | Section 2（选型输入） |
| **Medallion 三层职责** | [Section 3](sections/03-modeling-governance.md#medallion) | Section 2 / 4 / 5 / 7 |
| **Governance-as-Code** | [Section 3](sections/03-modeling-governance.md#governance-as-code) | Section 2 / 5 / 7 |
| **Landing Layer** | [Section 4](sections/04-ingestion-pipeline.md#landing-layer) | Section 2 / 5 |
| **选型结论（Platform Decision Record）** | [Section 2](sections/02-platform-selection.md#platform-decision-record) | Section 6（团队能力矩阵） |
| **Value Heat Map** | [Section 7](sections/07-day2-operations.md#value-heat-map) | Section 5（MVP 首域选择） |

---

## Repo 结构

```text
docs/cn/
├── README.md                          ← 本文件（中文入口）
├── anchors.md                         ← 锚点清单（供 L2 引用）
└── sections/
    ├── 00-what-this-document-is.md    ✅ Portfolio 宪法
    ├── 01-strategic-alignment.md      ✅
    ├── 02-platform-selection.md       ✅ 枢纽
    ├── 03-modeling-governance.md      ✅
    ├── 04-ingestion-pipeline.md       ✅
    ├── 05-migration-greenfield.md     ✅
    ├── 06-team-topology.md            ✅
    └── 07-day2-operations.md          ✅
```
