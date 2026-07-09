# Data Platform Delivery & Operating Model — English

> **L1 — Technology-agnostic top-level framework**
> A complete lifecycle framework for how an enterprise data platform is **built, delivered, migrated, operated, and continuously governed.**
>
> Status: ⬜ **Pending translation.** The authoritative source is the [Chinese version](../cn/README.md); this English edition will be translated once the CN draft is finalized (per `TASK_BRIEF.md` Batch 4).

← Back to overview: [`/README.md`](../../README.md) · 中文版（权威源）: [`docs/cn/README.md`](../cn/README.md)

---

## Status

The structure below mirrors the Chinese version one-to-one (same files, same stable slug anchors). Each link points to the placeholder stub that will hold the translated body; content is filled in during the final translation pass.

| # | Section | Role | EN Status |
|---|---|---|---|
| 0 | [What This Document Is](sections/00-what-this-document-is.md) | Portfolio constitution | ⬜ Pending |
| 1 | [Strategic Alignment & Discovery](sections/01-strategic-alignment.md) | Lifecycle entry | ⬜ Pending |
| 2 | [Platform Selection & Architecture Decision Framework](sections/02-platform-selection.md) | **Hub / router** | ⬜ Pending |
| 3 | [Data Modeling & Governance-as-Code](sections/03-modeling-governance.md) | Cross-cutting #1 | ⬜ Pending |
| 4 | [Ingestion & Pipeline Design](sections/04-ingestion-pipeline.md) | Cross-cutting #2 | ⬜ Pending |
| 5 | [Migration & Greenfield Strategy](sections/05-migration-greenfield.md) | Cross-cutting #3 | ⬜ Pending |
| 6 | [Team Topology & Operating Structure](sections/06-team-topology.md) | Cross-cutting #4 | ⬜ Pending |
| 7 | [Day-2 Operations & Platform Governance](sections/07-day2-operations.md) | Cross-cutting #5 | ⬜ Pending |

---

## Translation Notes

When translating from CN → EN:

1. **Keep stable slug anchors identical** to the CN version so L2 cross-repo references (`L1@<tag>#<slug>`) resolve in both languages. See [`docs/cn/anchors.md`](../cn/anchors.md).
2. **Preserve the contracts verbatim** — field names of the `Requirements Profile`, the `Platform Decision Record`, and Medallion layer names are part of the cross-repo contract and must not be renamed in translation.
3. **Tables stay tables.** Do not flatten structured tables into prose.
4. **Technology-agnostic body, platform differences in appendix notes** — same discipline as CN.
