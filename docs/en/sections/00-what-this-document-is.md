<!-- slug-anchors: portfolio-constitution, three-layer-structure -->

# Section 0 — What This Document Is

> **Role**: The Portfolio Constitution. This section defines the boundaries, layering, and inviolable collaboration rules for the entire documentation system.
> It is not about the data platform itself; it is about how "this body of documentation on data platforms" is organized.
>
> ← [Back to index](../README.md) · Anchor registry: [`anchors.md`](../../cn/anchors.md)

---

## 0.1 The Document's Sole Purpose

This documentation answers **one** question:

> **Regardless of the underlying technology, how does an enterprise data platform go from "why build it" to "how to keep it healthy for the long haul."**

It is the **L1 — technology-agnostic top-level framework**: covering the complete **lifecycle** of a data platform, from strategic alignment, selection, modeling and governance, ingestion, migration, and team, through to Day-2 operations.

Questions it deliberately does **not** answer (these belong to L2 / L3):

| Not in this document | Belongs to |
|---|---|
| How to draw the concrete architecture of a specific platform | L2 Playbook |
| How to write the SQL / Spark / DDL for a specific platform | L2 Playbook |
| How to configure a specific monitoring/orchestration tool | L2 Playbook |

> The boundary in one line: **platform selection is merely one input variable to [Section 2](02-platform-selection.md); it is not the subject of this document.**

---

<a id="three-layer-structure"></a>
## 0.2 Three-Layer Structure

The entire knowledge system is split into three layers with strictly separated responsibilities:

| Layer | Name | Content | Form |
|---|---|---|---|
| **L1** | Data Platform Delivery & Operating Model | technology-agnostic lifecycle and methodology | This repo |
| **L2** | Platform Playbooks | Single-platform architecture blueprints and implementation detail (Snowflake / Databricks / BigQuery …) | Separate repos, one each |
| **L3** | Cross-cutting Methodology | Medallion, Governance-as-Code, Ingestion, Migration, Team, Day-2, and other principles shared by all platforms | **Embedded within L1's Section 3–7** (not a standalone repo) |

```text
L1  Data Platform Delivery & Operating Model   ← this repo (technology-agnostic)
      Section 2 = selection distribution router
         │  cross-repo external-link distribution
         ├──────────────────┬──────────────────┐
         ↓                  ↓                  ↓
L2  Snowflake          Databricks         BigQuery
    Playbook           Playbook           Playbook
         └──────────────────┴──────────────────┘
                          ↓ all reference
L3  cross-cutting methodology (embedded in L1 Section 3/4/5/6/7)
```

**Why L3 is embedded rather than standalone**: cross-cutting methodology is deeply interwoven with the lifecycle narrative (for example, "migration" inevitably references "Medallion layering"), and forcibly splitting it into a third repo would create bidirectional cross-repo dependencies and version hell. Embedding makes L1 the **single authoritative source** for cross-cutting methodology, which L2 can then reference one-way.

---

<a id="portfolio-constitution"></a>
## 0.3 Portfolio Constitution — Three Mandatory Rules

The long-term maintainability and non-decay of the entire system rests on these three rules, and these alone. They are the "constitution"; no section and no L2 may violate them.

### Rule 1 — L1 Defines the Principles, L2 Writes Only the Differences

Any **technology-agnostic** methodology is defined in L1 exactly **once**. L2 references L1 and only fills in "how that platform's implementation differs from the general principle"; it does **not** re-explain the theory.

