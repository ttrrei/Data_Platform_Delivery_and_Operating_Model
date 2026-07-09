<!-- slug-anchors: one-way-door, six-dimension-evaluation, platform-decision-record, platform-scenario-mapping, platform-agnostic-architecture, distribution-mapping -->

# Section 2 — Platform Selection & Architecture Decision Framework

> **Role**: the **hub / router** of the entire framework. It maps the [Requirements Profile from Section 1](01-strategic-alignment.md#requirements-profile) into a selection conclusion and **dispatches** the reader to the corresponding L2 Playbook.
> **Boundary**: this section provides a **decision framework**, not the architectural detail of any single platform — "how exactly to build on Snowflake" belongs to L2. This section only decides "which L2 to follow."
> **Dependencies**: upstream [Requirements Profile](01-strategic-alignment.md#requirements-profile); references the [Medallion definition in Section 3](03-modeling-governance.md#medallion).
>
> ← [Previous: Section 1](01-strategic-alignment.md) · [Back to index](../README.md)

---

## 2.0 How This Section Works

```text
Requirements Profile (§1 output)
        │
        ▼
[1] One-Way Door identification ── flag irreversible decisions, raise their review rigor
        │
        ▼
[2] Six-dimension evaluation ──────── score each platform dimension by dimension → Platform Decision Record
        │
        ▼
[3] Scenario mapping table ────────── sanity-check against "representative profiles"
        │
        ▼
[4] Platform-agnostic principles ──── must be followed no matter who is chosen (OLAP/OLTP separation, etc.)
        │
        ▼
[5] Distribution mapping ──────────── route to the corresponding L2 Playbook
```

> **On platform scope**: this section uses **Snowflake / Databricks / BigQuery** as its concrete vehicles, because they cover the mainstream shapes of today's enterprise data platforms (SQL-first warehouse / Lakehouse / serverless). But **the six-dimension evaluation framework itself is technology-agnostic** — swap in Redshift, Microsoft Fabric/Synapse, ClickHouse, an open Iceberg lakehouse, or Postgres, and the same dimensions and scoring still apply; only the candidate set differs. The three platforms are **representative vehicles, not the boundary of the methodology**.

---

<a id="one-way-door"></a>
## 2.1 One-Way Door Decision Framework

> When defining an architectural blueprint, I am extremely wary of **"one-way door decisions"** — those fundamental, strategic choices that are **extraordinarily expensive or nearly impossible to reverse** after the fact.
>
> (The "one-way door / two-way door" classification of decisions originates from Amazon / Jeff Bezos; this section applies it to data-platform architecture and selection decisions.)

### 2.1.1 Definition and Identification

| Type | Definition | Decision Rigor |
|---|---|---|
| **One-Way Door** | A decision whose cost of reversal is extremely high — nearly irreversible | Slow decision, high-rigor review, write an ADR, sponsor endorsement |
| **Two-Way Door** | A decision that can be rolled back at low cost | Fast decision, safe to experiment, delegated to the team |

**To identify whether a decision is a one-way door, ask three questions:**

1. **Exit cost**: if you had to replace it two years from now, how much code would you rewrite, how much data would you migrate, how much trust would you rebuild?
2. **Lock-in radius**: does it lock in other decisions along with it (e.g., choosing a particular cloud locks you into a set of native services)?
3. **Data gravity**: once data settles here, how strong is the gravitational resistance to migrating it out?

> **Methodology**: first sort every architectural decision into two columns — "one-way door / two-way door." **Apply the heavyweight review process only to one-way doors**; fast-fail on two-way doors. Spending your review budget where things are irreversible is the core discipline of architecture governance.

### 2.1.2 Typical One-Way Door Decisions (Data-Platform Domain)

| Decision | Why It's Irreversible | Related Profile Field |
|---|---|---|
| **Core OLAP platform selection** | Data gravity + the entire modeling/pipeline stack bound to it | `workload_type` / `team_capability_ceiling` |
| **Cloud vendor lock-in** | Native-service lock-in, enormous exit cost | `cloud_lock_in_tolerance` |
| **Whether to separate OLAP / OLTP** | Determines the entire shape of the serving architecture (see §2.4) | `workload_type` / `streaming_need` |
| **Compliance edition / region selection** | Regulatory region and audit capability are hard to retrofit later | `compliance_regime` |
| **Core modeling paradigm** | Once Medallion layering is rolled out it is hard to refactor (see §3) | `governance_maturity` |

### 2.1.3 Case Study (Using Snowflake as an Example): Compliance-Driven Edition Selection

> In heavily regulated industries, we lean toward **Snowflake Enterprise Edition**, because it is audit-friendly and strong on security. Its unit price is higher up front, but capabilities such as multi-cluster auto-scaling actually optimize the overall **TCO (Total Cost of Ownership)**.

This illustrates a counterintuitive but critical principle: **one-way door decisions cannot be judged on sticker price alone — you must weigh the combined cost of TCO and irreversibility risk.** Under a `compliance_regime: sector-regulated` profile, a "cheaper but weak-on-audit" edition is a **pseudo-option** — it is eliminated outright on the compliance dimension (see the veto mechanism in §2.2). The edition floor also rises with regulatory intensity: for generally strong-compliance scenarios, Enterprise is the starting point; for hard-regulation scenarios involving private networking, enhanced encryption, and higher compliance certifications (such as core banking systems), the practical floor is often the Business Critical tier.

> **Note**: the edition names above are a Snowflake-specific example, used to illustrate the **technology-agnostic principle** that "compliance is a hard gate, and you must look at TCO rather than sticker price." Move to Databricks or BigQuery and the counterparts are their respective tiers/editions and their network-isolation and encryption options — **the principle is the same, only the specific labels differ**.

### 2.1.4 The Composition of TCO (Not Just Sticker Price)

"Look at TCO, not unit price" has to reduce to verifiable factors. L1 provides a technology-agnostic checklist; the concrete numbers are filled in during delivery for the chosen platform:

| Factor | Description |
|---|---|
| **License / platform fees** | Edition/tier price differences, committed-use discounts |
| **Compute** | Query/job compute, including elastic scaling and concurrency peaks |
| **Storage** | Storage + time travel / snapshots / multi-copy redundancy |
| **Data egress** | Cross-cloud/cross-region transfer fees, frequently underestimated |
| **Operations staffing** | Platform operations + the [hiring/training cost](06-team-topology.md#platform-team-capability-matrix) of team capability gaps (see §6.3) |
| **Migration cost** | One-time inbound migration + the double billing during the [Dual Running](05-migration-greenfield.md#migration-strategy) period (see §5) |
| **Opportunity cost / lock-in** | Exit cost and lock-in risk (the combined cost of a one-way door) |

> **Usage**: TCO is not an account you settle after selection; it is an **input** to the FinOps dimension of the [six-dimension evaluation](#six-dimension-evaluation) and to one-way door decisions. Lowest sticker price ≠ lowest TCO.

---

<a id="six-dimension-evaluation"></a>
## 2.2 Six-Dimension Evaluation

Map the fields of the Requirements Profile onto six evaluation dimensions and score candidate platforms dimension by dimension. The output is a **Platform Decision Record (PDR)**, referenced by the [team capability matrix in Section 6](06-team-topology.md#platform-team-capability-matrix).

### 2.2.1 The Six Dimensions and Their Profile Mapping

| # | Dimension | Evaluation Question | Primary Profile Input |
|---|---|---|---|
| 1 | **Workload** | Do the OLAP/AI-ML/serving workload shapes match the platform's engine? | `workload_type` |
| 2 | **Team** | Can the team's capability ceiling sustain the platform's operational/coding complexity? | `team_capability_ceiling` |
| 3 | **Governance** | Can the platform's audit / masking / lineage / RBAC meet the governance maturity requirement? | `governance_maturity` / `compliance_regime` |
| 4 | **Streaming** | What is the platform's native support for near-real-time / true-streaming? | `streaming_need` |
| 5 | **FinOps** | Cost controllability, TCO, metering and quota mechanisms? | `cost_sensitivity` |
| 6 | **Lock-in** | Does the degree of vendor/cloud binding conflict with the enterprise's portability requirement? | `cloud_lock_in_tolerance` |

### 2.2.2 Scoring Mechanism

- **Veto dimensions (Hard Gate)**: `compliance_regime` and an unacceptable `cloud_lock_in_tolerance` are **hard gates**. Any candidate that cannot satisfy the Profile's hard constraints on the Governance or Lock-in dimension is **eliminated outright** and does not enter the weighted comparison.
- **Weighted scoring**: the remaining dimensions are weighted according to the Profile's orientation. For example: `cost_sensitivity: cost-leading` raises the FinOps weight; `workload_type: ai-ml-centric` raises the Workload weight.
- **Record, don't just score**: each dimension's score must carry **a one-line rationale**, written into the PDR. A score without a rationale is untraceable — which is as good as not having evaluated at all.

<a id="platform-decision-record"></a>
### 2.2.3 Platform Decision Record (PDR) Template

> **Each candidate platform produces its own PDR.** Below are two worked examples — the same evaluation framework yields **different conclusions** under different Requirements Profiles; the examples themselves do not represent a default recommendation.

**Example A — one candidate under an `analytical-bi` + `regulated` profile:**

```yaml
platform_decision_record:
  candidate: Snowflake-Enterprise
  hard_gates:
    compliance_regime: PASS   # Enterprise meets sector-regulated audit requirements
    lock_in:           PASS   # single-cloud-ok, acceptable
  scores:               # 1–5, with rationale; keys are the six dimension names, ↔ Profile field mapping in §2.2.1
    workload:   { score: 5, why: "analytical-bi primary workload, OLAP engine is a natural fit" }
    team:       { score: 5, why: "SQL-first, a mid-capability team can handle it" }
    governance: { score: 5, why: "Dynamic Masking + audit + lineage all present" }
    streaming:  { score: 3, why: "near-real-time is met; true-streaming is weaker" }
    finops:     { score: 4, why: "auto-suspend + resource monitor control cost" }    # ← cost_sensitivity
    lock_in:    { score: 3, why: "moderate platform binding, cross-cloud migration possible but costly" }            # ← cloud_lock_in_tolerance
  decision: SELECTED
  one_way_door: true        # flagged as a one-way door, heavyweight review completed
  routes_to: L2/snowflake-lakehouse-playbook
```

**Example B — switch to an `ai-ml-centric` + `high-software-engineering` profile, and the same framework yields a different conclusion:**

```yaml
platform_decision_record:
  candidate: Databricks
  hard_gates:
    compliance_regime: PASS   # Unity Catalog meets audit/lineage requirements
    lock_in:           PASS   # prefer-portable: Lakehouse + open formats acceptable
  scores:               # 1–5, with rationale
    workload:   { score: 5, why: "ai-ml-centric primary workload, Spark + MLflow are a natural fit" }
    team:       { score: 4, why: "high-software-engineering team, can handle clusters/notebooks" }
    governance: { score: 4, why: "Unity Catalog governance is solid; fine-grained masking needs extra configuration" }
    streaming:  { score: 5, why: "Structured Streaming natively supports true-streaming" }
    finops:     { score: 3, why: "cluster cost requires strict governance via autoscaling + cluster policy" }
    lock_in:    { score: 4, why: "Delta / Iceberg open formats lower the exit cost" }
  decision: SELECTED
  one_way_door: true
  routes_to: L2/databricks-ai-ml-playbook
```

> The contrast between the two PDRs makes one point clear: **the framework is neutral, and the conclusion is driven by the Profile** — `analytical-bi + regulated` points to Snowflake, `ai-ml-centric + a strong engineering team` points to Databricks. Same dimensions, different weights and scores.

> The PDR is the ADR (Architecture Decision Record) for the **one-way door** that is platform selection. It must be archived, versioned, and revisited during the Day-2 retrospective (§7).

---

<a id="platform-scenario-mapping"></a>
## 2.3 Three-Platform Scenario Mapping Table

> ⚠️ **Disclaimer: the following are "representative profiles," not absolute boundaries.** The three platforms overlap heavily in capability; any one of them could, at a stretch, do another's job. The table below gives "under this profile, which platform is the path of least resistance as a default" — **not** "only it can do this." Real selection is governed by the six-dimension evaluation in §2.2; this table is only a sanity check.

| Representative Profile | Default Direction | One-Line Rationale | Route to L2 |
|---|---|---|---|
| `workload_type: analytical-bi` + `team_capability_ceiling: low~mid` + `governance_maturity: regulated` + `streaming_need: none~near-real-time` | **Snowflake** | SQL-first, low operations, mature audit governance — the least-resistance path for low-complexity near-real-time analytics | [→ §2.5](#distribution-mapping) |
| `workload_type: ai-ml-centric` + `team_capability_ceiling: high-software-engineering` + needs unified ML / data engineering | **Databricks** | Lakehouse + Spark + MLflow, for AI/ML-centric scenarios that need code flexibility | [→ §2.5](#distribution-mapping) |
| Already deeply bound to GCP + prefers serverless + `cost_sensitivity` sensitive to idle cost | **BigQuery** | GCP-native, serverless, pay-per-use, no cluster management required | [→ §2.5](#distribution-mapping) |

> **How to use this table**: after completing the six-dimension evaluation and arriving at a candidate, look back at this table to confirm "whether my profile aligns with the default direction." **A mismatch does not mean the choice is wrong — it requires the PDR to give an explicit deviation rationale** (for example, "the profile leans BI but we still chose Databricks, because there is a clear ML roadmap within two years" — a reasonable deviation).

---

<a id="platform-agnostic-architecture"></a>
## 2.4 Platform-Agnostic Architecture

**No matter which platform the six-dimension evaluation selects, the following principles must be followed.** They are the technology-agnostic architectural foundation.

### 2.4.1 Separate OLAP from OLTP (The Most Important One-Way Door)

> Another non-negotiable one-way door decision: **never use an analytical warehouse (such as Snowflake) to directly serve high-concurrency, low-latency external APIs.**

An analytical platform is a world-class **OLAP (analytics)** engine, but forcing it to handle row-level, high-frequency transactional queries (**OLTP** behavior) is **extraordinarily inefficient and lets cost run out of control**. Always separate OLAP from OLTP, **even if it means introducing an extra architectural layer**:

```text
        ┌─────────────── OLAP (heavy-compute zone) ───────────────┐
Source systems ─→ Landing ─→ Bronze ─→ Silver ─→ Gold (modeling/aggregation)
                                              │
                                              │  pipeline results pushed down
                                              ▼
        ┌────────────── Serving Layer (OLTP/low-latency) ──────────────┐
        │  DynamoDB / managed PostgreSQL / Redis, etc.             │
        │  ← from here, it powers high-concurrency, low-latency downstream APIs │
        └──────────────────────────────────────────────────────────┘
```

| Zone | Engine Type | Responsibility | Anti-Pattern |
|---|---|---|---|
| **Analytics zone** | OLAP (warehouse/Lakehouse) | Heavy modeling, large aggregations, batch / near-real-time | ❌ Directly serving high-frequency external APIs |
| **Serving zone (Serving Layer)** | OLTP/KV (DynamoDB / managed PostgreSQL …) | Low-latency, high-concurrency point lookups | ❌ Running large-scope analytical scans here |

> **Principle**: use the OLAP platform for heavy data modeling and aggregation, and push the **results** down through a pipeline to a serving layer that powers the APIs. This guarantees long-term **system health** and **cost predictability**. This separation is strongly correlated with the `workload_type: serving-api` field — if the Profile contains a serving need, the serving layer is a **mandatory item**, not an option.

### 2.4.2 Landing Layer and Medallion Responsibilities (Referenced, Not Redefined)

- The design principles of the **Landing Layer** (its boundary with Bronze, idempotency, replayability) are defined in [Section 4](04-ingestion-pipeline.md#landing-layer); this section only declares that it is the entry layer of any architecture.
- The **three-layer responsibilities of Medallion (Bronze/Silver/Gold)** are defined in [Section 3](03-modeling-governance.md#medallion); this section does not repeat them, and only references its layering in the diagram above.

> This is an expression of [Portfolio Rule 1](00-what-this-document-is.md#portfolio-constitution): cross-cutting principles are defined only once, in the authoritative source.

### 2.4.3 Other Platform-Agnostic Principles (Quick Reference)

| Principle | One Line | See |
|---|---|---|
| Decouple ingestion from compute | Use Medallion to isolate raw ingestion from business compute logic | [§3 Medallion](03-modeling-governance.md#medallion) |
| Governance-as-Code | Embed governance in CI/CD rather than relying on manual review | [§3 Governance-as-Code](03-modeling-governance.md#governance-as-code) |
| Configuration-driven ingestion | metadata-driven, don't write one-off code for each source | [§4 metadata-driven](04-ingestion-pipeline.md#metadata-driven) |

---

<a id="distribution-mapping"></a>
## 2.5 Distribution Mapping (→ L2)

Once the selection conclusion is fixed, route from here to the corresponding L2 Playbook for the **single-platform architectural detail**. L2 documents obey the [Portfolio Rules](00-what-this-document-is.md#portfolio-constitution): they write only the differences and reference the cross-cutting anchors in this L1.

| Platform | Representative Scenario | L2 Playbook | Status |
|---|---|---|---|
| **Snowflake** | Low-complexity near-real-time analytics, SQL-first, strong governance | Snowflake Lakehouse Playbook (separate repo) | ✅ Exists · link TBD `<L2-SNOWFLAKE-REPO-URL>` |
| **Databricks** | AI + ML centric, needs code flexibility | Databricks AI/ML Playbook (separate repo) | 🚧 To be written · placeholder `<L2-DATABRICKS-REPO-URL>` |
| **BigQuery** | GCP-native serverless analytics | BigQuery Analytical Playbook (separate repo) | ⬜ Future option · placeholder `<L2-BIGQUERY-REPO-URL>` |

> **Reference discipline**: once the L2 links are confirmed, this table is filled with the real repo URLs; when L2 references back to L1, it uses the version-anchored format `L1@<tag>#<slug>` from [`anchors.md`](../../cn/anchors.md). Databricks/BigQuery keep placeholders until their Playbooks land — no dead links left behind.

---

## 2.6 Section Summary

| Deliverable | Destination |
|---|---|
| One-Way Door list | Tiering of architecture review rigor |
| **Platform Decision Record (PDR)** | §6 team capability matrix |
| Platform-agnostic principles (OLAP/OLTP separation) | Must be followed by all L2s |
| Distribution mapping | Route to L2 Playbook |

> **Next** → [Section 3 — Data Modeling & Governance-as-Code](03-modeling-governance.md)
