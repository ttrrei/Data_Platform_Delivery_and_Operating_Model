# Data Platform Delivery & Operating Model

> 一个企业数据平台如何被 **创建、交付、迁移、运营和持续管理** 的完整 lifecycle 框架。
> A complete lifecycle framework for how an enterprise data platform is **built, delivered, migrated, operated, and continuously governed.**

[![Layer](https://img.shields.io/badge/layer-L1%20technology--agnostic-blue)]()
[![Status](https://img.shields.io/badge/CN-in%20progress-yellow)]()
[![Status](https://img.shields.io/badge/EN-pending%20translation-lightgrey)]()

---

## 这是什么 / What is this

这是一套 **technology-agnostic（技术无关）** 的顶层方法论文档（L1），回答一个问题：

> **不管底层用什么技术（Snowflake / Databricks / BigQuery …），一个企业数据平台如何从「为什么建」走到「如何长期健康地活下去」。**

它**不是**某个平台的架构蓝图。平台特定的「怎么设计、怎么写 SQL/Spark」属于各 L2 Playbook（独立 repo）。本文档负责 **lifecycle 与横切方法论**，平台选型只是其中 Section 2 的一个输入变量。

This is a **technology-agnostic** top-level methodology document (L1). It is **not** an architecture blueprint for any single platform — platform-specific design lives in the L2 Playbooks (separate repos). This document owns the **lifecycle and the cross-cutting methodology**.

---

## 语言版本 / Language Versions

| 语言 | 入口 | 状态 |
|---|---|---|
| 🇨🇳 中文（主） | [`docs/cn/README.md`](docs/cn/README.md) | 🚧 进行中（权威源） |
| 🇬🇧 English | [`docs/en/README.md`](docs/en/README.md) | ⬜ 待翻译（CN 定稿后产出） |

> **写作约定**：先完成中文版作为权威源（single source of truth），全文定稿后统一翻译为英文版。两版本结构、锚点（slug）保持一致，便于 L2 跨语言引用。

---

## 文档体系：三层结构 / Three-Layer Architecture

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

## 章节地图 / Section Map

| # | Section | 角色 | CN | EN |
|---|---|---|---|---|
| 0 | What This Document Is | Portfolio 宪法 | ✅ Draft | ⬜ |
| 1 | Strategic Alignment & Discovery | L1 正文起点 | ✅ Draft | ⬜ |
| 2 | Platform Selection & Architecture Decision Framework | **枢纽 / 路由器** | ✅ Draft | ⬜ |
| 3 | Data Modeling & Governance-as-Code | L3 横切 #1 | ✅ Draft | ⬜ |
| 4 | Ingestion & Pipeline Design | L3 横切 #2 | ✅ Draft | ⬜ |
| 5 | Migration & Greenfield Strategy | L3 横切 #3 | ✅ Draft | ⬜ |
| 6 | Team Topology & Operating Structure | L3 横切 #4 | ✅ Draft | ⬜ |
| 7 | Day-2 Operations & Platform Governance | L3 横切 #5 | ✅ Draft | ⬜ |

---

## 仓库结构 / Repository Layout

```text
.
├── README.md                       ← 本文件（总体说明 / master index）
├── TASK_BRIEF.md                   ← 章节产出规划（写作 SOP）
├── CONTRIBUTING.md                 ← 贡献指南（锚点纪律 / 三规则 / 风格）
├── CHANGELOG.md                    ← 变更记录（Keep a Changelog / SemVer）
├── .github/                        ← CODEOWNERS · issue/PR 模板 · docs-integrity CI
├── scripts/
│   └── check_anchors.py            ← docs-integrity 检查器（纯标准库，离线）
└── docs/
    ├── cn/                         ← 中文版（权威源）
    │   ├── README.md               ← L1 中文入口
    │   ├── anchors.md              ← 锚点清单（供 L2 引用）
    │   └── sections/
    │       ├── 00-what-this-document-is.md
    │       ├── 01-strategic-alignment.md
    │       ├── 02-platform-selection.md      ← 枢纽
    │       ├── 03-modeling-governance.md
    │       ├── 04-ingestion-pipeline.md
    │       ├── 05-migration-greenfield.md
    │       ├── 06-team-topology.md
    │       └── 07-day2-operations.md
    └── en/                         ← English（待翻译，结构与 cn 镜像）
        ├── README.md
        └── sections/
            └── 00–07 (placeholders)
```

---

## 如何使用 / How to Use

- **理解整体方法论 / 推动新平台 0→1**：进入 [中文版](docs/cn/README.md)，从 Section 1 顺序读到 Section 7。
- **已知用哪个平台，只看架构设计**：读 Section 2 末尾的「分发映射」，跳到对应 L2 Playbook。
- **写 / 维护某个 L2 文档**：先读 Section 3/4（横切方法论）——那是不应重复、只应引用的内容；引用锚点见 [`docs/cn/anchors.md`](docs/cn/anchors.md)。

---

## 贡献与变更 / Contributing & Changelog

- 贡献指南（锚点纪律、三条规则、风格约定）/ Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- 变更记录（Keep a Changelog / SemVer）/ Changelog: [`CHANGELOG.md`](CHANGELOG.md)

---

## License

© 2026 Xing Lu. All rights reserved.

保留所有权利。未经作者书面授权，不得转载、演绎或用于商业用途。
Reproduction, adaptation, or commercial use of this documentation without written permission is prohibited.