> Example: "The Bronze layer must be masked" is a principle, defined in [Section 3](03-modeling-governance.md#governance-as-code). The Snowflake Playbook does not repeat this statement; it only writes the **difference** — "in Snowflake, implement Bronze masking with Dynamic Masking Policy + Tag."

### Rule 2 — Cross-cutting Sections Are the Single Source of Truth

When an L1 cross-cutting section **conflicts** with the wording of some L2, **L1 prevails**. If an L2 finds that an L1 principle does not apply, the correct action is to raise an issue to revise L1 — not to privately rewrite the principle inside the L2.

### Rule 3 — Cross-repo References Must Be Version-Anchored

When L2 externally links to an L1 cross-cutting section, it **must** reference a stable anchor carrying a version tag:

```text
✅  L1@v1.2#governance-as-code      ← version-anchored, stable
❌  .../main/03-modeling.md          ← links floating content on main; breaks anytime
```

All referenceable anchors are registered in [`anchors.md`](../../cn/anchors.md). **Changing a registered slug = a breaking change**; it requires bumping L1's version tag and leaving a record in the Deprecated area of anchors.

> **Current status (maturity)**: This document is `v0.1-draft`, and its git tag is yet to be created after the CN version is finalized and merged into `main`. Until the tag exists, the version-anchoring format above is not yet resolvable, and L2 should **hold off** on referencing via `L1@<tag>#<slug>` (see the release notes in [`anchors.md`](../../cn/anchors.md) and the [`CHANGELOG`](../../../CHANGELOG.md)). This cross-repo contract mechanism is currently **designed and awaiting gradual rollout as L2 lands** — within a single repository, this document is already complete and usable.

---

## 0.4 Reading Paths

| Your goal | Path |
|---|---|
| Understand the overall methodology / drive a new platform 0→1 | Read Section 1 → 7 in order |
| Platform already chosen, just want the architecture | Read [Section 2 distribution mapping](02-platform-selection.md#distribution-mapping) → jump to the corresponding L2 |
| Write / maintain a specific L2 | Read Section 3 / 4 first (cross-cutting core), reference per `anchors.md` |

---

## 0.5 Core Contracts Running Throughout

The structured objects that downstream sections depend on each other for are registered centrally here, to avoid each section redefining them:

| Contract object | Defined in | Referenced in |
|---|---|---|
| **Requirements Profile** | [§1](01-strategic-alignment.md#requirements-profile) | §2 |
| **Medallion three-layer responsibilities** | [§3](03-modeling-governance.md#medallion) | §2 / §4 / §5 / §7 |
| **Governance-as-Code** | [§3](03-modeling-governance.md#governance-as-code) | §2 / §5 / §7 |
| **Landing Layer** | [§4](04-ingestion-pipeline.md#landing-layer) | §2 / §5 |
| **Platform Decision Record** | [§2](02-platform-selection.md#platform-decision-record) | §6 |
| **Value Heat Map** | [§7](07-day2-operations.md#value-heat-map) | §5 |

---

## 0.6 Scope Boundaries (Intentionally Not Covered by This Document)

L1 is an **operating model and lifecycle methodology**, not an engineering implementation manual. The following topics are **intentionally delegated** to L2 or later versions and are not elaborated here — declared explicitly so they are not misread as omissions:

| Topic | Belongs to | Reason |
|---|---|---|
| Full TCO calculation model (quantitative formulas) | L2 / delivery-phase financial modeling | Depends on specific platform pricing and usage; L1 only provides the [factor checklist](02-platform-selection.md#one-way-door) and principles |
| Security beyond RBAC / masking (network isolation, keys and secrets, encryption systems) | L2 (platform-specific) | Strongly platform-dependent; L1 only sets [Governance-as-Code](03-modeling-governance.md#governance-as-code) and least-privilege-access principles |
| DR / BCP (disaster recovery and business continuity) | L2 / platform operations | Tightly coupled to platform high-availability capabilities |
| Source-system Data Contract specifics | L2 / upstream governance | L1 only requires explicit schema declaration and fail-fast on the [ingestion](04-ingestion-pipeline.md#metadata-driven) side |
| Multi-region / data-residency architecture | L2 (platform-specific) | Determined jointly by compliance regions and platform capabilities |

> In other words, when this document says "complete," it means **a complete closed loop of the operating-model narrative** (see [§7.7](07-day2-operations.md#platform-evolution)), not an exhaustive enumeration of every engineering implementation detail.

---

> **Next** → [Section 1 — Strategic Alignment & Discovery](01-strategic-alignment.md)
