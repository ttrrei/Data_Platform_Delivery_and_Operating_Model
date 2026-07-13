<!-- slug-anchors: okr-alignment, current-state-audit, governance-identification, constraint-classification, requirements-profile -->

# Section 1 — Strategic Alignment & Discovery

> **Role**: The starting point of the L1 narrative. Turn fuzzy business needs into a structured input that can be fed directly into platform selection.
> **Output contract**: [Requirements Profile](#requirements-profile) — the only output of this section that is binding on downstream work, referenced field by field in [Section 2](02-platform-selection.md).
> **Boundary**: This section makes **no platform-selection judgement whatsoever**. The moment the thought "should we pick Snowflake or Databricks" arises, stop — that belongs to Section 2.
>
> ← [Previous — Section 0](00-what-this-document-is.md) · [Back to index](../README.md)

---

## 1.0 Why Start with Strategy Rather Than Technology

> If I were to build and run an enterprise-grade data platform from scratch, I would **never** start with technology selection. I would start with **business strategy** and **existing pain points**.

Technology selection is an output of Section 2, not a starting point. Projects that start from technology have a classic way of dying: they buy a powerful platform, only to find it doesn't solve the problem the company actually hurts from — either over-engineering (buying stream processing for a real-time need that doesn't exist), or a governance gap (compliance requirements were never translated into architectural constraints).

The work of this section is, before touching any technology, to make four things crystal clear and lock them into a structured profile:

```text
OKR alignment ──→ current-state audit ──→ governance identification ──→ constraint classification
   (why build it)   (where it hurts now)   (who decides / who is accountable)   (FR/NFR)
                                                    │
                                                    ↓
                                        Requirements Profile (output contract)
                                                    │
                                                    ↓
                                            Section 2 selection
```

---

<a id="okr-alignment"></a>
## 1.1 OKR Alignment (Strategic / OKR Alignment)

The first step is to clarify the company's **OKR**: which business objective is this platform actually serving?

The two most common drivers lead to **completely different** non-functional requirements:

| Driver | Typical OKR phrasing | Implied requirement on the platform |
|---|---|---|
| **Accelerate business decisions** | "Cut decision latency on core metrics from T+1 to hourly" | Low latency, self-service analytics, metric consistency |
| **Meet strict regulatory compliance** | "Satisfy APRA / banking & insurance regulatory reporting requirements" | Audit traceability, access control, data lineage, masking |

> **Key action**: Translate each OKR into a single "the platform must be able to…" capability statement. That statement is the source of the FR/NFR and the Requirements Profile that follow. An OKR that cannot be translated into a platform capability statement is irrelevant to this platform and should be excluded, to avoid scope creep.

**Anti-pattern**: Skipping the OKR and going straight to collecting "what features each department wants." A feature list has no priorities, is internally contradictory, and cannot answer "what happens if we don't do it." What the OKR provides is a **basis for trade-offs**.

---

<a id="current-state-audit"></a>
## 1.2 Current-State Bottleneck Audit (Current-State Audit)

Diagnose the current bottlenecks, turning "everyone feels things are terrible right now" into a quantifiable list. The audit runs along four dimensions:

| Dimension | Audit question | Example quantitative metric |
|---|---|---|
| **Latency / timeliness (Latency)** | How long from data creation to availability? | End-to-end freshness, report T+N |
| **Consistency (Consistency)** | Is the same metric defined consistently across departments? | Number of versions of an identically named metric, count of definition-conflict tickets |
| **Cost (Cost)** | Trend of compute/storage cost? Is it out of control? | Monthly compute-bill growth rate, cost per query |
| **Trust / quality (Trust)** | Does the business trust the data? Frequency of broken dashboards? | Data incidents per month, number of dashboard complaints |

> **Key action**: Every bottleneck must land on a **current baseline value**. Without a baseline, once migration is complete you cannot prove value (Section 5's zero-variance validation and Section 7's SLOs both depend on the baselines set here).

