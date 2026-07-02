# Task Brief — Data Platform Delivery & Operating Model (L1)

> 本文件规划整套 L1 文档的产出方式：每节的目标、依赖关系、产出物边界、写作顺序。
> 目的是让所有章节可以**有序、不重复、可引用**地被逐步完成。

---

## 1. 全局约束（所有章节通用）

写每一节时都要遵守的硬性规则，避免后期返工：

| 约束 | 说明 |
|---|---|
| **Technology-agnostic 优先** | L1 正文只写原则；平台特定实现一律以「各平台实现差异」附注形式收尾，或剥离到 L2。 |
| **反重复** | 横切方法论（Section 3/4/6/7）只在 L1 定义一次。其他节需要时引用，不重写。 |
| **稳定锚点** | 每节标题与小节标题用稳定的 slug（如 `#governance-as-code`），供 L2 跨 repo 外链。改 slug = breaking change，需升版本 tag。锚点登记在 `docs/cn/anchors.md`。 |
| **语言** | 中文叙述 + 英文术语。术语首次出现给英文，后续可中英混用。全文完成后统一翻译为英文版。 |
| **输入/输出契约** | 凡产出「传给下游章节的结构化对象」（如 Section 1 的 Requirements Profile），必须显式列出字段，下游章节直接引用同名对象。 |
| **表优于 bullet** | 决策维度、对比、映射等结构化内容用表格呈现。 |

---

## 2. 章节依赖关系

写作顺序不能完全按编号，要按依赖。关键依赖链：

```text
Section 1 (Requirements Profile 输出)
      ↓ 提供选型输入
Section 2 (六维评估 + 分发路由)
      ↓ 引用建模/治理原则
Section 3 (Medallion + Governance-as-Code)   ← 被 2/5/7 引用
      ↓
Section 4 (Ingestion)                         ← 被 5/7 引用
Section 5 (Migration & Greenfield)
Section 6 (Team Topology)                     ← 引用 2 的选型结论
Section 7 (Day-2 Ops)                         ← 引用 3/4 的产物定义
```

**结论：Section 2 是枢纽，但它依赖 Section 1 的输出契约和 Section 3 的原则引用。** 因此先锁定 Section 1 的 Requirements Profile 字段 + Section 3 的核心定义骨架，再正式展开 Section 2。

---

## 3. 推荐写作顺序（四批）

| 批次 | 章节 | 理由 |
|---|---|---|
| **Batch 1 — 地基** | Section 1 + Section 2 | 确立 Requirements Profile 契约 + 选型路由器，整套体系的承重结构。 |
| **Batch 2 — 横切核心** | Section 3 + Section 4 | 被最多章节引用的方法论，越早锁定越能减少后续返工。 |
| **Batch 3 — 横切其余** | Section 5 + Section 6 + Section 7 | 依赖前面的产物定义，最后批量完成。 |
| **Batch 4 — 收口** | 全文一致性校对 + 英文翻译 + L2 外链锚点核对 | 统一术语、核对跨 repo 锚点、产出英文版。 |

---

## 4. 逐章节产出规格

每节给出：**目标 / 必含产出物 / 边界（不写什么）/ 依赖**。

### Section 1 — Strategic Alignment & Discovery
- **目标**：把模糊的业务诉求转成可用于选型的结构化输入。
- **必含产出物**：
  - OKR 对齐方法
  - 现状 bottleneck 审计清单
  - 治理结构识别（Sponsor / 数据所有权）
  - 约束分类框架（FR / NFR + machine-enforced vs. human-enforced 轴线）
  - **Requirements Profile 对象**（显式字段：workload 类型 / 团队能力上限 / 治理成熟度 / streaming 需求 / 云厂商绑定度）
- **边界**：不做任何平台选型判断（那是 Section 2）。
- **依赖**：无（链条起点）。

### Section 2 — Platform Selection & Architecture Decision Framework
- **目标**：把 Requirements Profile 映射到平台选型，并分发到对应 L2。
- **必含产出物**：
  - One-Way Door 决策框架（定义 + 识别方法）
  - 六维评估模型表（workload / team / governance / streaming / FinOps / lock-in）
  - 三平台场景映射表（含「representative profile, 非绝对边界」声明）
  - 平台无关架构原则（OLAP/OLTP 分离、Landing Layer、Medallion 职责引用 Section 3）
  - **分发映射**：Snowflake → 已有 Playbook（URL 待补）；Databricks → 待写 Playbook 占位；BigQuery → 占位
