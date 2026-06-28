<!-- slug-anchors: greenfield-vs-migration, mvp-platform, migration-strategy, legacy-decommissioning -->

# Section 5 — Migration & Greenfield Strategy

> **角色**：L3 横切方法论 **#3**。覆盖平台起步的两种场景：从零新建（Greenfield）与从旧平台迁移（Migration）。
> **边界**：策略与方法论，**不写具体平台的迁移工具**（那属于 L2）。
> **依赖**：引用 [§3 Medallion / 治理](03-modeling-governance.md) 与 [§4 Landing / 摄取](04-ingestion-pipeline.md) 的定义。
>
> ← [上一节 Section 4](04-ingestion-pipeline.md) · [返回首页](../README.md)

---

<a id="greenfield-vs-migration"></a>
## 5.1 场景分叉：Greenfield vs. Migration

平台起步只有两种根本场景，策略完全不同。开工前必须明确身处哪一种：

| 场景 | 定义 | 核心风险 | 主导策略 |
|---|---|---|---|
| **Greenfield（新建）** | 无既有平台，从零搭建 | 过度工程、范围蔓延、迟迟不产出价值 | [MVP Platform](#mvp-platform) 收敛范围 |
| **Migration（迁移）** | 已有 legacy 平台，需替换 | 切换风险、数据不一致、双账单 | [Domain-Driven + Dual-run](#migration-strategy) |

> **混合场景**：大多数企业是「以 Migration 为主、局部 Greenfield」（旧平台还在跑，但新域直接在新平台建）。此时**两套策略并行**：旧域走迁移纪律，新域走 MVP 纪律。

---

<a id="mvp-platform"></a>
## 5.2 Greenfield：MVP Platform 边界

Greenfield 最大的死法不是技术，是**贪心**——想一次建成完美平台，结果半年没有任何业务可用产出，sponsor 失去耐心。

### MVP Platform 定义

**MVP Platform = 能端到端跑通一个真实业务域、且满足治理底线的最小平台。** 不是「功能阉割版」，是「范围收敛但纵向完整」。

| MVP 必须有（纵向完整） | MVP 可以暂缓（横向扩展） |
|---|---|
| 一条贯通 [Landing→Bronze→Silver→Gold](03-modeling-governance.md#medallion) 的真实链路 | 覆盖所有业务域 |
| 一个真实业务域的可消费 Gold 产品 | 全部历史数据回填 |
| [Governance-as-Code](03-modeling-governance.md#governance-as-code) 的最小门控（脱敏 + 质量测试 + RBAC 骨架） | 全套 observability/FinOps 精细化 |
| 一条可重复的 [metadata-driven 摄取](04-ingestion-pipeline.md#metadata-driven) | 全部源接入 |

> **选域原则**：第一个域用 [§7 Value Heat Map](07-day2-operations.md#sla-slo) 思路选——**高业务价值 × 高跨团队使用**的域优先，尽早证明价值。但避开「最复杂、最多合规纠纷」的域作为首发，那是第二批。

> **关键纪律**：MVP 的治理门控**不能省**。省了治理的 MVP 会变成「先上线后补治理」的承诺，而这个承诺几乎从不兑现，直接转化为 [§3 的治理债](03-modeling-governance.md#governance-as-code)。范围可以收敛，治理底线不能破。

---

<a id="migration-strategy"></a>
## 5.3 Migration：迁移与切换策略 ⭐

> 平台建好后，能否**无缝过渡**，最终决定项目成败。

### 5.3.1 拒绝 Big Bang

> 我**从不**主张「Big Bang」式一次性切换，因其运营风险巨大。取而代之的是**分阶段、领域驱动（Phased, Domain-Driven）** 的迁移策略。

| 方式 | 描述 | 风险 |
|---|---|---|
| **Big Bang（一次性切换）** | 某日全量切到新平台 | ❌ 单点全局失败、不可回退、信任一次性押注 |
| **Phased / Domain-Driven（分阶段领域驱动）** | 按业务域/血缘依赖逐步迁移 | ✅ 小步快赢、风险可隔离、可回退 |

### 5.3.2 Domain-Driven Rollout（领域驱动推进）

> 按具体**业务域**（如先财务、后销售）或按**数据血缘依赖**迁移。这让我们能在小而可控的迭代中拿下 quick wins。

| 排序依据 | 做法 |
|---|---|
| **按业务域** | 用 [§1.3 的「域 → Data Owner」表](01-strategic-alignment.md#governance-identification)，先迁 owner 明确、价值高的域 |
| **按血缘依赖** | 上游基础数据先迁，下游依赖随后，避免跨平台来回依赖 |

### 5.3.3 Dual Running + 自动对账（Reconciliation）⭐

> 对业务关键或监管报送，legacy 与新平台**并行运行（dual running）** 一段时间。期间构建**自动数据对账引擎**，交叉校验两套环境的底层数据与最终指标。**只有连续多个财务周期达到零方差（zero variance），才把利益相关者与审计方的信任迁移过来。**

```text
       ┌─ Legacy 平台 ──→ 指标 A（旧）─┐
源数据 ─┤                              ├─→ 自动对账引擎 ─→ 方差报告
       └─ 新平台 ──────→ 指标 A（新）─┘                      │
                                                  连续 N 个周期零方差？
                                                    │是           │否
                                                    ▼            ▼
                                            迁移信任 / 准备切换   定位差异 → 修复 → 重对账
```

| 对账要素 | 说明 |
|---|---|
| **对账层级** | 既比**底层数据**（行级/聚合），也比**最终指标**（业务口径） |
| **零方差门槛** | 不是「接近」，是**连续多个完整业务周期严格零方差** |
| **信任迁移** | 通过零方差验证后，才把 stakeholder/auditor 的信任从旧平台迁到新平台 |
| **自动化** | 对账是**引擎**不是人工 excel 比对，可重复、可审计 |

> 对账依赖 [§1.2 的现状基线](01-strategic-alignment.md#current-state-audit) 作为「正确答案」的参照系，依赖 [§3 Gold 层口径](03-modeling-governance.md#medallion) 作为指标定义的权威。

### 5.3.4 切换（Cutover）

零方差验证通过后，按域执行切换。每个域切换前确认：回退方案就绪、下游消费者已通知、新平台 [SLO](07-day2-operations.md#sla-slo) 已就位。切换是**按域分批**的，不是全局一次。

---

<a id="legacy-decommissioning"></a>
## 5.4 Legacy Decommissioning 作为硬性 KPI ⭐

> 切换成功后，必须执行**硬性时间表**关停 legacy 系统。许多企业迁移在财务上失败，正是因为他们把旧系统**无限期续命**，导致**双重云账单**。我把「Legacy System Decommissioning（旧系统退役）」当作项目完成的**不可商量的 KPI**。

| 反模式 | 正解 |
|---|---|
| 旧系统「先留着以防万一」，无限期续命 | 切换即设**硬退役时间表**，到期强制关停 |
| 退役无人负责、无截止 | 退役是**项目完成的 KPI**，未退役 = 项目未完成 |
| 双平台并行成常态 | dual-run 是**有限期**手段，不是终态 |

> **核心主张**：**迁移项目的「完成」不以新平台上线为准，而以旧平台关停为准。** 只要旧系统还在跑，就还在烧第二份云账单、还在分裂数据信任、还在阻止团队彻底转向新平台。退役 KPI 必须写进项目章程，由 [sponsor](01-strategic-alignment.md#governance-identification) 背书。

---

## 5.5 本节小结

| 产出物 | 关联 |
|---|---|
| [Greenfield/Migration 分叉](#greenfield-vs-migration) | 决定后续策略 |
| [MVP Platform 边界](#mvp-platform) | §7 Value Heat Map 选域 |
| [反 Big Bang + Domain-Driven + 零方差对账](#migration-strategy) | §1 基线 / §3 Gold 口径 |
| [Legacy 退役 KPI](#legacy-decommissioning) | §7 FinOps（消除双账单） |

> **下一节** → [Section 6 — Team Topology & Operating Structure](06-team-topology.md)
