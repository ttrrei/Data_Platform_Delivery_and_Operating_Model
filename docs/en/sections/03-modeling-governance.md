<!-- slug-anchors: medallion, data-productization, governance-as-code, platform-implementation-notes -->

# Section 3 — Data Modeling & Governance-as-Code

> **Role**: L3 cross-cutting methodology **#1**, referenced by [§2](02-platform-selection.md) / [§4](04-ingestion-pipeline.md) / [§5](05-migration-greenfield.md) / [§7](07-day2-operations.md). This section is the **single source of truth** for Medallion and Governance-as-Code.
> **Boundary**: Principles first. How a specific platform implements them is covered only in an [appendix note](#platform-implementation-notes); the deep detail is left to L2.
> **Dependencies**: None (cross-cutting authoritative source).
>
> ← [Previous Section 2](02-platform-selection.md) · [Back to index](../README.md)

---

## 3.0 The Two Classes of Debt This Section Addresses

> Across the SDLC (software development lifecycle), I focus on guarding against two classes of debt: **technical debt** and **governance debt**. Governance debt is usually **invisible** early on, but the cost of paying it down grows **exponentially** the longer it is deferred.

| Debt | Early symptom | Later cost | Countermeasure in this section |
|---|---|---|---|
| **Technical debt** | Compute logic tangled up with ingestion logic | Change one thing, break everything | [Medallion decoupling](#medallion) |
| **Governance debt (latent)** | "Nobody knows who uses this table", PII scattered everywhere | Compliance incidents, collapse of trust | [Governance-as-Code](#governance-as-code) |

Core idea: **turn governance from an "after-the-fact bureaucratic review" into an "automated gate embedded in the pipeline"**, thereby achieving genuine **Data Productization**.

---

<a id="medallion"></a>
## 3.1 Data Modeling: Paradigm & Medallion Layering ⭐

> Adopt the **Medallion (Bronze/Silver/Gold)** architecture to fully decouple **source-system ingestion logic** from **downstream business compute logic**.

This is the layering definition referenced by all of L2. **The architecture of any platform lands its layer responsibilities according to this scheme.**

> (The Medallion layered architecture was introduced by Databricks; what this section provides is a technology-agnostic definition of layer responsibilities that any platform can implement.)

### 3.1.1 Choosing the Modeling Paradigm

Medallion is a form of **layering** (raw → cleansed → curated), not a **modeling paradigm**. Layering solves "decoupling ingestion from business compute"; the paradigm solves "by what structure the tables in Silver/Gold are organized". The two are orthogonal, and **both must be decided** — building only Medallion without deciding on a paradigm is a common form of latent modeling debt.

L1 defines only the **principles for choosing a paradigm**, without locking down a specific one (DDL-level detail belongs to L2):

| Paradigm | When it fits | Cost / caveats |
|---|---|---|
| **Dimensional modeling (Star Schema / Kimball)** | BI and self-service analytics dominate, definitions need to be intuitive to the business (`workload_type: analytical-bi`) | Requires defining grain and conformed dimensions up front; aggregation-friendly, the default for most analytical scenarios |
| **Data Vault** | Multi-source integration, strong audit traceability, sources change frequently (`governance_maturity: regulated`) | Verbose structure; queries require a downstream mart to be built, engineering cost is high |
| **Wide table / One Big Table** | Single consumption scenario, prioritizing query simplicity and columnar-store performance | High redundancy, definitions drift easily, poor for reuse across multiple consumers |

> **Two decisions that must be locked down at modeling time**:
> - **Grain**: what "one row represents" in each fact/detail table must be unique and explicitly declared — ambiguous grain is the number-one root cause of downstream definition conflicts.
> - **SCD (Slowly Changing Dimension)**: how dimension history is retained (Type 1 overwrite / Type 2 keep historical versions) is dictated by the business's requirement for "traceability", and is usually landed in Silver→Gold.

> **Ownership and irreversibility**: paradigm selection is a matter of L1 principle; the concrete DDL, dbt materialization strategy, and SCD implementation belong to [L2](02-platform-selection.md#distribution-mapping). Once a paradigm is rolled out at scale, the cost of refactoring is extremely high — it is a [§2.1 one-way door](02-platform-selection.md#one-way-door) type of decision and must be settled during the selection phase.

### 3.1.2 The Three-Layer Responsibility Definition

| Layer | Alias | Responsibility | Data shape | Who owns it (see §6) |
|---|---|---|---|---|
| **Bronze** | Raw / raw layer | Faithfully land source data, **no business transformation**; compliance masking is completed here | Close to source structure, append-only, history retained | Data Engineer |
| **Silver** | Cleansed / cleansing layer | Cleansing, deduplication, standardization, conformed dimensions, blending | Normalized, trustworthy, integration-oriented | Analytics Engineer |
| **Gold** | Curated / business layer | Business aggregation, metrics, consumption-oriented wide tables / data marts | Analysis/consumption-oriented, authoritative definitions | Analytics Engineer |

> **Key boundary**: Bronze handles only "land as-is + compliance masking" and must **never** carry business compute; business definitions occur only in Silver→Gold. This boundary is the very substance of "technical-debt decoupling" — changing a business definition never touches ingestion, and changing ingestion never pollutes the business layer.

### 3.1.3 Promotion Criteria ⭐

Data does **not** automatically move up from one layer to the next. Each promotion is an **automated gate** (this is precisely where [Governance-as-Code](#governance-as-code) lands):

| Promotion | Gates that must pass |
|---|---|
| **→ Bronze** | Schema lands successfully; PII already masked per compliance; idempotent/replayable (see [§4 Landing](04-ingestion-pipeline.md#landing-layer)) |
| **Bronze → Silver** | Data quality tests pass (uniqueness / not-null / referential integrity); standardization rules applied; deduplication |
| **Silver → Gold** | Business rule tests pass; metric definitions validated; catalog documentation complete; owner sign-off |

> **Principle**: Only data assets that pass the strict automated governance checks are promoted to Silver/Gold and become trustworthy **Data Products**. Not passing = stuck in the current layer, no pollution downstream.

---

<a id="data-productization"></a>
## 3.2 Data Productization

An asset promoted to Silver/Gold is not "a table" but a **Data Product**. A qualified data product must satisfy three properties simultaneously:

| Property | Meaning | How it is guaranteed (machine-enforced) |
|---|---|---|
| **Reliable** | Quality is guaranteed, refreshed per SLA, trustworthy | dbt/CI data quality tests + [§7 freshness SLO](07-day2-operations.md#sla-slo) |
| **Discoverable** | Documented, has lineage, can be searched | Catalog documentation as part of the promotion gate |
| **Secure** | Access controlled, sensitive data masked | [RBAC](#governance-as-code) + Bronze masking |

> **Test of qualification**: if an asset cannot satisfy all three properties simultaneously, it is **not** a Data Product — merely "a table that happens to exist" — and must not be advertised externally as a consumable asset. All three properties are guaranteed by **machine enforcement**, not by human promises — echoing the [§1.4.2 machine-enforced principle](01-strategic-alignment.md#constraint-classification).

---

<a id="governance-as-code"></a>
## 3.3 Governance-as-Code ⭐

> I do **not** treat data governance as a bureaucratic review process; instead I **embed it in the CI/CD pipeline**, thereby achieving genuine data productization — ensuring data assets are reliable, discoverable, and secure by design.

This is the core principle referenced by [§2](02-platform-selection.md) / [§5](05-migration-greenfield.md) / [§7](07-day2-operations.md). It receives the [§1.4.2 list of machine-enforced constraints](01-strategic-alignment.md#constraint-classification) as its implementation scope.

### 3.3.1 The Four Principles of Governance-as-Code

| # | Principle | How it lands |
|---|---|---|
| 1 | **Write governance into the pipeline, not into meetings** | Governance rule = CI/CD check; violation = build failure, cannot be merged/promoted |
| 2 | **Mask early (Shift-Left Security)** | Mask per compliance right in the **Bronze layer**, not at the consumption layer |
| 3 | **Quality gates are the promotion criteria** | [§3.1.3 promotion criteria](#medallion) enforced by automated tests |
| 4 | **Defensive access control (RBAC)** | Design RBAC on day 1 to prevent role explosion and PII leakage |

### 3.3.2 Masking Early: Injecting Security via Tags During dbt Development (Governance-as-Code)

> Early in the Bronze layer, we mask per regulatory requirements. Security rules are baked directly into the **dbt development phase** via **Tagging (Governance-as-Code)** — on the platform side, a dynamic masking policy (such as a Snowflake Dynamic Masking Policy) lands the enforcement.

The mechanism (technology-agnostic phrasing):

```text
Development time: tag a field with a governance tag (e.g. pii.email, pii.ssn) — written in the dbt/model code, under version control
   │
CI time: check that "every field tagged PII must be bound to a masking policy" — build fails if not bound
   │
Runtime: the platform automatically masks for unauthorized roles by tag → masking policy
```

> **Key point**: masking rules are **code** (tag + policy binding) — reviewed, tested, versioned, and rolled back together with the model — rather than a configuration some DBA clicks through by hand. For platform implementation differences see the [§3.4 appendix note](#platform-implementation-notes).

### 3.3.3 Quality Gates and Documentation as First-Class CI Citizens

Enforce **both** within dbt (or an equivalent tool):

- **Automated data quality tests**: uniqueness, not-null, referential integrity, accepted values, custom business assertions.
- **Data catalog documentation**: model/field descriptions complete, otherwise the promotion gate does not pass.

> Both are hard components of the [promotion criteria](#medallion). **Untested, undocumented assets must not be promoted** — this turns "reliable" and "discoverable" from slogans into mandatory conditions at build time.

### 3.3.4 Defensive RBAC (Defensive Access Control)

> From day 1, design a strict **RBAC (Role-Based Access Control)** framework to prevent "role explosion" and PII/sensitive-data leakage; and use automated **Query History analysis** for continuous behavioral auditing.

| Design principle | Explanation |
|---|---|
| **Least privilege** | Roles are granted the minimum usable permissions per responsibility |
| **Prevent role explosion** | Plan roles along two dimensions — "function + data domain" — to avoid the exponential blow-up of one role per person |
| **Inheritance-based role hierarchy** | Express the permission hierarchy through role inheritance, rather than flat duplication |
| **Continuous behavioral auditing** | Automatically analyze query history to surface anomalous access patterns (echoing [§7 observability](07-day2-operations.md#data-observability)) |

> RBAC's domain partitioning consumes the [§1.3 "domain → Data Owner" table](01-strategic-alignment.md#governance-identification) directly.

---

<a id="platform-implementation-notes"></a>
## 3.4 Appendix Note: Per-Platform Implementation Differences

> The following is an **appendix note**, not the main text. The principles are defined above and are identical across all platforms; the table below lists only "how the same principle lands differently on each platform". The deep detail belongs to L2.

| Principle | Snowflake | Databricks | BigQuery |
|---|---|---|---|
| **Mask early** | Dynamic Data Masking Policy + Object Tagging | Unity Catalog column masks + tags | Column-level security + Policy Tags (Data Catalog) |
| **Quality gates** | dbt tests + Tasks/Streams orchestration | dbt / DLT expectations | dbt tests / Dataform assertions |
| **Lineage / catalog** | Snowflake Horizon + dbt docs | Unity Catalog lineage | Dataplex / Data Catalog |
| **RBAC** | Role hierarchy + inheritance | Unity Catalog (account/metastore level) | IAM + dataset/table ACL |
| **Behavioral auditing** | ACCOUNT_USAGE / QUERY_HISTORY | system tables / audit logs | Cloud Audit Logs / INFORMATION_SCHEMA |

> ⚠️ The table above is signposting only and **does not constitute an implementation guide**. For the concrete DDL/policy syntax, see the corresponding [L2 Playbook](02-platform-selection.md#distribution-mapping).

---

## 3.5 Section Summary

| Deliverable (authoritative definition) | Referenced by |
|---|---|
| [Medallion three-layer responsibilities + promotion criteria](#medallion) | §2 / §4 / §5 / §7 |
| [The three properties of a Data Product](#data-productization) | §7 (SLA target) |
| [The four Governance-as-Code principles](#governance-as-code) | §2 / §5 / §7 |
| [RBAC design principles](#governance-as-code) | §6 / §7 |

> **Next** → [Section 4 — Ingestion & Pipeline Design](04-ingestion-pipeline.md)