- **边界**：不写任何单平台的架构细节（留给 L2）。
- **依赖**：Section 1 的 Requirements Profile；引用 Section 3 的 Medallion 定义。

### Section 3 — Data Modeling & Governance-as-Code
- **目标**：定义建模分层与治理即代码的权威原则（L3）。
- **必含产出物**：
  - Medallion 三层职责定义 + promotion criteria
  - Data Productization 定义（reliable / discoverable / secure）
  - Governance-as-Code 原则（CI/CD 嵌入、Bronze 层脱敏、质量门控）
  - 各平台实现差异附注（Snowflake / Databricks / BigQuery）
- **边界**：原则为主；平台实现只做附注，深入细节留 L2。
- **依赖**：无（横切权威源）。被 2/5/7 引用。

### Section 4 — Ingestion & Pipeline Design
- **目标**：定义摄取与管道设计的平台无关原则（L3）。
- **必含产出物**：
  - Landing Layer 设计原则（与 Bronze 边界、幂等、可重放）
  - batch / CDC / streaming 三类模式边界
  - near-real-time vs. true streaming 决策逻辑
  - metadata-driven 配置化原则 + parse-time discipline
- **边界**：不绑定具体编排工具实现。
- **依赖**：引用 Section 3 的 Bronze 定义。被 5/7 引用。

### Section 5 — Migration & Greenfield Strategy
- **目标**：覆盖两种平台起步场景的策略（L3）。
- **必含产出物**：
  - Greenfield vs. Migration 场景分叉
  - Greenfield：MVP Platform 边界
  - Migration：反 Big Bang、Domain-Driven、Dual-run + 自动对账、零方差验证
  - Legacy Decommissioning 作为硬性 KPI
- **边界**：不写具体平台的迁移工具。
- **依赖**：引用 Section 3/4 的层与管道定义。

### Section 6 — Team Topology & Operating Structure
- **目标**：平台与团队能力的协同设计（L3）。
- **必含产出物**：
  - DataOps mindset 转型
  - DE / Analytics Engineer / BI 三层分工
  - 平台选型对团队能力矩阵的影响表
  - 服务方嵌入模式（Embedded vs. Advisory）+ 知识转移 + exit strategy
  - Self-Service Enablement（Data Champions、受控开放）
- **边界**：组织设计原则，不写具体招聘 JD。
- **依赖**：引用 Section 2 的选型结论。

### Section 7 — Day-2 Operations & Platform Governance
- **目标**：平台上线后的持续运营与治理（L3）。
- **必含产出物**：
  - SLA / SLO 定义框架（freshness / uptime / query performance）
  - FinOps 治理原则 + 各平台机制差异
  - Data Observability 框架（schema drift / downtime / volume / freshness）
  - Incident Response & Escalation（事故分级 + RCA）
  - 平台演进与版本管理（上游 runtime 升级、breaking change 联动 L2）
- **边界**：原则 + 各平台机制对比，不写具体监控工具配置。
- **依赖**：引用 Section 3/4 的产物定义。

---

## 5. 完成定义（Definition of Done）

整套 L1 视为完成，需满足：

- [x] Section 0–7 全部正文完成（CN）
- [x] 每节有稳定 slug 锚点，已记录成一张「锚点清单」供 L2 引用（`docs/cn/anchors.md`）
- [x] Requirements Profile 字段在 Section 1 定义、Section 2 引用，命名一致
- [x] 横切方法论无重复定义（Section 2/5/6/7 对 3/4 均为引用而非重写）
- [ ] Section 2 分发映射填入真实 L2 repo URL（Snowflake repo 已存在、URL 待补填；Databricks / BigQuery 待 Playbook 落地）
- [ ] 中文版定稿后产出英文版
- [x] README 章节地图状态全部更新

---

## 6. 给协作者 / AI agent 的交接说明

如果把某一节交给 Claude 或其他 agent 写，提供：
1. 本 TASK_BRIEF 对应章节的「产出规格」段落
2. 该节依赖的上游产物（如 Requirements Profile 字段定义）
3. 已完成章节中需要被引用的锚点（见 `docs/cn/anchors.md`）
4. 全局约束（第 1 节）

要求 agent 输出时：保持 technology-agnostic、平台差异走附注、用稳定 slug、表优于 bullet。
