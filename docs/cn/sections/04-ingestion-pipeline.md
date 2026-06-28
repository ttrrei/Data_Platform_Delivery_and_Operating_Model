<!-- slug-anchors: landing-layer, ingestion-patterns, near-real-time-vs-streaming, metadata-driven -->

# Section 4 — Ingestion & Pipeline Design

> **角色**：L3 横切方法论 **#2**，被 [§2](02-platform-selection.md) / [§5](05-migration-greenfield.md) / [§7](07-day2-operations.md) 引用。本节是 Landing Layer 与摄取模式的**唯一权威源**。
> **边界**：定义平台无关的摄取/管道原则，**不绑定具体编排工具**（Airflow / dbt / DLT / native scheduler 的选型属于 L2）。
> **依赖**：引用 [§3 的 Bronze 定义](03-modeling-governance.md#medallion)。
>
> ← [上一节 Section 3](03-modeling-governance.md) · [返回首页](../README.md)

---

## 4.0 摄取是平台的「肠胃」

摄取层的质量，决定整个平台的数据可信度上界。本节回答四个问题：

```text
数据进来先落哪？ ─────→ [§4.1] Landing Layer（与 Bronze 的边界）
用什么方式进来？ ─────→ [§4.2] batch / CDC / streaming 三模式
要多实时？        ─────→ [§4.3] near-real-time vs. true streaming 决策
怎么不重复造轮子？ ───→ [§4.4] metadata-driven 配置化 + parse-time discipline
```

---

<a id="landing-layer"></a>
## 4.1 Landing Layer 设计原则 ⭐

被 [§2 架构原则](02-platform-selection.md#platform-agnostic-architecture) 与 [§5 迁移](05-migration-greenfield.md) 引用。

### 4.1.1 Landing 与 Bronze 的边界

很多团队把 Landing 和 Bronze 混为一谈，这是治理债的常见源头。二者职责不同：

| 层 | 职责 | 形态 | 是否进 Medallion |
|---|---|---|---|
| **Landing（着陆区）** | 接住源系统**原始字节**，未解析、未建表 | 文件/对象（如对象存储原始 payload） | 否，是 Bronze 的**前置** |
| **Bronze**（见 [§3](03-modeling-governance.md#medallion)） | 把 Landing 的原始数据**解析落表** + 合规脱敏 | 结构化表、append | 是，Medallion 第一层 |

> **边界原则**：Landing 保留**最原始、未经任何解析**的数据副本；Bronze 才开始结构化。这条边界让「解析逻辑出错」可以**仅重放 Landing**修复，而不必回源系统重抽。

### 4.1.2 三条不可妥协的设计属性

| 属性 | 定义 | 为什么不可妥协 |
|---|---|---|
| **幂等（Idempotent）** | 同一批数据摄取 N 次，结果与 1 次相同 | 重试/故障恢复不会产生重复或污染 |
| **可重放（Replayable）** | 任意历史批次可被重新处理 | 解析逻辑修复、回填、审计追溯的前提 |
| **不可变 + 可追溯（Immutable & Traceable）** | Landing 数据只追加不修改，带摄取元数据（来源/时间/批次） | 审计与血缘的根，呼应 [§3 RBAC 审计](03-modeling-governance.md#governance-as-code) |

> **实现要点（technology-agnostic）**：以「源 + 时间窗 + 批次 ID」为幂等键；写入用 overwrite-by-partition 或 merge-on-key，避免 append 产生重复；保留原始 payload 直到下游确认消费。

---

<a id="ingestion-patterns"></a>
## 4.2 三类摄取模式边界（Batch / CDC / Streaming）

不是所有数据都该用同一种方式进来。三类模式有清晰的适用边界：

| 模式 | 机制 | 适用场景 | 代价 |
|---|---|---|---|
| **Batch（批）** | 周期性全量/增量抽取 | 大多数分析负载、源无 CDC 能力、可容忍 T+N | 简单、便宜、延迟高 |
| **CDC（变更数据捕获）** | 捕获源库的 insert/update/delete | 需近实时同步事务库、需保留变更历史 | 中等复杂度、需处理乱序/删除 |
| **Streaming（流）** | 持续事件流处理 | 真·实时（秒/亚秒级）、事件驱动 | 高复杂度、高运维成本 |

> **默认偏好**：**能 batch 就别 CDC，能 CDC 就别 streaming。** 每升一级，运维复杂度与成本显著上升。模式的选择由下游**业务**对延迟的真实需求决定（来自 [§1 OKR](01-strategic-alignment.md#okr-alignment) → Profile 的 `streaming_need`），而非工程师对「实时」的偏好。

---

<a id="near-real-time-vs-streaming"></a>
## 4.3 Near-Real-Time vs. True Streaming 决策逻辑 ⭐

这是最常被工程冲动带偏的决策。区分二者：

| | Near-Real-Time（近实时） | True Streaming（真流式） |
|---|---|---|
| **延迟量级** | 分钟级（micro-batch） | 秒/亚秒级 |
| **典型实现** | 高频 micro-batch / 增量调度 | 事件流引擎、持续处理 |
| **运维成本** | 中 | 高（常驻、状态管理、背压） |
| **适用** | 绝大多数「业务说要实时」的需求 | 真正事件驱动：风控、实时告警、在线特征 |

### 决策树

```text
业务延迟需求是？
  │
  ├─ T+N / 小时级可接受 ───────────────→ Batch（§4.2）
  │
  ├─ 分钟级即可满足业务动作 ──────────→ Near-Real-Time（micro-batch / 增量）
  │
  └─ 秒级且事件驱动、晚一秒就产生损失 ─→ True Streaming
                                          （需 Profile streaming_need = true-streaming
                                            且业务能说出「秒级延迟带来的具体收益」）
```

> **核心主张**：**「实时」是一种被严重高估的需求。** 在选 true streaming 前，强制业务回答：「分钟级延迟，会让你损失什么具体的钱或风险？」答不出 → 用 near-real-time。这条纪律直接影响 [§2 选型](02-platform-selection.md#six-dimension-evaluation) 的 streaming 维度评分与 [§7 的运维成本](07-day2-operations.md#finops)。

---

<a id="metadata-driven"></a>
## 4.4 Metadata-Driven 配置化 + Parse-Time Discipline ⭐

### 4.4.1 Metadata-Driven 摄取

反模式：为每个数据源手写一份一次性摄取代码。源有 50 个，就有 50 份难维护的脚本，新增源 = 复制粘贴 + 改改改。

正解：**把摄取抽象成「配置 + 通用引擎」**。

| 要素 | 说明 |
|---|---|
| **配置（Metadata）** | 源连接、schema、抽取模式（batch/CDC）、调度、幂等键、脱敏 tag —— 全部声明在配置/表里 |
| **通用引擎** | 一套代码读配置、执行摄取，对所有源复用 |
| **新增源** | = 加一行配置，**不写新代码** |

> **收益**：摄取逻辑可测试、可审计、可批量变更；新增/下线源是配置操作而非工程操作。配置本身进版本控制，是 [Governance-as-Code](03-modeling-governance.md#governance-as-code) 在摄取侧的体现。

### 4.4.2 Parse-Time Discipline（解析期纪律）

**关键原则：把 schema 的解析与校验放在「解析期」，让坏数据尽早、显式地失败——而不是悄悄进入下游。**

| 纪律 | 做法 | 反模式 |
|---|---|---|
| **Schema 显式声明** | 摄取时声明预期 schema，按 metadata 校验 | schema-on-read 时才发现字段缺失 |
| **Fail-fast（早失败）** | schema 漂移/类型不符在解析期就报错并隔离 | 坏数据静默进 Bronze，污染下游 |
| **坏数据隔离（Quarantine）** | 不符合预期的记录进死信/隔离区，不阻塞好数据 | 一条坏记录搞挂整批 |

> **与 observability 的联动**：解析期捕获的 schema 漂移，是 [§7 Data Observability 的 schema drift 信号](07-day2-operations.md#data-observability) 的最早采集点。在解析期拦截，比在 dashboard 破图后才发现便宜几个数量级。

---

## 4.5 本节小结

| 产出物（权威定义） | 被谁引用 |
|---|---|
| [Landing Layer 三属性](#landing-layer) | §2 / §5 |
| [三类摄取模式边界](#ingestion-patterns) | §5 / §7 |
| [near-real-time vs. streaming 决策](#near-real-time-vs-streaming) | §2 / §7 |
| [metadata-driven + parse-time discipline](#metadata-driven) | §5 / §7 |

> **下一节** → [Section 5 — Migration & Greenfield Strategy](05-migration-greenfield.md)
