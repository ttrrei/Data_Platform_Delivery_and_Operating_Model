<!-- slug-anchors: sla-slo, value-heat-map, finops, data-observability, incident-response, platform-evolution -->

# Section 7 — Day-2 Operations & Platform Governance

> **Role**: L3 cross-cutting methodology **#5**. Continuous operation and governance after the platform goes live—once architecture, migration, and teams are in place, **long-term operations determine whether the platform lives or dies**.
> **Boundaries**: Principles + a comparison of platform-specific mechanisms; **it does not cover the configuration of specific monitoring tools** (that belongs to L2).
> **Dependencies**: References the [Data Product definition in §3](03-modeling-governance.md#data-productization) and the [ingestion artifacts of §4](04-ingestion-pipeline.md).
>
> ← [Previous Section 6](06-team-topology.md) · [Back to index](../README.md)

---

<a id="sla-slo"></a>
## 7.1 Value Prioritization & the SLA / SLO Framework

<a id="value-heat-map"></a>
### 7.1.1 Value Heat Map (Grab the Quick Wins First)

> In the early delivery phase, I use a **Heat Map** of "**business value × cross-team usage**" to prioritize high-impact, cross-functional data assets, delivering immediate value to stakeholders as early as possible.

| | Single-team usage | Multi-team usage |
|---|---|---|
| **High business value** | Important but localized; second batch | 🔥 **Top priority** (quick win, high cross-functional impact) |
| **Low business value** | Lowest priority | Caution: broadly used but low value; confirm the real need first |

> This map simultaneously drives [§5 MVP domain selection](05-migration-greenfield.md#mvp-platform) (launch first with the domains in the 🔥 quadrant) and the prioritization of Day-2 operational investment.

### 7.1.2 SLA / SLO Definition Framework ⭐

Define measurable service objectives for each [Data Product](03-modeling-governance.md#data-productization). Distinguish SLO (internal target) from SLA (the commitment to consumers):

| Dimension | Metric definition | Example SLO |
|---|---|---|
| **Freshness** | How current the data is; end-to-end latency | "The Gold finance mart completes its refresh before 08:00 daily" |
| **Uptime / Availability** | The proportion of time the platform/critical datasets are available | "Core Gold datasets have ≥ 99.5% monthly availability" |
| **Query Performance** | Response time of critical queries/reports | "Core dashboard p95 query < 5s" |

> **Principle**: An SLO must be **measurable, have a baseline, and be bound to a specific Data Product**. The baseline comes from the [§1.2 current-state audit](01-strategic-alignment.md#current-state-audit) (in a migration scenario, the new platform's SLO should be no worse than the old platform's baseline). The SLO is the target value for [observability](#data-observability) monitoring, and also the basis for [incident](#incident-response) severity grading.

---

<a id="finops"></a>
## 7.2 FinOps Cost Governance ⭐

> After go-live, establish a rigorous **FinOps** mechanism. At the platform layer, configure **warehouse-level resource monitoring, strict auto-suspend policies, and real-time anomaly alerting** to prevent runaway compute bills.
>
> (FinOps is an established industry practice for cloud cost management (see the FinOps Foundation); this section takes its technology-agnostic principles and lands them on the data platform.)

### 7.2.1 The Three FinOps Principles (technology-agnostic)

| Principle | Description | Related to |
|---|---|---|
| **Resource visibility + attribution** | Attribute cost by domain/team/product—whoever spends it, sees it | [§1.3 ownership](01-strategic-alignment.md#governance-identification) |
| **Idle means shutdown (auto-suspend)** | Compute resources auto-suspend when idle; don't pay for idling | `cost_sensitivity` field |
| **Limits + anomaly alerting** | Set resource caps/budgets; alert in real time when thresholds are exceeded and enable circuit-breaking | [incident](#incident-response) |

> **Interplay with migration**: FinOps's single largest saving is often the [§5 Legacy decommissioning](05-migration-greenfield.md#legacy-decommissioning)—eliminating double billing. FinOps governance that fails to drive the retirement of the old system is like lavishly renovating a house on which you are still paying two rents.

### 7.2.2 FinOps Mechanism Differences Across Platforms (annex)

> Annex, not the main text. The principles are consistent, the mechanisms differ; for details see [L2](02-platform-selection.md#distribution-mapping).

| Mechanism | Snowflake | Databricks | BigQuery |
|---|---|---|---|
| **Idle shutdown** | Warehouse auto-suspend | Cluster auto-termination | Serverless (the pay-per-use model is inherently free of idle charges; the baseline idle time of reserved slots is still billed) |
| **Limits** | Resource Monitors | Budget / cluster policies | Quotas / reserved slots / pay-per-use caps |
| **Cost attribution** | Warehouse + query tagging | Cluster tags / system tables | Labels + billing export |
| **Elastic TCO optimization** | multi-cluster auto-scaling | autoscaling clusters | automatic slot scheduling |

---

<a id="data-observability"></a>
## 7.3 Data Observability ⭐

> Production management **cannot rely on static tests alone**. We deploy a **Data Observability** framework that monitors upstream schema changes, data downtime, and data drift, ensuring the engineering team **proactively intercepts and resolves** data-quality issues before executives see a broken chart.

### 7.3.1 The Four Pillars of Monitoring

| Pillar | What it monitors | Signal source |
|---|---|---|
| **Freshness** | Whether data arrives on time | Compared against the [§7.1 freshness SLO](#sla-slo) |
| **Schema (structural drift)** | Whether the upstream schema has changed/broken downstream | Earliest capture point = [§4 parse-time discipline](04-ingestion-pipeline.md#metadata-driven) |
| **Volume** | Whether row counts/data size are anomalous (spikes/plunges) | Ingestion batch statistics |
| **Downtime / Quality** | Whether data has stopped updating and whether quality/distribution has drifted and degraded (data drift) | Quality tests + distribution baseline comparison + pipeline status |

> Note: A common industry "five-pillar" framework breaks out Distribution (distribution drift) as a fifth pillar; this framework folds it into the Downtime/Quality pillar, monitoring the same subjects.

> **Core assertion**: **static testing ≠ observability.** The [§3 dbt tests](03-modeling-governance.md#governance-as-code) catch **known** bad data at CI time; observability continuously catches **unknown** anomalies in production (especially upstream schema/volume drift). The two are complementary and neither can be omitted. The goal of observability is **proactive interception**—detecting and responding **before** an executive sees a broken dashboard.

---

<a id="incident-response"></a>
## 7.4 Incident Response & Escalation

Once observability detects an anomaly, a response mechanism is needed to turn "detection" into "resolution."

### 7.4.1 Incident Severity Grading

| Level | Definition | Response |
|---|---|---|
| **SEV-1** | A core Data Product is unavailable / regulatory reporting is affected / erroneous data has already leaked into decisions | Respond immediately, pull in the owner + sponsor, be able to roll back |
| **SEV-2** | An important dataset is delayed/quality-degraded but has not leaked | On-call response, time-boxed fix |
| **SEV-3** | Localized, non-critical, can be scheduled for fixing | Goes into the backlog |

> The grading is based on the [§7.1 SLO](#sla-slo) and [§1.3 data ownership](01-strategic-alignment.md#governance-identification) (whose domain and whose product determine the escalation path).

### 7.4.2 RCA (Root Cause Analysis)

| Principle | Description |
|---|---|
| **Blameless** | The retrospective is about the issue, not the person; the goal is systemic improvement |
| **Root cause, not symptom** | Trace to the root cause (e.g., "a source's schema drift was not intercepted at parse-time"), not stopping at "just rerun it" |
| **Convert into a gate** | Every RCA produces at least one new **machine-enforceable** gate (echoing [§3 Governance-as-Code](03-modeling-governance.md#governance-as-code)), so the same class of incident never recurs |

> **Closed loop**: incident → RCA → new [Governance-as-Code](03-modeling-governance.md#governance-as-code) gate / [observability](#data-observability) monitor → recurrence prevention. This is the core loop by which the platform **hardens itself**.

---

<a id="platform-evolution"></a>
## 7.5 Platform Evolution & Version Management

The platform is not in its final state the moment it goes live. Upstream runtime upgrades, capability evolution, and breaking changes need to be managed, and **linked to L2**.

| Item | Approach | Linkage |
|---|---|---|
| **Upstream runtime upgrades** | Roll out platform version/engine upgrades via canary + regression testing; don't blindly chase the new | [§6 DataOps CI/CD](06-team-topology.md#dataops-mindset) |
| **Breaking change management** | A breaking change to a platform or cross-cutting principle → bump the L1 version tag | [`anchors.md`](../../cn/anchors.md) version anchoring |
| **Linkage to L2** | When an L1 cross-cutting anchor changes, notify all L2 Playbooks that reference it to sync | [Portfolio rule 3](00-what-this-document-is.md#portfolio-constitution) |
| **Periodic selection review** | Periodically revisit the [§2 PDR](02-platform-selection.md#platform-decision-record) to confirm the selection assumptions still hold | §2 one-way-door review |

> **Closed loop with the Portfolio constitution**: whenever any L1 slug registered in [`anchors.md`](../../cn/anchors.md) undergoes a breaking change, the version tag must be bumped and L2 notified—this is the concrete Day-2 execution of [§0 rule 3](00-what-this-document-is.md#portfolio-constitution). If platform evolution does not link to document versioning, cross-repo references will quietly rot into dead links.

---

## 7.6 Section Summary

| Deliverable | Related to |
|---|---|
| [Value Heat Map](#value-heat-map) | §5 MVP domain selection |
| [SLA/SLO framework](#sla-slo) | §3 Data Product / §1 baseline |
| [Three FinOps principles + platform differences](#finops) | §5 decommissioning / §1 cost_sensitivity |
| [Four observability pillars](#data-observability) | §3 tests / §4 parse-time |
| [Incident + RCA closed loop](#incident-response) | §3 Governance-as-Code |
| [Platform evolution & version linkage](#platform-evolution) | §0 Portfolio constitution / anchors |

---

## 7.7 Full-Document Closed Loop

At this point, L1 completes a full lifecycle closed loop:

```text
§1 Why build ──→ §2 What to choose ──→ §3 How to model & govern ──→ §4 How to ingest
                                                                           │
§7 How to stay alive long-term ←── §6 Who operates ←── §5 How to migrate & launch ←┘
   │
   └─→ RCA / evolution feeds back to §2 selection review + §3 new gates (self-hardening loop)
```

> **Return** → [Back to index](../README.md) · [Section 0 constitution](00-what-this-document-is.md) · [Anchor registry](../../cn/anchors.md)
