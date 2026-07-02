<!-- slug-anchors: sla-slo, value-heat-map, finops, data-observability, incident-response, platform-evolution -->

# Section 7 — Day-2 Operations & Platform Governance

> **角色**：L3 横切方法论 **#5**。平台上线后的持续运营与治理——当架构、迁移、团队都到位后，**长期运营决定平台的存亡**。
> **边界**：原则 + 各平台机制对比，**不写具体监控工具的配置**（属于 L2）。
> **依赖**：引用 [§3 的 Data Product 定义](03-modeling-governance.md#data-productization) 与 [§4 的摄取产物](04-ingestion-pipeline.md)。
>
> ← [上一节 Section 6](06-team-topology.md) · [返回首页](../README.md)

---

<a id="sla-slo"></a>
## 7.1 价值优先级与 SLA / SLO 框架

<a id="value-heat-map"></a>
### 7.1.1 Value Heat Map（先拿 Quick Wins）

> 在初期交付阶段，我用一张「**业务价值 × 多团队使用度**」的 **Heat Map（热力图）** 来优先排序高影响、跨职能的数据资产，尽早给 stakeholder 交付即时价值。

| | 单团队使用 | 多团队使用 |
|---|---|---|
| **高业务价值** | 重要但局部，第二批 | 🔥 **最高优先**（quick win，跨职能影响大） |
| **低业务价值** | 最低优先 | 谨慎：使用广但价值低，先确认真需求 |

> 这张图同时驱动 [§5 MVP 选域](05-migration-greenfield.md#mvp-platform)（首发选 🔥 象限的域）与 Day-2 的运营投入排序。

### 7.1.2 SLA / SLO 定义框架 ⭐

为每个 [Data Product](03-modeling-governance.md#data-productization) 定义可度量的服务目标。区分 SLO（内部目标）与 SLA（对消费者的承诺）：

| 维度 | 指标定义 | 示例 SLO |
|---|---|---|
| **Freshness（时效）** | 数据最新到什么时间点；端到端延迟 | "Gold 财务集市每日 08:00 前刷新完成" |
| **Uptime / Availability（可用性）** | 平台/关键数据集的可用时间比 | "核心 Gold 数据集月可用性 ≥ 99.5%" |
| **Query Performance（查询性能）** | 关键查询/报表的响应时间 | "核心 dashboard p95 查询 < 5s" |

> **原则**：SLO 必须**可度量、有基线、绑定具体 Data Product**。基线来自 [§1.2 现状审计](01-strategic-alignment.md#current-state-audit)（迁移场景下，新平台 SLO 不应劣于旧平台基线）。SLO 是 [observability](#data-observability) 监控的目标值，也是 [incident](#incident-response) 分级的依据。

---

<a id="finops"></a>
## 7.2 FinOps 成本治理 ⭐

> 上线后，建立严格的 **FinOps** 机制。在平台层配置 **warehouse 级资源监控、严格的 auto-suspend 策略、实时异常告警**，防止失控的 compute 账单。

### 7.2.1 FinOps 三原则（technology-agnostic）

| 原则 | 说明 | 关联 |
|---|---|---|
| **资源可见 + 归因** | 成本按域/团队/产品归因，谁花的谁看见 | [§1.3 ownership](01-strategic-alignment.md#governance-identification) |
| **闲置即关停（auto-suspend）** | 计算资源空闲自动挂起，不为空转付费 | `cost_sensitivity` 字段 |
| **限额 + 异常告警** | 设资源上限/预算，超阈值实时告警并可熔断 | [incident](#incident-response) |

> **与迁移的联动**：FinOps 的最大单笔节流，往往是 [§5 的 Legacy 退役](05-migration-greenfield.md#legacy-decommissioning)——消除双重账单。FinOps 治理若不推动旧系统退役，就是在精装修一栋还在交两份房租的房子。

### 7.2.2 各平台 FinOps 机制差异（附注）

> 附注，非正文。原则一致，机制不同；细节见 [L2](02-platform-selection.md#distribution-mapping)。

| 机制 | Snowflake | Databricks | BigQuery |
|---|---|---|---|
| **闲置关停** | Warehouse auto-suspend | Cluster auto-termination | Serverless（天然无闲置计费） |
| **限额** | Resource Monitors | Budget / cluster policies | Quotas / 预留 slots / 按量上限 |
| **成本归因** | Warehouse + query tagging | Cluster tags / system tables | Labels + billing export |
| **弹性优化 TCO** | multi-cluster auto-scaling | autoscaling clusters | 自动 slot 调度 |

---

<a id="data-observability"></a>
## 7.3 Data Observability（数据可观测性）⭐

> 生产环境管理**不能只靠静态测试**。我们部署 **Data Observability** 框架，监控上游 schema 变更、数据停摆（data downtime）、数据漂移（data drift），确保工程团队在高管看到破图之前，就**主动拦截并解决**数据质量问题。

### 监控的四个支柱

| 支柱 | 监控什么 | 信号来源 |
|---|---|---|
| **Freshness（时效）** | 数据是否按时到达 | 对照 [§7.1 freshness SLO](#sla-slo) |
| **Schema（结构漂移）** | 上游 schema 是否变化/破坏下游 | 最早采集点 = [§4 parse-time discipline](04-ingestion-pipeline.md#metadata-driven) |
| **Volume（数据量）** | 行数/体量是否异常（突增/骤降） | 摄取批次统计 |
| **Downtime / Quality（停摆与质量）** | 数据是否停更、质量是否劣化 | 质量测试 + 管道状态 |

> **核心主张**：**static testing（静态测试）≠ observability。** [§3 的 dbt 测试](03-modeling-governance.md#governance-as-code) 在 CI 期捕获**已知**的坏；observability 在生产期持续捕获**未知**的异常（尤其上游 schema/volume 漂移）。二者互补，缺一不可。observability 的目标是**主动拦截**——在 executive 看到破掉的 dashboard **之前**就发现并响应。

---

<a id="incident-response"></a>
## 7.4 Incident Response & Escalation（事故响应与升级）

observability 发现异常后，需要一套响应机制把「发现」变成「解决」。

### 7.4.1 事故分级（Severity）

| 级别 | 定义 | 响应 |
|---|---|---|
| **SEV-1** | 核心 Data Product 不可用 / 监管报送受影响 / 错误数据已外泄到决策 | 立即响应、拉 owner + sponsor、可回退 |
| **SEV-2** | 重要数据集延迟/质量劣化，未外泄 | 当班响应、限时修复 |
| **SEV-3** | 局部、非关键、可排期修复 | 进 backlog |

> 分级依据是 [§7.1 SLO](#sla-slo) 与 [§1.3 数据 ownership](01-strategic-alignment.md#governance-identification)（谁的域、谁的产品决定升级路径）。

### 7.4.2 RCA（Root Cause Analysis 根因分析）

| 原则 | 说明 |
|---|---|
| **无指责（blameless）** | 复盘对事不对人，目标是系统改进 |
| **根因而非症状** | 追到根因（如「某源 schema 漂移未被 parse-time 拦截」），不止步于「重跑就好」 |
| **转化为门控** | 每个 RCA 产出至少一条**可机器强制**的新门控（呼应 [§3 治理即代码](03-modeling-governance.md#governance-as-code)），让同类事故不再复发 |

> **闭环**：incident → RCA → 新增 [Governance-as-Code](03-modeling-governance.md#governance-as-code) 门控 / [observability](#data-observability) 监测 → 防复发。这是平台**自我加固**的核心循环。

---

<a id="platform-evolution"></a>
## 7.5 平台演进与版本管理

平台不是上线即终态。上游 runtime 升级、能力演进、breaking change 需要被管理，并**联动 L2**。

| 事项 | 做法 | 联动 |
|---|---|---|
| **上游 runtime 升级** | 平台版本/引擎升级走灰度 + 回归测试，不盲目跟新 | [§6 DataOps CI/CD](06-team-topology.md#dataops-mindset) |
| **Breaking Change 管理** | 平台或横切原则的 breaking change → 升 L1 版本 tag | [`anchors.md`](../anchors.md) 版本锚定 |
| **联动 L2** | L1 横切锚点变更，通知所有引用它的 L2 Playbook 同步 | [Portfolio 规则 3](00-what-this-document-is.md#portfolio-constitution) |
| **定期复盘选型** | 周期性回看 [§2 PDR](02-platform-selection.md#platform-decision-record)，确认选型假设仍成立 | §2 单向门复审 |

> **与 Portfolio 宪法的闭环**：L1 任何被 [`anchors.md`](../anchors.md) 登记的 slug 发生 breaking change，必须升版本 tag 并通知 L2——这是 [§0 规则 3](00-what-this-document-is.md#portfolio-constitution) 在 Day-2 的具体执行。平台演进若不联动文档版本，跨 repo 引用就会悄悄腐烂成死链。

---

## 7.6 本节小结

| 产出物 | 关联 |
|---|---|
| [Value Heat Map](#value-heat-map) | §5 MVP 选域 |
| [SLA/SLO 框架](#sla-slo) | §3 Data Product / §1 基线 |
| [FinOps 三原则 + 平台差异](#finops) | §5 退役 / §1 cost_sensitivity |
| [Observability 四支柱](#data-observability) | §3 测试 / §4 parse-time |
| [Incident + RCA 闭环](#incident-response) | §3 治理即代码 |
| [平台演进与版本联动](#platform-evolution) | §0 Portfolio 宪法 / anchors |

---

## 7.7 全文闭环

至此，L1 完成一个完整 lifecycle 闭环：

```text
§1 为什么建 ──→ §2 选什么 ──→ §3 怎么建模治理 ──→ §4 怎么摄取
                                                          │
§7 怎么长期活 ←── §6 谁来运营 ←── §5 怎么迁移上线 ←───────┘
   │
   └─→ RCA / 演进 反馈回 §2 选型复审 + §3 新门控（自我加固循环）
```

> **返回** → [中文版首页](../README.md) · [Section 0 宪法](00-what-this-document-is.md) · [锚点清单](../anchors.md)
