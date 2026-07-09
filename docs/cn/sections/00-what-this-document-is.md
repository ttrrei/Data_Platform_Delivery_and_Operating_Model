<!-- slug-anchors: portfolio-constitution, three-layer-structure -->

# Section 0 — What This Document Is

> **角色**：Portfolio 宪法。本节定义整套文档体系的边界、分层与不可破坏的协作规则。
> 它不讲数据平台，它讲「这套讲数据平台的文档」本身怎么组织。
>
> ← [返回中文版首页](../README.md) · 锚点登记：[`anchors.md`](../anchors.md)

---

## 0.1 文档的唯一目的

这套文档回答**一个**问题：

> **不管底层用什么技术，一个企业数据平台如何从「为什么建」走到「如何长期健康地活下去」。**

它是 **L1 — technology-agnostic 顶层框架**：覆盖一个数据平台从战略对齐、选型、建模治理、摄取、迁移、团队到 Day-2 运营的完整 **lifecycle**。

它刻意**不**回答的问题（属于 L2 / L3）：

| 不在本文档 | 归属 |
|---|---|
| 某个平台的具体架构怎么画 | L2 Playbook |
| 某个平台的 SQL / Spark / DDL 怎么写 | L2 Playbook |
| 某个监控/编排工具怎么配置 | L2 Playbook |

> 一句话边界：**平台选型只是 [Section 2](02-platform-selection.md) 的一个输入变量，不是本文档的主题。**

---

<a id="three-layer-structure"></a>
## 0.2 三层结构（Three-Layer Structure）

整套知识体系分三层，职责严格分离：

| 层 | 名称 | 内容 | 形态 |
|---|---|---|---|
| **L1** | Data Platform Delivery & Operating Model | technology-agnostic 的 lifecycle 与方法论 | 本 repo |
| **L2** | Platform Playbooks | 单平台的架构蓝图与实现细节（Snowflake / Databricks / BigQuery …） | 各自独立 repo |
| **L3** | 横切方法论（Cross-cutting Methodology） | Medallion、Governance-as-Code、Ingestion、Migration、Team、Day-2 等被所有平台共享的原则 | **内嵌于 L1 的 Section 3–7**（不单独成 repo） |

```text
L1  Data Platform Delivery & Operating Model   ← 本 repo（technology-agnostic）
      Section 2 = 选型分发路由器
         │  跨 repo 外链分发
         ├──────────────────┬──────────────────┐
         ↓                  ↓                  ↓
L2  Snowflake          Databricks         BigQuery
    Playbook           Playbook           Playbook
         └──────────────────┴──────────────────┘
                          ↓ 全部引用
L3  横切方法论（内嵌于 L1 Section 3/4/5/6/7）
```

**为什么 L3 内嵌而非独立**：横切方法论与 lifecycle 叙事高度交织（例如「迁移」必然引用「Medallion 分层」），强行拆成第三个 repo 会制造跨 repo 的双向依赖与版本地狱。内嵌让 L1 成为横切方法论的**唯一权威源**，L2 单向引用即可。

---

<a id="portfolio-constitution"></a>
## 0.3 Portfolio Constitution — 三条强制规则

整套体系能长期可维护、不腐化，靠且仅靠这三条规则。它们是「宪法」，任何章节、任何 L2 都不得违反。

### 规则 1 — L1 定义原则，L2 只写差异

任何 **technology-agnostic** 的方法论，只在 L1 定义**一次**。L2 引用 L1，只补「该平台与通用原则的实现差异」，**不重讲原理**。

