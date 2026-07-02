<!-- slug-anchors: dataops-mindset, role-topology, platform-team-capability-matrix, engagement-model, self-service-enablement -->

# Section 6 — Team Topology & Operating Structure

> **角色**：L3 横切方法论 **#4**。平台与团队能力的协同设计——技术升级必须匹配团队能力升级。
> **边界**：组织设计**原则**，不写具体招聘 JD。
> **依赖**：引用 [§2 的选型结论（PDR）](02-platform-selection.md#platform-decision-record)。
>
> ← [上一节 Section 5](05-migration-greenfield.md) · [返回首页](../README.md)

---

## 6.0 没有团队升级，再好的栈也是摆设

> 技术升级必须匹配团队能力升级。没有现代化的团队，再好的 Modern Data Stack (MDS) 也会变成 **shelfware（束之高阁的软件）**。

本节四件事：转**心智**（DataOps）、定**分工**（角色拓扑）、配**能力**（按选型）、设**协作与退出**（服务模式）、最终**还权于业务**（自助）。

---

<a id="dataops-mindset"></a>
## 6.1 DataOps Mindset 转型

> 传统数据团队常依赖拖拽式 ETL 工具或裸写存储过程，缺乏核心**软件工程纪律**。我推动团队转向 **DataOps mindset**，让版本控制（Git Flow）、单元测试（TDD）、持续集成（CI/CD）成为每个数据工程师的**基础技能**。

| 维度 | 传统数据团队 | DataOps 团队 |
|---|---|---|
| **变更管理** | 在 GUI 里手改、无版本 | Git Flow，一切进版本控制 |
| **质量保证** | 上线后靠人发现 | TDD / 自动测试（呼应 [§3 质量门控](03-modeling-governance.md#governance-as-code)） |
| **交付** | 手工部署、不可重复 | CI/CD 自动化、可重复、可回滚 |
| **协作** | 个人英雄、知识在脑子里 | code review、知识在 repo 里 |

> **这是 [Governance-as-Code](03-modeling-governance.md#governance-as-code) 能落地的前提**：治理写进流水线，要求团队先具备「把一切当代码」的工程纪律。没有 DataOps 心智，治理即代码无从谈起。

---

<a id="role-topology"></a>
## 6.2 角色拓扑：DE / Analytics Engineer / BI 三层分工 ⭐

> 我引入 **Analytics Engineer（分析工程师）** 角色，作为 Data Engineer (DE) 与 Business Analyst (BI) 之间的桥梁。

| 角色 | 核心职责 | 对应 Medallion 层 | 关键技能 |
|---|---|---|---|
| **Data Engineer (DE)** | 核心摄取、性能调优、基础设施稳定性 | [Landing / Bronze](04-ingestion-pipeline.md#landing-layer) | 软件工程、管道、平台运维 |
| **Analytics Engineer (AE)** | 业务建模、[治理即代码](03-modeling-governance.md#governance-as-code) | [Silver / Gold](03-modeling-governance.md#medallion) | SQL/dbt、建模、领域知识 |
| **BI / Business Analyst** | 消费 Gold、出洞察、对接业务 | 消费 [Gold](03-modeling-governance.md#medallion) | 可视化、业务分析 |

> **为什么需要 AE 这一层**：让 **DE 专注核心摄取、性能调优与基础设施稳定性**，而 **AE 拥有 dbt 里的业务建模与治理即代码**。这个结构**防止 DE 被 ad-hoc 业务请求拖垮**——否则 DE 一边修管道一边接业务口径需求，两头都做不好。AE 是「业务语义」与「工程纪律」的交汇点，直接承载 [§3 的 Silver→Gold 晋级与文档](03-modeling-governance.md#medallion)。

---

<a id="platform-team-capability-matrix"></a>
## 6.3 平台选型 → 团队能力矩阵影响表 ⭐

平台选型（[§2 PDR](02-platform-selection.md#platform-decision-record)，字段 `team_capability_ceiling`）直接决定团队需要什么能力配置。这是选型的**组织后果**，常被忽略：

| 选型画像 | 对 DE 的要求 | 对 AE 的要求 | 团队风险 |
|---|---|---|---|
| **SQL-first 仓库**（如 Snowflake 画像） | 中：SQL + 编排即可 | 高：dbt 建模是主战场 | 低门槛，AE 是瓶颈岗 |
| **Lakehouse / 代码弹性**（如 Databricks 画像） | 高：Spark/Python/集群调优 | 中高：需懂 notebook + dbt | DE 能力门槛高，招聘难 |
| **Serverless**（如 BigQuery 画像） | 中：少运维，重 SQL + IaC | 高：建模 + 成本意识 | 成本治理依赖 AE 自律 |

> **核心主张**：**选型不只是选技术，是选「你要养什么样的团队」。** 若 [§1 Profile](01-strategic-alignment.md#requirements-profile) 的 `team_capability_ceiling = low-sql-only`，却在 §2 选了需要高软件工程能力的平台，差距必须由**招聘或培训**填补——这个差距要在选型时就计入 [TCO](02-platform-selection.md#one-way-door)，而不是上线后才发现团队驾驭不了。

---

<a id="engagement-model"></a>
## 6.4 服务方嵌入模式 + 知识转移 + Exit Strategy

当由外部服务方/咨询团队交付平台时，协作模式决定了「交付后团队能否独立运营」。

### 6.4.1 Embedded vs. Advisory

| 模式 | 描述 | 适用 | 风险 |
|---|---|---|---|
| **Embedded（嵌入式）** | 服务方工程师进入客户团队共同交付 | 客户团队能力起点低、需边做边学 | 依赖加深，退出难 |
| **Advisory（顾问式）** | 服务方定方向/评审，客户团队动手 | 客户已有一定能力、要的是方法论 | 落地速度慢，依赖客户执行力 |

> 多数情况是**先 Embedded 后 Advisory**：初期嵌入带飞，随知识转移推进逐步退成顾问角色。

### 6.4.2 知识转移与 Exit Strategy（关键）

> **嵌入式服务的成败不看交付了什么，而看离开后客户能否独立运营。**

| 要素 | 做法 |
|---|---|
| **知识转移** | 结对编程、文档化（呼应 [§3 catalog 文档](03-modeling-governance.md#governance-as-code)）、内部培训，知识进 repo 不进个人脑 |
| **能力移交里程碑** | 设「客户独立完成 X」的可验收里程碑，而非按工时结算 |
| **Exit Strategy（退出策略）** | 项目启动**即**定义退出标准与时间表——服务方目标是「让自己变得不被需要」 |

> **与 [§5 Legacy 退役](05-migration-greenfield.md#legacy-decommissioning) 的对称性**：迁移要硬性退役旧系统，服务方协作要硬性退出依赖。两者都拒绝「无限期续命」。退出策略不清晰的咨询关系，会和不退役的 legacy 一样持续烧钱。

---

<a id="self-service-enablement"></a>
## 6.5 Self-Service Enablement（自助化赋能）

> 平台管理的**终极目标是数据民主化（data democratization）**。在内部团队升级的同时，我们在业务单元内培养 **'Data Champions'**。通过开放受严格治理的 Silver/Gold 层，实现真正的**自助分析（Self-Service Analytics）**，把数据团队从被动的「接工单瓶颈」转变为战略性的「平台赋能者」。

| 要素 | 说明 |
|---|---|
| **Data Champions** | 在各业务单元培养的数据骨干，作为业务侧的自助分析带头人与平台联络人 |
| **受控开放（Governed Access）** | 只开放**通过治理门控的** [Silver/Gold 数据产品](03-modeling-governance.md#data-productization)，受 [RBAC](03-modeling-governance.md#governance-as-code) 约束——开放 ≠ 失控 |
| **角色转变** | 数据团队从「ticket-taking 瓶颈」→「platform enabler 平台赋能者」 |

```text
传统：业务 ──工单──→ 数据团队（瓶颈）──→ 数据
自助：业务（Data Champions）──直接消费──→ 受治理的 Gold 层
                              数据团队 = 维护平台与治理护栏（赋能者）
```

> **前提**：自助化的前提是 [§3 的治理即代码](03-modeling-governance.md#governance-as-code) 已经到位。**没有治理护栏的「开放」是灾难**——会制造口径混乱与数据泄漏。先有 governed，才谈 self-service。

---

## 6.6 本节小结

| 产出物 | 关联 |
|---|---|
| [DataOps mindset](#dataops-mindset) | §3 治理即代码的前提 |
| [DE/AE/BI 三层分工](#role-topology) | §3 Medallion 各层负责人 |
| [选型→能力矩阵](#platform-team-capability-matrix) | §2 PDR / §1 Profile |
| [Embedded/Advisory + Exit](#engagement-model) | §5 退役的对称纪律 |
| [Self-Service + Data Champions](#self-service-enablement) | §3 受控开放 |

> **下一节** → [Section 7 — Day-2 Operations & Platform Governance](07-day2-operations.md)
