<!-- slug-anchors: medallion, data-productization, governance-as-code, platform-implementation-notes -->

# Section 3 — Data Modeling & Governance-as-Code

> **角色**：L3 横切方法论 **#1**，被 [§2](02-platform-selection.md) / [§4](04-ingestion-pipeline.md) / [§5](05-migration-greenfield.md) / [§7](07-day2-operations.md) 引用。本节是 Medallion 与 Governance-as-Code 的**唯一权威源（single source of truth）**。
> **边界**：原则为主。平台具体怎么实现只做[附注](#platform-implementation-notes)，深入细节留 L2。
> **依赖**：无（横切权威源）。
>
> ← [上一节 Section 2](02-platform-selection.md) · [返回首页](../README.md)

---

## 3.0 本节解决的两类负债

> 在 SDLC（开发生命周期）中，我重点防范两类负债：**技术债（technical debt）** 与 **数据治理债（governance debt）**。治理债初期通常**不可见**，但越往后偿还成本越呈**指数级**增长。

| 负债 | 初期表现 | 后期代价 | 本节对策 |
|---|---|---|---|
| **技术债** | 计算逻辑与摄取逻辑纠缠 | 改一处崩一片 | [Medallion 解耦](#medallion) |
| **治理债（隐性）** | "没人知道这表谁在用"、PII 散落 | 合规事故、信任崩塌 | [Governance-as-Code](#governance-as-code) |

核心思路：**把治理从「事后的官僚评审」变成「嵌入流水线的自动门控」**，从而实现真正的 **Data Productization（数据产品化）**。

---

<a id="medallion"></a>
## 3.1 数据建模：范式与 Medallion 分层 ⭐

> 采用 **Medallion（Bronze/Silver/Gold）** 架构，把**原始系统摄取逻辑**与**下游业务计算逻辑**彻底解耦。

这是被全体 L2 引用的分层定义。**任何平台的架构都按此分层职责落地。**

> （Medallion 分层架构由 Databricks 提出；本节给出的是 technology-agnostic 的分层职责定义，任何平台均可落地。）

### 3.1.1 建模范式的选择（Modeling Paradigm）

Medallion 是**分层**（raw → cleansed → curated），不是**建模范式**。分层解决「摄取与业务计算解耦」，范式解决「Silver/Gold 里的表按什么结构组织」。二者正交，**必须都定**——只搭了 Medallion 却没定范式，是常见的隐性建模债。

L1 只定**范式选型原则**，不锁死具体范式（DDL 级细节属于 L2）：

| 范式 | 适用信号 | 代价 / 注意 |
|---|---|---|
| **维度建模（Star Schema / Kimball）** | BI 与自助分析为主、口径需对业务直观（`workload_type: analytical-bi`） | 需前置定义 grain 与一致性维度；聚合友好，是多数分析场景默认 |
| **Data Vault** | 多源整合、强审计溯源、源频繁变更（`governance_maturity: regulated`） | 结构冗长，查询需下游再建集市，工程成本高 |
| **宽表 / One Big Table** | 单一消费场景、追求查询简单与列存性能 | 冗余高、口径易发散，不利多消费者复用 |

> **两条必须在建模期定死的决策**：
> - **Grain（粒度）**：每张事实/明细表「一行代表什么」必须唯一且显式声明——粒度含糊是下游口径冲突的头号根因。
> - **SCD（缓变维，Slowly Changing Dimension）**：维度历史如何留痕（Type 1 覆盖 / Type 2 留历史版本）由业务对「可追溯」的要求决定，通常在 Silver→Gold 落地。

> **归属与不可逆性**：范式选择在 L1 定原则，具体 DDL、dbt 物化策略、SCD 实现属于 [L2](02-platform-selection.md#distribution-mapping)。范式一旦大规模铺开，重构成本极高——属 [§2.1 单向门](02-platform-selection.md#one-way-door) 一类，选型期即须定。

### 3.1.2 三层职责定义

| 层 | 别名 | 职责 | 数据形态 | 谁负责（见 §6） |
|---|---|---|---|---|
| **Bronze** | Raw / 原始层 | 忠实落地源数据，**不做业务转换**；在此完成合规脱敏 | 接近源结构、append、保留历史 | Data Engineer |
| **Silver** | Cleansed / 清洗层 | 清洗、去重、标准化、一致性维度、blending | 规范化、可信、面向集成 | Analytics Engineer |
| **Gold** | Curated / 业务层 | 业务聚合、指标、面向消费的宽表/数据集市 | 面向分析/消费、口径权威 | Analytics Engineer |

> **关键边界**：Bronze 只管「原样进来 + 合规脱敏」，**绝不**承载业务计算；业务口径只在 Silver→Gold 发生。这道边界就是「技术债解耦」的本体——改业务口径不碰摄取，改摄取不污染业务层。

### 3.1.3 Promotion Criteria（晋级门槛）⭐

数据**不会自动**从一层升到下一层。每次晋级是一道**自动门控**（这正是 [Governance-as-Code](#governance-as-code) 的落点）：

| 晋级 | 必须通过的门控 |
|---|---|
| **→ Bronze** | schema 落地成功；PII 已按合规脱敏；幂等/可重放（见 [§4 Landing](04-ingestion-pipeline.md#landing-layer)） |
| **Bronze → Silver** | 数据质量测试通过（唯一性/非空/参照完整性）；标准化规则应用；去重 |
| **Silver → Gold** | 业务规则测试通过；指标口径校验；catalog 文档齐备；owner 签署 |

> **原则**：只有通过严格自动治理检查的数据资产，才被晋级到 Silver/Gold，成为可信的 **Data Product**。未通过 = 卡在原层，不污染下游。

---

<a id="data-productization"></a>
## 3.2 Data Productization（数据产品化）

晋级到 Silver/Gold 的资产，不是「一张表」，而是一个 **Data Product（数据产品）**。一个合格的数据产品必须同时满足三性：

| 属性 | 含义 | 如何保证（机器强制） |
|---|---|---|
| **Reliable（可靠）** | 质量有保证、按 SLA 刷新、可信 | dbt/CI 数据质量测试 + [§7 freshness SLO](07-day2-operations.md#sla-slo) |
| **Discoverable（可发现）** | 有文档、有血缘、可被检索 | catalog 文档作为晋级门控的一部分 |
| **Secure（安全）** | 访问受控、敏感数据脱敏 | [RBAC](#governance-as-code) + Bronze 脱敏 |

> **判定标准**：一个资产若不能同时满足三性，它就**不是** Data Product，只是「一张恰好存在的表」，不得对外宣称为可消费资产。三性都靠**机器强制**保证，而非靠人承诺——呼应 [§1.4.2 machine-enforced 原则](01-strategic-alignment.md#constraint-classification)。

---

<a id="governance-as-code"></a>
## 3.3 Governance-as-Code（治理即代码）⭐

> 我**不**把数据治理当成官僚式评审流程，而是把它**嵌入 CI/CD 流水线**，从而实现真正的数据产品化——确保数据资产可靠、可发现、且天生安全。

这是被 [§2](02-platform-selection.md) / [§5](05-migration-greenfield.md) / [§7](07-day2-operations.md) 引用的核心原则。它接收 [§1.4.2 的 machine-enforced 约束清单](01-strategic-alignment.md#constraint-classification) 作为实现范围。

### 3.3.1 四条治理即代码原则

| # | 原则 | 落地方式 |
|---|---|---|
| 1 | **治理写进流水线，不写进会议** | 治理规则 = CI/CD 检查；违反 = 构建失败，无法合并/晋级 |
| 2 | **早脱敏（Shift-Left Security）** | 在 **Bronze 层**就按合规脱敏，而非等到消费层 |
| 3 | **质量门控即晋级门槛** | [§3.1.3 promotion criteria](#medallion) 由自动测试强制 |
| 4 | **防御式访问控制（RBAC）** | day-1 设计 RBAC，防 role explosion 与 PII 泄漏 |

### 3.3.2 早脱敏：在 dbt 开发期用 Tag 注入安全（Governance-as-Code）

> 在 Bronze 层早期，我们按监管要求脱敏。把安全规则通过 **Tagging（治理即代码）** 直接烘焙进 **dbt 开发阶段**——平台侧用动态脱敏策略（如 Snowflake Dynamic Masking Policy）落地。

机制（technology-agnostic 表述）：

```text
开发期：给字段打 governance tag（如 pii.email、pii.ssn）—— 写在 dbt/模型代码里，进版本控制
   │
CI 期：检查「凡标 PII 的字段，必须绑定脱敏策略」—— 未绑定则构建失败
   │
运行期：平台按 tag → 脱敏策略 自动对未授权角色脱敏
```

> **要点**：脱敏规则是**代码**（tag + 策略绑定），随模型一起评审、测试、版本化、回滚——而不是某个 DBA 手工点的配置。平台实现差异见 [§3.4 附注](#platform-implementation-notes)。

### 3.3.3 质量门控与文档作为 CI 一等公民

在 dbt（或等价工具）内**同时**强制：

- **自动数据质量测试**：唯一性、非空、参照完整性、接受值、自定义业务断言。
- **数据 catalog 文档**：模型/字段描述齐备，否则晋级门控不通过。

> 二者都是 [promotion criteria](#medallion) 的硬性组成。**未测试、未文档化的资产不得晋级**——这把「可靠」「可发现」从口号变成构建期的强制条件。

### 3.3.4 防御式 RBAC（Defensive Access Control）

> 从 day-1 设计严格的 **RBAC（基于角色的访问控制）** 框架，防止「role explosion（角色爆炸）」与 PII/敏感数据泄漏；并用自动化的 **Query History 分析**做持续行为审计。

| 设计原则 | 说明 |
|---|---|
| **最小权限** | 角色按职责授予最小可用权限 |
| **防角色爆炸** | 角色按「功能 + 数据域」二维规划，避免一人一角色的指数膨胀 |
| **继承式角色层级** | 用角色继承表达权限层级，而非平铺复制 |
| **持续行为审计** | 自动分析 query history，发现异常访问模式（呼应 [§7 observability](07-day2-operations.md#data-observability)） |

> RBAC 的域划分直接消费 [§1.3 的「域 → Data Owner」表](01-strategic-alignment.md#governance-identification)。

---

<a id="platform-implementation-notes"></a>
## 3.4 各平台实现差异附注

> 以下是**附注**，不是正文。原则在上文已定义且对所有平台一致；下表只列「同一原则在各平台落地的差异」。深入细节属于 L2。

| 原则 | Snowflake | Databricks | BigQuery |
|---|---|---|---|
| **早脱敏** | Dynamic Data Masking Policy + Object Tagging | Unity Catalog column masks + tags | Column-level security + Policy Tags（Data Catalog） |
| **质量门控** | dbt tests + Tasks/Streams 编排 | dbt / DLT expectations | dbt tests / Dataform assertions |
| **血缘 / catalog** | Snowflake Horizon + dbt docs | Unity Catalog lineage | Dataplex / Data Catalog |
| **RBAC** | Role 层级 + 继承 | Unity Catalog（account/metastore 级） | IAM + dataset/table ACL |
| **行为审计** | ACCOUNT_USAGE / QUERY_HISTORY | system tables / audit logs | Cloud Audit Logs / INFORMATION_SCHEMA |

> ⚠️ 上表仅为指路，**不构成实现指南**。具体 DDL/策略语法见对应 [L2 Playbook](02-platform-selection.md#distribution-mapping)。

---

## 3.5 本节小结

| 产出物（权威定义） | 被谁引用 |
|---|---|
| [Medallion 三层职责 + promotion criteria](#medallion) | §2 / §4 / §5 / §7 |
| [Data Product 三性](#data-productization) | §7（SLA 对象） |
| [Governance-as-Code 四原则](#governance-as-code) | §2 / §5 / §7 |
| [RBAC 设计原则](#governance-as-code) | §6 / §7 |

> **下一节** → [Section 4 — Ingestion & Pipeline Design](04-ingestion-pipeline.md)