> 例：「Bronze 层必须脱敏」是原则，定义在 [Section 3](03-modeling-governance.md#governance-as-code)。Snowflake Playbook 不重复这句话，只写「在 Snowflake 用 Dynamic Masking Policy + Tag 实现 Bronze 脱敏」这一**差异**。

### 规则 2 — 横切章节是唯一权威源（Single Source of Truth）

当 L1 横切章节与某个 L2 的表述**冲突**时，**以 L1 为准**。L2 若发现 L1 原则不适用，正确做法是提 issue 修订 L1，而不是在 L2 里私自改写原则。

### 规则 3 — 跨 repo 引用必须版本锚定（Version-Anchored Reference）

L2 外链 L1 横切章节时，**必须**引用带版本 tag 的稳定锚点：

```text
✅  L1@v1.2#governance-as-code      ← 锚定版本，稳定
❌  .../main/03-modeling.md          ← 链 main 浮动内容，随时会断
```

所有可被引用的锚点登记在 [`anchors.md`](../anchors.md)。**改一个已登记的 slug = breaking change**，必须升 L1 的版本 tag 并在 anchors 的 Deprecated 区留记录。

> **当前状态（成熟度）**：本文档为 `v0.1-draft`，其 git tag 待 CN 收口合并 `main` 后创建。tag 存在之前，上述版本锚定格式尚不可解析，L2 应**暂缓**按 `L1@<tag>#<slug>` 引用（详见 [`anchors.md`](../anchors.md) 发版说明与 [`CHANGELOG`](../../../CHANGELOG.md)）。这套跨 repo 契约机制目前**已设计、待随 L2 落地逐步铺开**——本文档在单仓库内即完整可用。

---

## 0.4 阅读路径

| 你的目标 | 路径 |
|---|---|
| 理解整体方法论 / 推动新平台 0→1 | Section 1 → 7 顺序读 |
| 已定平台，只看架构 | 读 [Section 2 分发映射](02-platform-selection.md#distribution-mapping) → 跳对应 L2 |
| 写 / 维护某个 L2 | 先读 Section 3 / 4（横切核心），按 `anchors.md` 引用 |

---

## 0.5 贯穿全文的核心契约

下游章节互相依赖的结构化对象，集中登记于此，避免各章重复定义：

| 契约对象 | 定义于 | 被引用于 |
|---|---|---|
| **Requirements Profile** | [§1](01-strategic-alignment.md#requirements-profile) | §2 |
| **Medallion 三层职责** | [§3](03-modeling-governance.md#medallion) | §2 / §4 / §5 / §7 |
| **Governance-as-Code** | [§3](03-modeling-governance.md#governance-as-code) | §2 / §5 / §7 |
| **Landing Layer** | [§4](04-ingestion-pipeline.md#landing-layer) | §2 / §5 |
| **Platform Decision Record** | [§2](02-platform-selection.md#platform-decision-record) | §6 |
| **Value Heat Map** | [§7](07-day2-operations.md#value-heat-map) | §5 |

---

## 0.6 范围边界（本文档有意不覆盖）

L1 是**运营模式与生命周期方法论**，不是工程实施手册。以下主题**有意下放**给 L2 或后续版本，本文档不展开——在此显式声明，避免被误读为遗漏：

| 主题 | 归属 | 原因 |
|---|---|---|
| 完整 TCO 测算模型（量化公式） | L2 / 交付期财务建模 | 依赖具体平台计价与用量；L1 只给[因子清单](02-platform-selection.md#one-way-door)与原则 |
| RBAC / 脱敏以外的安全（网络隔离、密钥与 secrets、加密体系） | L2（平台特定） | 强平台相关；L1 只定[治理即代码](03-modeling-governance.md#governance-as-code)与访问最小化原则 |
| DR / BCP（容灾与业务连续性） | L2 / 平台运维 | 与平台高可用能力强绑定 |
| 源系统数据契约（Data Contract）细则 | L2 / 上游治理 | L1 只在[摄取](04-ingestion-pipeline.md#metadata-driven)侧要求 schema 显式声明与 fail-fast |
| 多区域 / 数据驻留架构 | L2（平台特定） | 由合规区域与平台能力共同决定 |

> 换言之，本文档「完整」指的是**运营模式叙事的完整闭环**（见 [§7.7](07-day2-operations.md#platform-evolution)），而非穷尽所有工程实施细节。

---

> **下一节** → [Section 1 — Strategic Alignment & Discovery](01-strategic-alignment.md)
