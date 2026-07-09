<!-- slug-anchors: landing-layer, ingestion-patterns, near-real-time-vs-streaming, metadata-driven -->

# Section 4 — Ingestion & Pipeline Design

> **Role**: L3 cross-cutting methodology **#2**, referenced by [§2](02-platform-selection.md) / [§5](05-migration-greenfield.md) / [§7](07-day2-operations.md). This section is the **single authoritative source** for the Landing Layer and ingestion patterns.
> **Boundary**: Defines platform-agnostic ingestion/pipeline principles, **not bound to any specific orchestration tool** (the choice between Airflow / dbt / DLT / a native scheduler belongs to L2).
> **Dependency**: References the [Bronze definition in §3](03-modeling-governance.md#medallion).
>
> ← [Previous, Section 3](03-modeling-governance.md) · [Back to index](../README.md)

---

## 4.0 Ingestion Is the Platform's "Digestive System"

The quality of the ingestion layer sets the upper bound on the data trustworthiness of the entire platform. This section answers four questions:

```text
Where does data land first? ────→ [§4.1] Landing Layer (its boundary with Bronze)
How does it get in?          ────→ [§4.2] The three modes: batch / CDC / streaming
How real-time must it be?    ────→ [§4.3] Near-Real-Time vs. True Streaming decision
How to avoid reinventing?    ────→ [§4.4] metadata-driven configuration + parse-time discipline
```

---

<a id="landing-layer"></a>
## 4.1 Landing Layer Design Principles ⭐

Referenced by [§2 architecture principles](02-platform-selection.md#platform-agnostic-architecture) and [§5 migration](05-migration-greenfield.md).

### 4.1.1 The Boundary Between Landing and Bronze

Many teams conflate Landing and Bronze, and this is a common source of governance debt. The two have distinct responsibilities:

| Layer | Responsibility | Form | Part of Medallion? |
|---|---|---|---|
| **Landing** | Catches the source system's **raw bytes**, unparsed and untabulated | Files/objects (e.g., raw payloads in object storage) | No, it is the **precursor** to Bronze |
| **Bronze** (see [§3](03-modeling-governance.md#medallion)) | **Parses Landing's raw data into tables** + compliance masking | Structured tables, append | Yes, the first layer of the Medallion |

> **Boundary principle**: Landing retains a **completely raw, entirely unparsed** copy of the data; structuring begins only at Bronze. This boundary means that a "parsing-logic bug" can be fixed by **replaying Landing alone**, without having to re-extract from the source system.

### 4.1.2 Three Non-Negotiable Design Properties

| Property | Definition | Why It's Non-Negotiable |
|---|---|---|
| **Idempotent** | Ingesting the same batch N times yields the same result as ingesting it once | Retries/failure recovery produce no duplicates or contamination |
| **Replayable** | Any historical batch can be reprocessed | A prerequisite for parse-logic fixes, backfills, and audit traceability |
| **Immutable & Traceable** | Landing data is append-only, never modified, and carries ingestion metadata (source/time/batch) | The root of audit and lineage, echoing [§3 RBAC audit](03-modeling-governance.md#governance-as-code) |

> **Implementation notes (technology-agnostic)**: Use "source + time window + batch ID" as the idempotency key; write with overwrite-by-partition or merge-on-key to avoid append-induced duplicates; retain the raw payload until downstream confirms consumption.

### 4.1.3 Landing's Security Boundary

Landing stores the **unmasked** raw payload—the [§3 early-masking](03-modeling-governance.md#governance-as-code) point lands in Bronze and does not reach here. Landing must therefore satisfy three mandatory rules of its own:

| Rule | Requirement |
|---|---|
| **Minimized access** | Landing is readable only by the ingestion engine and platform admin roles; business roles have no visibility at all (reusing the [§3 RBAC design](03-modeling-governance.md#governance-as-code)) |
| **Retention policy** | The raw payload is given a retention/cleanup cycle per compliance requirements; "retain until downstream confirms consumption" is a **lower bound**, not indefinite |
| **Tokenize before landing (physical de-identification scenarios)** | If compliance forbids storing raw sensitive values (e.g., PCI for card numbers), runtime dynamic masking does not apply—values must be tokenized **before** writing to Landing, in which case replayability is bounded by the tokenized payload |

---

<a id="ingestion-patterns"></a>
## 4.2 Boundaries of the Three Ingestion Modes (Batch / CDC / Streaming)

Not all data should come in the same way. The three modes have clear boundaries of applicability:

| Mode | Mechanism | When to Use | Cost |
|---|---|---|---|
| **Batch** | Periodic full/incremental extraction | Most analytical workloads, sources without CDC capability, tolerance for T+N | Simple, cheap, high latency |
| **CDC (Change Data Capture)** | Captures insert/update/delete on the source database | Need near-real-time sync of transactional databases, need to retain change history | Moderate complexity, must handle out-of-order events and deletes |
| **Streaming** | Continuous event-stream processing | Truly real-time (second/sub-second), event-driven | High complexity, high operational cost |

> **Default preference**: **If batch will do, don't use CDC; if CDC will do, don't use streaming.** Each step up significantly raises operational complexity and cost. The choice of mode is driven by the downstream **business**'s real demand for latency (from [§1 OKR](01-strategic-alignment.md#okr-alignment) → the Profile's `streaming_need`), not by engineers' preference for "real-time."

---

<a id="near-real-time-vs-streaming"></a>
## 4.3 Near-Real-Time vs. True Streaming Decision Logic ⭐

This is the decision most often derailed by engineering impulse. To distinguish the two:

| | Near-Real-Time | True Streaming |
|---|---|---|
| **Latency magnitude** | Minutes (micro-batch) | Seconds/sub-second |
| **Typical implementation** | High-frequency micro-batch / incremental scheduling | Event-stream engine, continuous processing |
| **Operational cost** | Medium | High (always-on, state management, backpressure) |
| **Applicability** | The vast majority of "the business says it needs real-time" requirements | Genuinely event-driven: risk control, real-time alerting, online features |

### 4.3.1 Decision Tree

```text
What is the business latency requirement?
  │
  ├─ T+N / hourly is acceptable ───────────────→ Batch (§4.2)
  │
  ├─ Minutes suffice for the business action ──→ Near-Real-Time (micro-batch / incremental)
  │
  └─ Seconds, event-driven, a second late = loss ─→ True Streaming
                                          (requires Profile streaming_need = true-streaming
                                            and the business can state "the concrete benefit
                                            that second-level latency brings")
```

> **Core claim**: **"Real-time" is an overrated requirement in most scenarios.** Before choosing True Streaming, force the business to answer: "What concrete money or risk would minute-level latency cost you?" If they can't answer → use near-real-time. This discipline directly affects the streaming-dimension score in [§2 selection](02-platform-selection.md#six-dimension-evaluation) and the [§7 operational cost](07-day2-operations.md#finops).

---

<a id="metadata-driven"></a>
## 4.4 Metadata-Driven Configuration + Parse-Time Discipline ⭐

### 4.4.1 Metadata-Driven Ingestion

Anti-pattern: hand-writing a one-off ingestion script for each data source. With 50 sources you get 50 hard-to-maintain scripts, and adding a source = copy-paste + tweak, tweak, tweak.

The right approach: **abstract ingestion into "configuration + a generic engine."**

| Element | Description |
|---|---|
| **Configuration (Metadata)** | Source connection, schema, extraction mode (batch/CDC), scheduling, idempotency key, masking tags—all declared in config/tables |
| **Generic engine** | One codebase that reads the config, executes ingestion, and is reused across all sources |
| **Adding a source** | = add a line of configuration, **write no new code** |

> **Benefits**: Ingestion logic becomes testable, auditable, and changeable in bulk; adding/retiring a source is a configuration operation rather than an engineering one. The configuration itself goes into version control—this is [Governance-as-Code](03-modeling-governance.md#governance-as-code) manifested on the ingestion side.

### 4.4.2 Parse-Time Discipline

**Key principle: put schema parsing and validation at "parse-time," so bad data fails early and explicitly—rather than sneaking into downstream.**

| Discipline | Practice | Anti-pattern |
|---|---|---|
| **Explicit schema declaration** | Declare the expected schema at ingestion and validate against metadata | Discovering missing fields only at schema-on-read time |
| **Fail-fast** | Schema drift/type mismatch raises an error and is quarantined at parse-time | Bad data silently enters Bronze and contaminates downstream |
| **Bad-data quarantine** | Records that don't meet expectations go to a dead-letter/quarantine area without blocking good data | One bad record takes down the whole batch |

> **Linkage with observability**: Schema drift caught at parse-time is the earliest collection point for the [§7 Data Observability schema-drift signal](07-day2-operations.md#data-observability). Intercepting at parse-time is orders of magnitude cheaper than discovering it only after a dashboard breaks.

---

## 4.5 Section Summary

| Deliverable (authoritative definition) | Referenced by |
|---|---|
| [Landing Layer's three properties](#landing-layer) | §2 / §5 |
| [Boundaries of the three ingestion modes](#ingestion-patterns) | §5 / §7 |
| [near-real-time vs. streaming decision](#near-real-time-vs-streaming) | §2 / §7 |
| [metadata-driven + parse-time discipline](#metadata-driven) | §5 / §7 |

> **Next** → [Section 5 — Migration & Greenfield Strategy](05-migration-greenfield.md)
