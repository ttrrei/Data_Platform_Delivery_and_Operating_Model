# 锚点清单 / Anchor Registry

> 供 **L2 Playbook 跨 repo 引用** 的稳定锚点（slug）登记表。
>
> **规则**：
> 1. 每个锚点是 L1 横切方法论的稳定引用点。**改 slug = breaking change**，必须升版本 tag。
> 2. L2 引用格式：`L1@<version-tag>#<slug>`，例如 `L1@v1.2#governance-as-code`。**不要链 `main` 浮动内容。**
> 3. 新增锚点只能 append，不能复用已废弃的 slug。废弃锚点保留在「Deprecated」区并标注替代项。

当前版本：`v0.1-draft`（CN 初稿；EN 翻译后升 `v1.0`）

---

## Section 0 — What This Document Is

| Slug | 含义 |
|---|---|
| `#portfolio-constitution` | 三条 portfolio 强制规则 |
| `#three-layer-structure` | L1 / L2 / L3 分层定义 |

## Section 1 — Strategic Alignment & Discovery

| Slug | 含义 |
|---|---|
| `#okr-alignment` | OKR 对齐方法 |
| `#current-state-audit` | 现状 bottleneck 审计清单 |
| `#governance-identification` | Sponsor / 数据所有权识别 |
| `#constraint-classification` | FR/NFR + machine vs. human enforced 分类框架 |
| `#requirements-profile` | **Requirements Profile 输出对象**（选型输入契约） |

## Section 2 — Platform Selection & Architecture Decision Framework

| Slug | 含义 |
|---|---|
| `#one-way-door` | One-Way Door 决策框架 |
| `#six-dimension-evaluation` | 六维评估模型（workload/team/governance/streaming/finops/lock-in） |
| `#platform-scenario-mapping` | 三平台场景映射表 |
| `#platform-agnostic-architecture` | 平台无关架构原则（OLAP/OLTP 分离、serving layer） |
| `#distribution-mapping` | 分发映射（→ L2 外链路由） |

## Section 3 — Data Modeling & Governance-as-Code

| Slug | 含义 |
|---|---|
| `#medallion` | Medallion 三层职责定义 + promotion criteria |
| `#data-productization` | Data Product 定义（reliable/discoverable/secure） |
| `#governance-as-code` | 治理即代码原则（CI/CD 嵌入、脱敏、质量门控、RBAC） |
| `#platform-implementation-notes` | 各平台实现差异附注 |

## Section 4 — Ingestion & Pipeline Design

| Slug | 含义 |
|---|---|
| `#landing-layer` | Landing Layer 设计原则（与 Bronze 边界、幂等、可重放） |
| `#ingestion-patterns` | batch / CDC / streaming 三类模式边界 |
| `#near-real-time-vs-streaming` | near-real-time vs. true streaming 决策逻辑 |
| `#metadata-driven` | metadata-driven 配置化 + parse-time discipline |

## Section 5 — Migration & Greenfield Strategy

| Slug | 含义 |
|---|---|
| `#greenfield-vs-migration` | 两种起步场景分叉 |
| `#mvp-platform` | Greenfield MVP Platform 边界 |
| `#migration-strategy` | 反 Big Bang / Domain-Driven / Dual-run / 自动对账 |
| `#legacy-decommissioning` | Legacy 退役作为硬性 KPI |

## Section 6 — Team Topology & Operating Structure

| Slug | 含义 |
|---|---|
| `#dataops-mindset` | DataOps mindset 转型 |
| `#role-topology` | DE / Analytics Engineer / BI 三层分工 |
| `#platform-team-capability-matrix` | 平台选型 → 团队能力矩阵影响表 |
| `#engagement-model` | Embedded vs. Advisory + 知识转移 + exit strategy |
| `#self-service-enablement` | Data Champions / 受控开放 |

## Section 7 — Day-2 Operations & Platform Governance

| Slug | 含义 |
|---|---|
| `#sla-slo` | SLA / SLO 定义框架 |
| `#finops` | FinOps 治理原则 + 各平台机制差异 |
| `#data-observability` | Data Observability 框架（schema/downtime/volume/freshness） |
| `#incident-response` | 事故分级 + RCA |
| `#platform-evolution` | 平台演进与版本管理（联动 L2） |

---

## Deprecated

_（暂无）_
