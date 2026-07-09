<!-- slug-anchors: okr-alignment, current-state-audit, governance-identification, constraint-classification, requirements-profile -->

# Section 1 — Strategic Alignment & Discovery

> **角色**：L1 正文起点。把模糊的业务诉求，转成一份可直接喂给选型的结构化输入。
> **产出契约**：[Requirements Profile](#requirements-profile) —— 本节唯一对下游有约束力的输出对象，被 [Section 2](02-platform-selection.md) 逐字段引用。
> **边界**：本节**不做任何平台选型判断**。出现「该选 Snowflake 还是 Databricks」的念头，立刻停下——那是 Section 2 的事。
>
> ← [上一节 Section 0](00-what-this-document-is.md) · [返回首页](../README.md)

---

## 1.0 为什么从战略而非技术开始

> 如果让我从零构建并管理一个企业级数据平台，我**绝不**从技术选型开始，而是从**业务战略**和**现有痛点**开始。

技术选型是 Section 2 的产物，不是起点。从技术开始的项目，典型死法是：买了一个强大的平台，却发现它解决的不是公司真正痛的那个问题——要么过度工程（为不存在的实时需求买了流处理），要么治理缺位（合规要求从未被翻译成架构约束）。

本节的工作，就是在碰任何技术之前，把四件事说清楚，并固化成一份结构化档案：

```text
OKR 对齐 ──→ 现状审计 ──→ 治理结构识别 ──→ 约束分类
   (为什么建)   (现在痛在哪)   (谁拍板/谁负责)    (FR/NFR)
                                                    │
                                                    ↓
                                        Requirements Profile（输出契约）
                                                    │
                                                    ↓
                                            Section 2 选型
```

---

<a id="okr-alignment"></a>
## 1.1 OKR 对齐（Strategic / OKR Alignment）

第一步是厘清公司的 **OKR**：这个平台到底为哪个商业目标服务？

最常见的两类驱动力，会导向**完全不同**的非功能性要求：

| 驱动力 | 典型 OKR 表述 | 对平台的隐含要求 |
|---|---|---|
| **加速商业决策** | "把核心指标的决策延迟从 T+1 降到小时级" | 低延迟、自助分析、指标一致性 |
| **满足强监管合规** | "满足 APRA / 银行保险业监管报送要求" | 审计可追溯、访问控制、数据血缘、脱敏 |

> **关键动作**：把每条 OKR 翻译成一句「平台必须能……」的能力声明。这句声明，就是后面 FR/NFR 和 Requirements Profile 的源头。一条无法翻译成平台能力声明的 OKR，说明它与本平台无关，应当被排除，避免范围蔓延。

**反模式**：跳过 OKR、直接收集「各部门想要什么功能」。功能清单没有优先级、互相矛盾，且无法回答「不做会怎样」。OKR 提供的是**取舍依据**。

---

<a id="current-state-audit"></a>
## 1.2 现状 Bottleneck 审计（Current-State Audit）

诊断当前瓶颈，把「大家都觉得现在很烂」变成一份可量化的清单。审计沿四个维度展开：

| 维度 | 审计问题 | 量化指标示例 |
|---|---|---|
| **延迟 / 时效（Latency）** | 数据从产生到可用要多久？ | 端到端 freshness、报表 T+N |
| **一致性（Consistency）** | 同一指标各部门口径是否一致？ | 同名指标的多版本数量、口径冲突工单数 |
| **成本（Cost）** | 计算/存储成本趋势？是否失控？ | 月度 compute 账单增速、单查询成本 |
| **可信度 / 质量（Trust）** | 业务是否信任数据？破图频率？ | 数据事故数/月、dashboard 投诉数 |

> **关键动作**：每个瓶颈都要落到一个**当前基线数值**。没有基线，迁移完成后就无法证明价值（Section 5 的零方差验证、Section 7 的 SLO 都依赖这里的基线）。

**审计的两个副产物**（后续章节会用）：

- **痛点 → OKR 映射**：确认每个瓶颈确实卡住了某条 OKR；卡不住任何 OKR 的「痛点」降优先级。
- **隐性治理债（Hidden Governance Debt）线索**：审计时若发现「没人知道这张表谁在用」「PII 散落在多处」，记下——这是 [Section 3 治理即代码](03-modeling-governance.md#governance-as-code) 要偿还的债。

---

<a id="governance-identification"></a>
## 1.3 治理结构识别（Governance & Ownership）

平台不是技术项目，是**组织项目**。开工前必须识别清楚「谁拍板、谁负责、谁担责」：

| 角色 | 定义 | 不清晰的后果 |
|---|---|---|
| **Executive Sponsor** | 为平台买单、能跨部门协调资源、能背 OKR 的高管 | 没有 sponsor 的平台在第一次预算审查时死亡 |
| **Data Owner（按域）** | 每个业务域（财务/销售/…）数据的业务负责人 | 没有 owner，数据质量无人担责，治理无法落地 |
| **Data Steward** | owner 授权下的日常数据管理执行者 | 缺位则治理规则有人定无人守 |
| **Platform Team** | 建设与运维平台本身的工程团队（详见 [Section 6](06-team-topology.md)） | 与 owner 边界不清则陷入 ad-hoc 请求泥潭 |

> **关键动作**：产出一张 **RACI** 或至少一张「域 → Data Owner」对照表。这张表直接决定 [Section 5 的 Domain-Driven 迁移顺序](05-migration-greenfield.md#migration-strategy)（按域迁移，先迁有明确 owner 的域）和 [Section 3 的 RBAC 设计](03-modeling-governance.md#governance-as-code)。

---

<a id="constraint-classification"></a>
## 1.4 约束分类框架（Constraint Classification）

把前三步的洞察，翻译成 **Functional Requirements (FR)** 与 **Non-Functional Requirements (NFR)**。这是从「业务语言」到「架构语言」的关键转换。

### 1.4.1 FR / NFR 第一轴

| 类型 | 定义 | 数据平台场景示例 |
|---|---|---|
| **FR（功能性）** | 平台要**做什么** | 支持自助 BI、支持指标 X 的口径计算、对外提供 API |
| **NFR（非功能性）** | 平台要做得**多好** | 数据安全、高并发、延迟上界、可用性 SLA、可审计性 |

### 1.4.2 第二轴：Machine-Enforced vs. Human-Enforced（关键区分轴）

仅区分 FR/NFR 不够。每条约束还要标注它**靠什么保证**——这条轴线直接决定它在 Section 3/7 里以什么形态落地：

| 强制方式 | 定义 | 落地形态 | 示例 |
|---|---|---|---|
| **Machine-Enforced（机器强制）** | 由代码/CI/平台策略自动保证，违反则被阻断 | [Governance-as-Code](03-modeling-governance.md#governance-as-code)、CI 门控、Masking Policy | "PII 字段在 Bronze 必须脱敏" → CI 检查 tag |
| **Human-Enforced（人工强制）** | 靠流程、评审、培训保证，违反靠人发现 | SOP、评审会、培训 | "重大模型变更需架构评审" |

> **核心主张**：**能 machine-enforce 的，绝不留给 human-enforce。** 人工强制的约束，往往随时间被违反——评审会遗漏、流程被绕过、人员会更替。本轴线的产物，是给 [Section 3 治理即代码](03-modeling-governance.md#governance-as-code) 的一份「哪些约束必须自动化」的清单。

> **关键动作**：每条 NFR 标注 `[machine|human]`。所有标 `machine` 的，进入 Section 3 的 CI/CD 治理实现范围。

---

<a id="requirements-profile"></a>
## 1.5 Requirements Profile —— 本节输出契约 ⭐

> 这是 Section 1 **唯一**对下游有约束力的产出。Section 2 的[六维评估](02-platform-selection.md#six-dimension-evaluation)逐字段消费它。字段名是契约，下游必须用同名引用，不得改名。

### 1.5.1 字段定义

| 字段 | 取值（枚举） | 来源 | 在 Section 2 的用途 |
|---|---|---|---|
| `workload_type` | `analytical-bi` / `ai-ml-centric` / `mixed` / `serving-api` | OKR + 现状审计 | 决定 OLAP 引擎类型与是否需独立 serving 层 |
| `team_capability_ceiling` | `low-sql-only` / `mid-sql-plus-python` / `high-software-engineering` | 团队现状（Section 6 详评） | 决定平台可接受的运维/编码复杂度上界 |
| `governance_maturity` | `ad-hoc` / `defined` / `regulated` | 治理识别 + 合规驱动 | 决定治理特性强度（审计/脱敏/血缘） |
| `streaming_need` | `none` / `near-real-time` / `true-streaming` | OKR 的延迟要求 | 决定是否需流式架构（见 §4） |
| `cloud_lock_in_tolerance` | `single-cloud-ok` / `prefer-portable` / `multi-cloud-required` | 企业云战略 + 监管 | 决定 lock-in 维度评分 |
| `compliance_regime` | `none` / `pii-only`（如 GDPR 类通用隐私法） / `sector-regulated`（如 APRA/HIPAA/PCI DSS） | 合规驱动 | 约束选型的硬门槛（一票否决项） |
| `cost_sensitivity` | `cost-leading` / `balanced` / `capability-leading` | 现状成本审计 + sponsor 取向 | 决定 FinOps/TCO 在评估中的权重 |

> 前 5 个字段是 TASK_BRIEF 明确要求的核心字段；`compliance_regime` 与 `cost_sensitivity` 作为高频决定性字段补充进契约。

### 1.5.2 输出模板（可直接复制填写）

```yaml
# Requirements Profile —— Section 1 输出，Section 2 输入
requirements_profile:
  workload_type:            analytical-bi        # analytical-bi | ai-ml-centric | mixed | serving-api
  team_capability_ceiling:  mid-sql-plus-python  # low-sql-only | mid-sql-plus-python | high-software-engineering
  governance_maturity:      regulated            # ad-hoc | defined | regulated
  streaming_need:           near-real-time       # none | near-real-time | true-streaming
  cloud_lock_in_tolerance:  single-cloud-ok      # single-cloud-ok | prefer-portable | multi-cloud-required
  compliance_regime:        sector-regulated     # none | pii-only | sector-regulated
  cost_sensitivity:         balanced             # cost-leading | balanced | capability-leading

  # 附：可追溯性（非选型输入，但供后续章节引用）
  drivers:
    - okr: "把核心财务指标决策延迟从 T+1 降到小时级"
      maps_to: [workload_type, streaming_need]
  baselines:        # 来自 §1.2 审计，供 §5 零方差 / §7 SLO 引用
    report_freshness: "T+1"
    monthly_compute_growth: "18% MoM"
  machine_enforced_constraints:   # 来自 §1.4.2，供 §3 治理实现
    - "PII 字段在 Bronze 必须脱敏"
    - "Gold 层指标变更必须过 dbt 测试"
```

> **填写纪律**：每个枚举值必须能追溯到 §1.1–1.4 的某个具体发现。填不出来源的字段，说明 discovery 没做够，不要拍脑袋填。

---

## 1.6 本节小结

| 产出物 | 去向 |
|---|---|
| OKR → 平台能力声明 | 贯穿全文的「为什么」 |
| 量化的现状基线 | §5 零方差验证、§7 SLO |
| 域 → Data Owner 表 | §5 迁移顺序、§3 RBAC、§6 团队 |
| machine-enforced 约束清单 | §3 治理即代码 |
| **Requirements Profile** | **§2 六维评估（核心契约）** |

> **下一节** → [Section 2 — Platform Selection & Architecture Decision Framework](02-platform-selection.md)
