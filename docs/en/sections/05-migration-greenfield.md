<!-- slug-anchors: greenfield-vs-migration, mvp-platform, migration-strategy, legacy-decommissioning -->

# Section 5 — Migration & Greenfield Strategy

> **Role**: L3 cross-cutting methodology **#3**. Covers the two scenarios for standing up a platform: building from scratch (Greenfield) and migrating from a legacy platform (Migration).
> **Boundary**: Strategy and methodology — **not the migration tooling of any specific platform** (that belongs to L2).
> **Dependencies**: References the definitions in [§3 Medallion / Governance](03-modeling-governance.md) and [§4 Landing / Ingestion](04-ingestion-pipeline.md).
>
> ← [Previous Section 4](04-ingestion-pipeline.md) · [Back to index](../README.md)

---

<a id="greenfield-vs-migration"></a>
## 5.1 The Scenario Fork: Greenfield vs. Migration

There are only two fundamental scenarios for standing up a platform, and their strategies differ completely. Before work begins, you must be clear about which one you are in:

| Scenario | Definition | Core risk | Governing strategy |
|---|---|---|---|
| **Greenfield (new build)** | No existing platform; built from scratch | Over-engineering, scope creep, taking too long to deliver value | [MVP Platform](#mvp-platform) to converge scope |
| **Migration** | An existing legacy platform must be replaced | Cutover risk, data inconsistency, double billing | [Domain-Driven + Dual Running](#migration-strategy) |

> **Hybrid scenario**: Most enterprises are "primarily Migration, partly Greenfield" (the old platform is still running, but new domains are built directly on the new platform). Here **both strategies run in parallel**: legacy domains follow migration discipline, new domains follow MVP discipline.

---

<a id="mvp-platform"></a>
## 5.2 Greenfield: The MVP Platform Boundary

The biggest way Greenfield dies is not technical — it is **greed**: trying to build the perfect platform in one shot, only to spend six months with no usable business output while the sponsor loses patience.

### 5.2.1 Defining the MVP Platform

**MVP Platform = the minimal platform that can run one real business domain end to end while meeting the governance baseline.** It is not a "feature-stripped edition"; it is "converged in scope but vertically complete."

| MVP must have (vertically complete) | MVP may defer (horizontal expansion) |
|---|---|
| One real end-to-end pipeline spanning [Landing→Bronze→Silver→Gold](03-modeling-governance.md#medallion) | Coverage of all business domains |
| A consumable Gold product for one real business domain | Backfill of all historical data |
| The minimal gate of [Governance-as-Code](03-modeling-governance.md#governance-as-code) (masking + quality tests + RBAC skeleton) | The full, fine-grained observability/FinOps suite |
| One repeatable [metadata-driven ingestion](04-ingestion-pipeline.md#metadata-driven) pipeline | All source integrations |

> **Domain-selection principle**: Choose the first domain using the [§7 Value Heat Map](07-day2-operations.md#value-heat-map) approach (the framework is defined in §7.1.1; this is a forward reference) — prioritize domains with **high business value × high cross-team usage** to prove value as early as possible. But avoid the "most complex, most compliance-contested" domain as the debut; that one is in the second wave.

> **Key discipline**: The MVP's governance gates **cannot be skipped**. An MVP that skips governance becomes a "ship first, add governance later" promise — and that promise is almost never kept, converting directly into the [governance debt of §3](03-modeling-governance.md#governance-as-code). Scope can converge; the governance baseline cannot be breached.

---

<a id="migration-strategy"></a>
## 5.3 Migration: Migration & Cutover Strategy ⭐

> Once the platform is built, whether the transition can be made **seamless** ultimately decides the project's success or failure.

### 5.3.1 Reject Big Bang

> I **never** advocate a "Big Bang" one-shot cutover, because its operational risk is enormous. Instead, I use a **phased, Domain-Driven** migration strategy.

| Approach | Description | Risk |
|---|---|---|
| **Big Bang (one-shot cutover)** | Switch everything to the new platform on a single day | ❌ Single-point global failure, no rollback, trust bet on one throw |
| **Phased / Domain-Driven** | Migrate incrementally by business domain / lineage dependency | ✅ Small, fast wins; risk can be isolated; rollback is possible |

### 5.3.2 Domain-Driven Rollout

> Migrate by concrete **business domain** (e.g., finance first, then sales) or by **data lineage dependency**. This lets us secure quick wins in small, controllable iterations.

| Ordering basis | Practice |
|---|---|
| **By business domain** | Use the [§1.3 "Domain → Data Owner" table](01-strategic-alignment.md#governance-identification); migrate domains with a clear owner and high value first |
| **By lineage dependency** | Migrate upstream foundational data first and downstream dependents afterward, to avoid cross-platform back-and-forth dependencies |

### 5.3.3 Dual Running + Automated Reconciliation ⭐

> For business-critical or regulatory-reporting workloads, run legacy and the new platform **in parallel (Dual Running)** for a period. During this time, build an **automated data reconciliation engine** that cross-checks the underlying data and the final metrics of both environments. **Only after achieving zero-variance across several consecutive financial cycles do you migrate the trust of stakeholders and auditors.**

```text
       ┌─ Legacy platform ──→ Metric A (old) ─┐
Source ─┤                                     ├─→ Reconciliation engine ─→ Variance report
 data   └─ New platform ─────→ Metric A (new) ─┘                      │
                                                  Zero-variance for N consecutive cycles?
                                                    │Yes          │No
                                                    ▼            ▼
                                       Migrate trust / prepare cutover   Locate difference → fix → re-reconcile
```

| Reconciliation element | Explanation |
|---|---|
| **Reconciliation level** | Compare both the **underlying data** (row-level / aggregate) and the **final metrics** (business definition) |
| **Comparison semantics first** | Fix the comparison definitions before reconciliation begins: rounding rules, time zones, late-data cutoffs, NULL / dedup semantics. Otherwise what you chase is usually **spurious variance** produced by definitional mismatch, and zero-variance becomes forever unreachable |
| **Zero-variance threshold** | Not "close," but **strict zero-variance across several complete business cycles** |
| **Trust migration** | Only after passing zero-variance verification do you migrate stakeholder/auditor trust from the old platform to the new one |
| **Automation** | Reconciliation is an **engine**, not manual Excel comparison — repeatable and auditable |

> Reconciliation depends on the [§1.2 current-state baseline](01-strategic-alignment.md#current-state-audit) as the frame of reference for the "correct answer," and on the [§3 Gold-layer definitions](03-modeling-governance.md#medallion) as the authority for metric definitions.

### 5.3.4 Cutover

Once zero-variance verification passes, execute the cutover by domain. Before cutting over each domain, confirm: the rollback plan is ready, downstream consumers have been notified, and the new platform's [SLO](07-day2-operations.md#sla-slo) is in place. Cutover happens **in batches by domain**, not globally in one shot.

---

<a id="legacy-decommissioning"></a>
## 5.4 Legacy Decommissioning as a Hard KPI ⭐

> After a successful cutover, you must execute a **hard schedule** to shut down the legacy system. Many enterprise migrations fail financially precisely because they keep the old system alive **indefinitely**, incurring **double cloud bills**. I treat "Legacy System Decommissioning" as a **non-negotiable KPI** for project completion.

| Anti-pattern | Correct approach |
|---|---|
| Keep the old system "just in case," alive indefinitely | Set a **hard decommissioning schedule** at cutover; force shutdown at the deadline |
| Decommissioning has no owner and no deadline | Decommissioning is a **KPI for project completion**; not decommissioned = project not complete |
| Parallel dual platforms become the norm | Dual Running is a **time-bounded** measure, not an end state |

> **Core claim**: **A migration project is "done" not when the new platform goes live, but when the old platform is shut down.** As long as the old system keeps running, it keeps burning a second cloud bill, keeps splitting data trust, and keeps blocking the team from fully turning to the new platform. The decommissioning KPI must be written into the project charter and endorsed by the [sponsor](01-strategic-alignment.md#governance-identification).

---

## 5.5 Section Summary

| Deliverable | Linkage |
|---|---|
| [Greenfield/Migration fork](#greenfield-vs-migration) | Determines the subsequent strategy |
| [MVP Platform boundary](#mvp-platform) | §7 Value Heat Map domain selection |
| [Anti-Big-Bang + Domain-Driven + zero-variance reconciliation](#migration-strategy) | §1 baseline / §3 Gold definitions |
| [Legacy decommissioning KPI](#legacy-decommissioning) | §7 FinOps (eliminate double billing) |

> **Next** → [Section 6 — Team Topology & Operating Structure](06-team-topology.md)
