<!-- slug-anchors: one-way-door, six-dimension-evaluation, platform-decision-record, platform-scenario-mapping, platform-agnostic-architecture, distribution-mapping -->

# Section 2 — Platform Selection & Architecture Decision Framework

> **角色**：整套体系的**枢纽 / 路由器**。它把 [Section 1 的 Requirements Profile](01-strategic-alignment.md#requirements-profile) 映射成选型结论，并把读者**分发**到对应的 L2 Playbook。
> **边界**：本节给的是**决策框架**，不是任何单平台的架构细节——「Snowflake 具体怎么搭」属于 L2。本节只决定「该走哪个 L2」。
> **依赖**：上游 [Requirements Profile](01-strategic-alignment.md#requirements-profile)；引用 [Section 3 的 Medallion 定义](03-modeling-governance.md#medallion)。
>
> ← [上一节 Section 1](01-strategic-alignment.md) · [返回首页](../README.md)

---

## 2.0 本节如何运作

```text
Requirements Profile（§1 输出）
        │
        ▼
[1] One-Way Door 识别 ── 标出不可逆决策，提高其评审规格
        │
        ▼
[2] 六维评估模型 ──────── 逐维给平台打分 → Platform Decision Record
        │
        ▼
[3] 场景映射表 ────────── 对照「代表性画像」做 sanity check
        │
        ▼
[4] 平台无关架构原则 ──── 无论选谁都必须遵守（OLAP/OLTP 分离等）
        │
        ▼
[5] 分发映射 ──────────── 路由到对应 L2 Playbook
```

> **关于平台范围**：本节以 **Snowflake / Databricks / BigQuery** 为具体承载，因为它们覆盖了当前企业数据平台的主流形态（SQL-first 仓库 / Lakehouse / serverless）。但**六维评估框架本身是 technology-agnostic 的**——换成 Redshift、Microsoft Fabric/Synapse、ClickHouse、开放 Iceberg 湖仓或 Postgres，同一套维度与打分照样适用，只是候选集不同。三平台是**代表性载体，不是方法论的边界**。

---

<a id="one-way-door"></a>
## 2.1 One-Way Door 决策框架

> 定义架构蓝图时，我对 **「one-way door decisions」（单向门决策）** 极度警惕——那些事后**极其昂贵或几乎不可能逆转**的根本性战略选择。
>
> （「单向门 / 双向门」的决策分类源自 Amazon / Jeff Bezos；本节将其应用到数据平台的架构与选型决策。）

### 2.1.1 定义与识别

| 类型 | 定义 | 决策规格 |
|---|---|---|
| **One-Way Door（单向门）** | 反悔成本极高、近乎不可逆的决策 | 慢决策、高规格评审、写 ADR、sponsor 背书 |
| **Two-Way Door（双向门）** | 可低成本回退的决策 | 快决策、可试错、授权给团队 |

**识别一个决策是否为单向门，问三个问题：**

1. **退出成本**：若两年后要换掉它，需要重写多少代码、迁移多少数据、重建多少信任？
2. **锁定半径**：它是否把其它决策也一起锁死（如选了某云就锁死了一批 native 服务）？
3. **数据引力**：数据一旦沉淀到此，迁出的引力阻力有多大？

> **方法论**：把所有架构决策先分到「单向门 / 双向门」两栏。**只对单向门动用重型评审流程**；双向门快速试错。把评审预算花在不可逆的地方，是架构治理的核心纪律。

### 2.1.2 典型单向门决策（数据平台领域）

| 决策 | 为何不可逆 | 关联 Profile 字段 |
|---|---|---|
| **核心 OLAP 平台选型** | 数据引力 + 全套建模/管道绑定 | `workload_type` / `team_capability_ceiling` |
| **云厂商绑定** | native 服务锁定、迁出成本巨大 | `cloud_lock_in_tolerance` |
| **是否分离 OLAP / OLTP** | 决定整个 serving 架构形态（见 §2.4） | `workload_type` / `streaming_need` |
| **合规版本/区域选型** | 监管区域、审计能力事后难补 | `compliance_regime` |
| **核心建模范式** | Medallion 分层一旦铺开难重构（见 §3） | `governance_maturity` |

### 2.1.3 案例（以 Snowflake 为例）：合规驱动下的版本选型

> 在重监管行业，我们倾向 **Snowflake Enterprise Edition**，因其审计友好、安全能力强。它前期单价更高，但 multi-cluster 自动扩缩等能力反而优化了整体 **TCO（总拥有成本）**。

这说明一个反直觉但关键的原则：**单向门决策不能只看 sticker price，要看 TCO 与不可逆风险的联合代价。** 在 `compliance_regime: sector-regulated` 的画像下，「更便宜但审计能力弱」的版本是一个**伪选项**——它在合规维度直接出局（见 §2.2 的一票否决机制）。版本底线还随监管强度上移：一般强合规场景 Enterprise 起步；涉及私网连接、增强加密与更高合规认证的硬监管场景（如银行核心系统），实际底线往往是 Business Critical 一级。

> **注**：以上版本名是 Snowflake 的具体例子，用来说明「合规是硬门槛、要看 TCO 而非 sticker price」这条 **technology-agnostic 原则**；换到 Databricks 或 BigQuery，对应的是各自的 tier / edition 与网络隔离、加密选项——**原则一致，具体名目不同**。

### 2.1.4 TCO 的构成（不只是 sticker price）

「看 TCO 而非单价」要落到可核对的因子。L1 给一份 technology-agnostic 的清单，具体数值在交付期按选定平台填：

| 因子 | 说明 |
|---|---|
| **License / 平台费** | edition/tier 差价、承诺用量折扣 |
| **Compute** | 查询/作业算力，含弹性伸缩与并发峰值 |
| **Storage** | 存储 + 时间旅行/快照/多副本冗余 |
| **数据出口（Egress）** | 跨云/跨区传输费，常被低估 |
| **运维人力** | 平台运维 + 团队能力缺口的[招聘/培训成本](06-team-topology.md#platform-team-capability-matrix)（见 §6.3） |
| **迁移成本** | 一次性迁入 + [Dual Running](05-migration-greenfield.md#migration-strategy) 期的双份账单（见 §5） |
| **机会成本 / 锁定** | 迁出成本与 lock-in 风险（单向门的联合代价） |

> **用法**：TCO 不是选型后才算的账，而是[六维评估](#six-dimension-evaluation) FinOps 维度与单向门决策的**输入**。sticker price 最低 ≠ TCO 最低。

---

<a id="six-dimension-evaluation"></a>
## 2.2 六维评估模型（Six-Dimension Evaluation）

把 Requirements Profile 的字段，映射到六个评估维度，逐维给候选平台打分。产物是一份 **Platform Decision Record（PDR）**，被 [Section 6 的团队能力矩阵](06-team-topology.md#platform-team-capability-matrix) 引用。

### 2.2.1 六个维度与 Profile 映射

| # | 维度 | 评估问题 | 主要 Profile 输入 |
|---|---|---|---|
| 1 | **Workload** | OLAP/AI-ML/serving 的负载形态与平台引擎是否匹配？ | `workload_type` |
| 2 | **Team** | 团队能力上限能否撑起该平台的运维/编码复杂度？ | `team_capability_ceiling` |
| 3 | **Governance** | 平台的审计/脱敏/血缘/RBAC 能否满足治理成熟度要求？ | `governance_maturity` / `compliance_regime` |
| 4 | **Streaming** | 平台对 near-real-time / true-streaming 的原生支持？ | `streaming_need` |
| 5 | **FinOps** | 成本可控性、TCO、计量与限额机制？ | `cost_sensitivity` |
| 6 | **Lock-in** | 厂商/云绑定程度与企业可移植性要求是否冲突？ | `cloud_lock_in_tolerance` |

### 2.2.2 评分机制

- **一票否决维度（Hard Gate）**：`compliance_regime` 与不可接受的 `cloud_lock_in_tolerance` 是**硬门槛**。任一候选在 Governance 或 Lock-in 维度无法满足 Profile 的硬约束 → **直接出局**，不进加权比较。
- **加权打分**：其余维度按 Profile 的取向赋权。例：`cost_sensitivity: cost-leading` 则 FinOps 权重上调；`workload_type: ai-ml-centric` 则 Workload 权重上调。
- **记录而非仅打分**：每个维度的得分必须附**一句理由**，写进 PDR。无理由的分数不可追溯，等于没评。

<a id="platform-decision-record"></a>
### 2.2.3 Platform Decision Record（PDR）模板

> **每个候选平台各出一份 PDR。** 下面给两个填写示例——同一套评估框架在不同 Requirements Profile 下会得出**不同结论**；示例本身不代表默认推荐。

**示例 A — `analytical-bi` + `regulated` 画像下的一个候选：**

```yaml
platform_decision_record:
  candidate: Snowflake-Enterprise
  hard_gates:
    compliance_regime: PASS   # Enterprise 满足 sector-regulated 审计要求
    lock_in:           PASS   # single-cloud-ok，可接受
  scores:               # 1–5，附理由；键为六维度名，↔ Profile 字段映射见 §2.2.1
    workload:   { score: 5, why: "analytical-bi 主负载，OLAP 引擎天然匹配" }
    team:       { score: 5, why: "SQL-first，团队 mid 能力即可驾驭" }
    governance: { score: 5, why: "Dynamic Masking + 审计 + 血缘齐备" }
    streaming:  { score: 3, why: "near-real-time 可满足；true-streaming 偏弱" }
    finops:     { score: 4, why: "auto-suspend + resource monitor 控成本" }    # ← cost_sensitivity
    lock_in:    { score: 3, why: "平台绑定中等，跨云可迁但有成本" }            # ← cloud_lock_in_tolerance
  decision: SELECTED
  one_way_door: true        # 标记为单向门，已走重型评审
  routes_to: L2/snowflake-lakehouse-playbook
```

**示例 B — 换成 `ai-ml-centric` + `high-software-engineering` 画像，同一框架给出不同结论：**

```yaml
platform_decision_record:
  candidate: Databricks
  hard_gates:
    compliance_regime: PASS   # Unity Catalog 满足审计/血缘要求
    lock_in:           PASS   # prefer-portable：Lakehouse + 开放格式可接受
  scores:               # 1–5，附理由
    workload:   { score: 5, why: "ai-ml-centric 主负载，Spark + MLflow 天然匹配" }
    team:       { score: 4, why: "团队 high-software-engineering，可驾驭集群/notebook" }
    governance: { score: 4, why: "Unity Catalog 治理完善；细粒度脱敏需额外配置" }
    streaming:  { score: 5, why: "Structured Streaming 原生支持 true-streaming" }
    finops:     { score: 3, why: "集群成本需 autoscaling + cluster policy 严格治理" }
    lock_in:    { score: 4, why: "Delta / Iceberg 开放格式降低迁出成本" }
  decision: SELECTED
  one_way_door: true
  routes_to: L2/databricks-ai-ml-playbook
```

> 两份 PDR 的对比说明一点：**框架是中立的，结论由 Profile 驱动**——`analytical-bi + regulated` 指向 Snowflake，`ai-ml-centric + 强工程团队` 指向 Databricks。相同维度、不同权重与得分。

> PDR 是选型这个**单向门**的 ADR（Architecture Decision Record）。它必须被存档、版本化，并在 Day-2 复盘（§7）时回看。

---

<a id="platform-scenario-mapping"></a>
## 2.3 三平台场景映射表

> ⚠️ **声明：以下是「代表性画像（representative profile）」，不是绝对边界。** 三个平台能力高度重叠，任何一个都能勉强做另一个的活。下表给的是「在该画像下，哪个平台是阻力最小的默认选择」，**不是**「只有它能做」。真实选型以 §2.2 的六维评估为准，本表仅作 sanity check。

| 代表性画像 | 默认指向 | 一句话理由 | 路由 L2 |
|---|---|---|---|
| `workload_type: analytical-bi` + `team_capability_ceiling: low~mid` + `governance_maturity: regulated` + `streaming_need: none~near-real-time` | **Snowflake** | SQL-first、低运维、审计治理成熟，低复杂度近实时分析的阻力最小路径 | [→ §2.5](#distribution-mapping) |
| `workload_type: ai-ml-centric` + `team_capability_ceiling: high-software-engineering` + 需要统一 ML/数据工程 | **Databricks** | Lakehouse + Spark + MLflow，AI/ML 为中心、需要代码弹性的场景 | [→ §2.5](#distribution-mapping) |
| 已深度绑定 GCP + 偏好 serverless + `cost_sensitivity` 敏感于闲置成本 | **BigQuery** | GCP-native、serverless、按量计费，无需管理集群 | [→ §2.5](#distribution-mapping) |

> **如何用这张表**：评估完六维得到候选后，回看本表确认「我的画像与默认指向是否一致」。**若不一致，不代表选错，而是要求 PDR 里给出明确的偏离理由**（例如「画像偏 BI 但仍选 Databricks，因为两年内有明确 ML 路线图」——这是合理偏离）。

---

<a id="platform-agnostic-architecture"></a>
## 2.4 平台无关架构原则（Platform-Agnostic Architecture）

**无论六维评估选出谁，以下原则都必须遵守。** 它们是 technology-agnostic 的架构地基。

### 2.4.1 分离 OLAP 与 OLTP（最重要的一道单向门）

> 另一个不可商量的单向门决策：**绝不用分析型仓库（如 Snowflake）去直接服务高并发、低延迟的对外 API。**

分析型平台是世界级的 **OLAP（分析）** 引擎，但强迫它处理行级、高频的事务型查询（**OLTP** 行为）**极其低效且成本失控**。即便会引入一个额外的架构层，也**永远分离 OLAP 与 OLTP**：

```text
        ┌─────────────── OLAP（重计算区）───────────────┐
源系统 ─→ Landing ─→ Bronze ─→ Silver ─→ Gold（建模/聚合）
                                              │
                                              │  pipeline 结果下沉
                                              ▼
        ┌────────────── Serving Layer（OLTP/低延迟）──────────────┐
        │  DynamoDB / 托管 PostgreSQL / Redis 等                    │
        │  ← 由此支撑高并发、低延迟的下游 API                       │
        └──────────────────────────────────────────────────────────┘
```

| 区域 | 引擎类型 | 职责 | 反模式 |
|---|---|---|---|
| **分析区** | OLAP（仓库/Lakehouse） | 重建模、大聚合、批/近实时 | ❌ 直接对外服务高频 API |
| **服务区（Serving Layer）** | OLTP/KV（DynamoDB / 托管 PostgreSQL …） | 低延迟、高并发点查 | ❌ 在此做大范围分析扫描 |

> **原则**：用 OLAP 平台做重数据建模与聚合，把**结果**通过 pipeline 下沉到 serving layer 支撑 API。这保证了长期的**系统健康度**与**成本可预测性**。该分离与 `workload_type: serving-api` 字段强相关——若 Profile 含 serving 需求，serving layer 是**必选项**，不是可选项。

### 2.4.2 Landing Layer 与 Medallion 职责（引用，不重定义）

- **Landing Layer** 的设计原则（与 Bronze 的边界、幂等、可重放）定义在 [Section 4](04-ingestion-pipeline.md#landing-layer)，本节只声明它是任何架构的入口层。
- **Medallion（Bronze/Silver/Gold）三层职责** 定义在 [Section 3](03-modeling-governance.md#medallion)，本节不重复，仅在上图中引用其分层。

> 这是 [Portfolio 规则 1](00-what-this-document-is.md#portfolio-constitution) 的体现：横切原则只在权威源定义一次。

### 2.4.3 其它平台无关原则（速查）

| 原则 | 一句话 | 详见 |
|---|---|---|
| 解耦摄取与计算 | 用 Medallion 隔离原始摄取与业务计算逻辑 | [§3 Medallion](03-modeling-governance.md#medallion) |
| 治理即代码 | 治理嵌入 CI/CD，不靠人工评审 | [§3 Governance-as-Code](03-modeling-governance.md#governance-as-code) |
| 配置化摄取 | metadata-driven，不为每个源写一次性代码 | [§4 metadata-driven](04-ingestion-pipeline.md#metadata-driven) |

---

<a id="distribution-mapping"></a>
## 2.5 分发映射（Distribution Mapping → L2）

选型结论确定后，由此路由到对应的 L2 Playbook 获取**单平台架构细节**。L2 文档遵守 [Portfolio 规则](00-what-this-document-is.md#portfolio-constitution)：只写差异，引用本 L1 的横切锚点。

| 平台 | 代表场景 | L2 Playbook | 状态 |
|---|---|---|---|
| **Snowflake** | 低复杂度近实时分析、SQL-first、强治理 | Snowflake Lakehouse Playbook（独立 repo） | ✅ 已有 · 链接待补 `<L2-SNOWFLAKE-REPO-URL>` |
| **Databricks** | AI + ML 为中心、需要代码弹性 | Databricks AI/ML Playbook（独立 repo） | 🚧 待写 · 占位 `<L2-DATABRICKS-REPO-URL>` |
| **BigQuery** | GCP-native serverless 分析 | BigQuery Analytical Playbook（独立 repo） | ⬜ 未来可选 · 占位 `<L2-BIGQUERY-REPO-URL>` |

> **引用纪律**：L2 链接确定后，本表填入真实 repo URL；L2 反向引用 L1 时使用 [`anchors.md`](../anchors.md) 的版本锚定格式 `L1@<tag>#<slug>`。Databricks/BigQuery 在 Playbook 落地前保留占位符，不留死链。

---

## 2.6 本节小结

| 产出物 | 去向 |
|---|---|
| One-Way Door 清单 | 架构评审规格分级 |
| **Platform Decision Record (PDR)** | §6 团队能力矩阵 |
| 平台无关架构原则（OLAP/OLTP 分离） | 所有 L2 必须遵守 |
| 分发映射 | 路由到 L2 Playbook |

> **下一节** → [Section 3 — Data Modeling & Governance-as-Code](03-modeling-governance.md)
