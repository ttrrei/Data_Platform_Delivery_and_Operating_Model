# Data Platform Delivery & Operating Model — English

> **L1 — Technology-agnostic top-level framework**
> A complete lifecycle framework for how an enterprise data platform is **built, delivered, migrated, operated, and continuously governed.**
>
> Status: ✅ **Draft** (translated from CN). The authoritative source remains the [Chinese version](../cn/README.md); on any wording conflict, CN wins. This English edition mirrors the CN structure and stable slug anchors one-to-one.

← Back to overview: [`/README.md`](../../README.md) · 中文版（权威源）: [`docs/cn/README.md`](../cn/README.md)

---

## Status

The structure below mirrors the Chinese version one-to-one (same files, same stable slug anchors). Each section has been translated from the authoritative CN source.

| # | Section | Role | EN Status |
|---|---|---|---|
| 0 | [What This Document Is](sections/00-what-this-document-is.md) | Portfolio constitution | ✅ Draft |
| 1 | [Strategic Alignment & Discovery](sections/01-strategic-alignment.md) | Lifecycle entry | ✅ Draft |
| 2 | [Platform Selection & Architecture Decision Framework](sections/02-platform-selection.md) | **Hub / router** | ✅ Draft |
| 3 | [Data Modeling & Governance-as-Code](sections/03-modeling-governance.md) | Cross-cutting #1 | ✅ Draft |
| 4 | [Ingestion & Pipeline Design](sections/04-ingestion-pipeline.md) | Cross-cutting #2 | ✅ Draft |
| 5 | [Migration & Greenfield Strategy](sections/05-migration-greenfield.md) | Cross-cutting #3 | ✅ Draft |
| 6 | [Team Topology & Operating Structure](sections/06-team-topology.md) | Cross-cutting #4 | ✅ Draft |
| 7 | [Day-2 Operations & Platform Governance](sections/07-day2-operations.md) | Cross-cutting #5 | ✅ Draft |

---

## Translation Notes

When translating from CN → EN:

1. **Keep stable slug anchors identical** to the CN version so L2 cross-repo references (`L1@<tag>#<slug>`) resolve in both languages. See [`docs/cn/anchors.md`](../cn/anchors.md).
2. **Preserve the contracts verbatim** — field names of the `Requirements Profile`, the `Platform Decision Record`, and Medallion layer names are part of the cross-repo contract and must not be renamed in translation.
3. **Tables stay tables.** Do not flatten structured tables into prose.
4. **Technology-agnostic body, platform differences in appendix notes** — same discipline as CN.