**Two by-products of the audit** (used in later sections):

- **Pain-point → OKR mapping**: Confirm that each bottleneck genuinely blocks some OKR; a "pain point" that blocks no OKR is deprioritized.
- **Hidden Governance Debt leads**: If, during the audit, you find "nobody knows who uses this table" or "PII is scattered across many places," write it down — this is the debt that [Section 3 Governance-as-Code](03-modeling-governance.md#governance-as-code) has to repay.

---

<a id="governance-identification"></a>
## 1.3 Governance & Ownership Identification (Governance & Ownership)

A platform is not a technology project, it is an **organizational project**. Before kickoff you must clearly identify "who decides, who is responsible, who is accountable":

| Role | Definition | Consequence if unclear |
|---|---|---|
| **Executive Sponsor** | The executive who pays for the platform, can coordinate resources across departments, and can own the OKR | A platform without a sponsor dies at the first budget review |
| **Data Owner (by domain)** | The business owner of the data for each business domain (finance / sales / …) | Without an owner, no one is accountable for data quality and governance cannot land |
| **Data Steward** | The day-to-day data-management executor authorized by the owner | Absent, governance rules are set by someone but guarded by no one |
| **Platform Team** | The engineering team that builds and operates the platform itself (see [Section 6](06-team-topology.md)) | If the boundary with owners is unclear, it sinks into a swamp of ad-hoc requests |

> **Key action**: Produce a **RACI**, or at minimum a "domain → Data Owner" mapping table. This table directly determines [Section 5's Domain-Driven migration order](05-migration-greenfield.md#migration-strategy) (migrate by domain, starting with domains that have a clear owner) and [Section 3's RBAC design](03-modeling-governance.md#governance-as-code).

---

<a id="constraint-classification"></a>
## 1.4 Constraint Classification Framework (Constraint Classification)

Translate the insights from the first three steps into **Functional Requirements (FR)** and **Non-Functional Requirements (NFR)**. This is the key conversion from "business language" to "architecture language."

### 1.4.1 FR / NFR — the First Axis

| Type | Definition | Data-platform example |
|---|---|---|
| **FR (functional)** | What the platform must **do** | Support self-service BI, support the definition-based calculation of metric X, expose an external API |
| **NFR (non-functional)** | **How well** the platform must do it | Data security, high concurrency, latency upper bound, availability SLA, auditability |

### 1.4.2 The Second Axis: Machine-Enforced vs. Human-Enforced (the Critical Distinguishing Axis)

Distinguishing FR/NFR alone is not enough. Each constraint must also be tagged with **what guarantees it** — this axis directly determines the form it takes in Sections 3/7:

| Enforcement | Definition | Realization form | Example |
|---|---|---|---|
| **Machine-Enforced** | Automatically guaranteed by code/CI/platform policy; violations are blocked | [Governance-as-Code](03-modeling-governance.md#governance-as-code), CI gating, Masking Policy | "PII fields must be masked in Bronze" → CI tag check |
| **Human-Enforced** | Guaranteed by process, review, and training; violations are caught by people | SOP, review meetings, training | "Major model changes require architecture review" |

> **Core assertion**: **Whatever can be machine-enforced must never be left to human-enforcement.** Human-enforced constraints tend to be violated over time — review meetings miss things, processes get bypassed, and people turn over. The output of this axis is a "which constraints must be automated" list handed to [Section 3 Governance-as-Code](03-modeling-governance.md#governance-as-code).

> **Key action**: Tag each NFR with `[machine|human]`. Everything tagged `machine` enters the scope of Section 3's CI/CD governance implementation.

---

<a id="requirements-profile"></a>
## 1.5 Requirements Profile — the Output Contract of This Section ⭐

> This is the **only** output of Section 1 that is binding on downstream work. Section 2's [six-dimension evaluation](02-platform-selection.md#six-dimension-evaluation) consumes it field by field. The field names are the contract; downstream must reference them by the same name and must not rename them.

### 1.5.1 Field Definitions

| Field | Value (enum) | Source | Use in Section 2 |
|---|---|---|---|
| `workload_type` | `analytical-bi` / `ai-ml-centric` / `mixed` / `serving-api` | OKR + current-state audit | Determines the OLAP engine type and whether a separate serving layer is needed |
| `team_capability_ceiling` | `low-sql-only` / `mid-sql-plus-python` / `high-software-engineering` | Team's current state (detailed assessment in Section 6) | Determines the upper bound of operational/coding complexity the platform can tolerate |
| `governance_maturity` | `ad-hoc` / `defined` / `regulated` | Governance identification + compliance driver | Determines the strength of governance features (audit / masking / lineage) |
| `streaming_need` | `none` / `near-real-time` / `true-streaming` | Latency requirements from the OKR | Determines whether a streaming architecture is needed (see §4) |
| `cloud_lock_in_tolerance` | `single-cloud-ok` / `prefer-portable` / `multi-cloud-required` | Enterprise cloud strategy + regulation | Determines the lock-in dimension score |
| `compliance_regime` | `none` / `pii-only` (general privacy laws such as GDPR) / `sector-regulated` (e.g. APRA/HIPAA/PCI DSS) | Compliance driver | A hard gate on selection (a veto item) |
| `cost_sensitivity` | `cost-leading` / `balanced` / `capability-leading` | Current-state cost audit + sponsor orientation | Determines the weight of FinOps/TCO in the evaluation |

> The first 5 fields are the core fields explicitly required by the TASK_BRIEF; `compliance_regime` and `cost_sensitivity` are added to the contract as high-frequency, decisive fields.

### 1.5.2 Output Template (copy and fill in directly)

```yaml
# Requirements Profile — Section 1 output, Section 2 input
requirements_profile:
  workload_type:            analytical-bi        # analytical-bi | ai-ml-centric | mixed | serving-api
  team_capability_ceiling:  mid-sql-plus-python  # low-sql-only | mid-sql-plus-python | high-software-engineering
  governance_maturity:      regulated            # ad-hoc | defined | regulated
  streaming_need:           near-real-time       # none | near-real-time | true-streaming
  cloud_lock_in_tolerance:  single-cloud-ok      # single-cloud-ok | prefer-portable | multi-cloud-required
  compliance_regime:        sector-regulated     # none | pii-only | sector-regulated
  cost_sensitivity:         balanced             # cost-leading | balanced | capability-leading

  # Appendix: traceability (not a selection input, but referenced by later sections)
  drivers:
    - okr: "Cut decision latency on core financial metrics from T+1 to hourly"
      maps_to: [workload_type, streaming_need]
  baselines:        # From the §1.2 audit; referenced by §5 zero-variance / §7 SLO
    report_freshness: "T+1"
    monthly_compute_growth: "18% MoM"
  machine_enforced_constraints:   # From §1.4.2; for §3 governance implementation
    - "PII fields must be masked in Bronze"
    - "Gold-layer metric changes must pass dbt tests"
```

> **Filling discipline**: Every enum value must be traceable to a specific finding in §1.1–1.4. A field whose source you cannot state means discovery was not thorough enough — do not fill it in by gut feel.

---

## 1.6 Section Summary

| Deliverable | Destination |
|---|---|
| OKR → platform capability statement | The "why" that runs through the whole document |
| Quantified current-state baselines | §5 zero-variance validation, §7 SLO |
| Domain → Data Owner table | §5 migration order, §3 RBAC, §6 team |
| Machine-enforced constraint list | §3 Governance-as-Code |
| **Requirements Profile** | **§2 six-dimension evaluation (core contract)** |

> **Next** → [Section 2 — Platform Selection & Architecture Decision Framework](02-platform-selection.md)
