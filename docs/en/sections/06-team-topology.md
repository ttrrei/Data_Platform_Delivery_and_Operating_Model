<!-- slug-anchors: dataops-mindset, role-topology, platform-team-capability-matrix, engagement-model, self-service-enablement -->

# Section 6 — Team Topology & Operating Structure

> **Role**: L3 cross-cutting methodology **#4**. Co-design of platform and team capability — a technology upgrade must be matched by a team-capability upgrade.
> **Boundary**: Organizational design **principles**, not concrete hiring JDs.
> **Dependency**: References [§2's selection conclusion (PDR)](02-platform-selection.md#platform-decision-record).
>
> ← [Previous Section 5](05-migration-greenfield.md) · [Back to index](../README.md)

---

## 6.0 Without a Team Upgrade, Even the Best Stack Is Just Decoration

> A technology upgrade must be matched by a team-capability upgrade. Without a modernized team, even the best Modern Data Stack (MDS) turns into **shelfware**.

This section covers four things: shifting the **mindset** (DataOps), defining the **division of labor** (role topology), provisioning **capability** (per platform selection), designing **collaboration and exit** (engagement model), and ultimately **handing power back to the business** (self-service).

---

<a id="dataops-mindset"></a>
## 6.1 DataOps Mindset Transformation

> Traditional data teams often rely on drag-and-drop ETL tools or hand-written stored procedures, lacking core **software-engineering discipline**. I drive the team toward a **DataOps mindset**, making version control (Git Flow), unit testing (TDD), and continuous integration (CI/CD) **foundational skills** for every data engineer.
>
> (DataOps is an established methodology movement in the industry that ports DevOps engineering discipline into data workflows; this section adopts its core practices.)

| Dimension | Traditional data team | DataOps team |
|---|---|---|
| **Change management** | Manual edits in a GUI, no versioning | Git Flow, everything under version control |
| **Quality assurance** | Discovered by people after go-live | TDD / automated tests (echoing [§3 quality gates](03-modeling-governance.md#governance-as-code)) |
| **Delivery** | Manual deployment, not repeatable | CI/CD automation, repeatable, rollback-capable |
| **Collaboration** | Lone heroes, knowledge in people's heads | Code review, knowledge in the repo |

> **This is the precondition for [Governance-as-Code](03-modeling-governance.md#governance-as-code) to land**: governance is written into the pipeline, which requires the team to first possess the engineering discipline of "treating everything as code." Without a DataOps mindset, Governance-as-Code is a non-starter.

---

<a id="role-topology"></a>
## 6.2 Role Topology: The DE / Analytics Engineer / BI Three-Tier Division of Labor ⭐

> I introduce the **Analytics Engineer** role as a bridge between the Data Engineer (DE) and the Business Analyst (BI).
>
> (The Analytics Engineer role, and the "AE sits between DE and BI" division of labor, was proposed and popularized by dbt Labs in the Modern Data Stack context; this section adopts that division and maps it onto the Medallion layers.)

| Role | Core responsibilities | Corresponding Medallion layer | Key skills |
|---|---|---|---|
| **Data Engineer (DE)** | Core ingestion, performance tuning, infrastructure stability | [Landing / Bronze](04-ingestion-pipeline.md#landing-layer) | Software engineering, pipelines, platform operations |
| **Analytics Engineer (AE)** | Business modeling, [Governance-as-Code](03-modeling-governance.md#governance-as-code) | [Silver / Gold](03-modeling-governance.md#medallion) | SQL/dbt, modeling, domain knowledge |
| **BI / Business Analyst** | Consuming Gold, producing insights, interfacing with the business | Consumes [Gold](03-modeling-governance.md#medallion) | Visualization, business analysis |

> **Why the AE layer is needed**: it lets the **DE focus on core ingestion, performance tuning, and infrastructure stability**, while the **AE owns business modeling and Governance-as-Code in dbt**. This structure **prevents the DE from being dragged down by ad-hoc business requests** — otherwise the DE is fixing pipelines and fielding business-definition requirements at the same time, doing neither well. The AE is the meeting point of "business semantics" and "engineering discipline," directly carrying [§3's Silver→Gold promotion and documentation](03-modeling-governance.md#medallion).

---

<a id="platform-team-capability-matrix"></a>
## 6.3 Platform Selection → Team Capability Matrix Impact Table ⭐

Platform selection ([§2 PDR](02-platform-selection.md#platform-decision-record), field `team_capability_ceiling`) directly determines what capability configuration the team needs. This is the **organizational consequence** of selection, and it is often overlooked:

| Selection profile | Requirements on the DE | Requirements on the AE | Team risk |
|---|---|---|---|
| **SQL-first warehouse** (e.g., Snowflake profile) | Medium: SQL + orchestration suffices | High: dbt modeling is the main battleground | Low barrier; AE is the bottleneck role |
| **Lakehouse / code elasticity** (e.g., Databricks profile) | High: Spark/Python/cluster tuning | Medium-high: needs both notebooks + dbt | High DE skill bar, hard to hire |
| **Serverless** (e.g., BigQuery profile) | Medium: low ops, heavy SQL + IaC | High: modeling + cost awareness | Cost governance relies on AE self-discipline |

> **Core claim**: **Selection is not just choosing technology — it is choosing "what kind of team you have to grow."** If [§1's Profile](01-strategic-alignment.md#requirements-profile) has `team_capability_ceiling = low-sql-only`, yet §2 selected a platform requiring high software-engineering capability, the gap must be filled by **hiring or training** — and that gap must be counted into [TCO](02-platform-selection.md#one-way-door) at selection time, not discovered after go-live when the team can't drive the platform.

---

<a id="engagement-model"></a>
## 6.4 Service-Provider Embedding Model + Knowledge Transfer + Exit Strategy

When a platform is delivered by an external service provider / consulting team, the collaboration model determines whether "the team can operate independently after delivery."

### 6.4.1 Embedded vs. Advisory

| Model | Description | Fit | Risk |
|---|---|---|---|
| **Embedded** | Provider engineers join the client team and deliver jointly | Client team starts from a low capability baseline, needs to learn by doing | Dependency deepens, hard to exit |
| **Advisory** | Provider sets direction / reviews, the client team does the work | Client already has some capability, wants methodology | Slower to land, depends on the client's execution capacity |

> Most often it is **Embedded first, then Advisory**: embed and carry the work early, then progressively step back into an advisory role as knowledge transfer advances.

### 6.4.2 Knowledge Transfer and Exit Strategy (Critical)

> **The success of an embedded engagement is measured not by what was delivered, but by whether the client can operate independently after departure.**

| Element | Practice |
|---|---|
| **Knowledge transfer** | Pair programming, documentation (echoing [§3 catalog documentation](03-modeling-governance.md#governance-as-code)), internal training — knowledge goes into the repo, not into individual heads |
| **Capability handover milestones** | Set verifiable milestones of "the client independently completes X," rather than billing by hours |
| **Exit Strategy** | Define exit criteria and a timeline **at** project kickoff — the provider's goal is "to make itself no longer needed" |

> **Symmetry with [§5 Legacy decommissioning](05-migration-greenfield.md#legacy-decommissioning)**: migration must hard-retire the old system; provider collaboration must hard-exit the dependency. Both reject "indefinite life support." A consulting relationship with an unclear exit strategy will burn money continuously, just like a legacy system that never gets decommissioned.

---

<a id="self-service-enablement"></a>
## 6.5 Self-Service Enablement

> The **ultimate goal of platform management is data democratization**. While the internal team is being upgraded, we cultivate **'Data Champions'** within the business units. By opening up strictly governed Silver/Gold layers, we achieve true **Self-Service Analytics**, transforming the data team from a passive "ticket-taking bottleneck" into a strategic "platform enabler."

| Element | Description |
|---|---|
| **Data Champions** | Data leads cultivated within each business unit, serving as the business-side self-service-analytics champions and platform liaisons |
| **Governed Access** | Open up only the [Silver/Gold data products](03-modeling-governance.md#data-productization) that **have passed governance gates**, constrained by [RBAC](03-modeling-governance.md#governance-as-code) — openness ≠ loss of control |
| **Role shift** | The data team moves from "ticket-taking bottleneck" → "platform enabler" |

```text
Traditional: business ──ticket──→ data team (bottleneck) ──→ data
Self-service: business (Data Champions) ──consume directly──→ governed Gold layer
                              data team = maintains the platform and governance guardrails (enabler)
```

> **Precondition**: self-service presupposes that [§3's Governance-as-Code](03-modeling-governance.md#governance-as-code) is already in place. **"Openness" without governance guardrails is a disaster** — it creates definition chaos and data leakage. Governed first, then self-service.

---

## 6.6 Section Summary

| Deliverable | Linkage |
|---|---|
| [DataOps mindset](#dataops-mindset) | Precondition for §3's Governance-as-Code |
| [DE/AE/BI three-tier division of labor](#role-topology) | Owners of each §3 Medallion layer |
| [Selection → capability matrix](#platform-team-capability-matrix) | §2 PDR / §1 Profile |
| [Embedded/Advisory + Exit](#engagement-model) | §5's symmetric discipline of decommissioning |
| [Self-Service + Data Champions](#self-service-enablement) | §3 governed access |

> **Next** → [Section 7 — Day-2 Operations & Platform Governance](07-day2-operations.md)
