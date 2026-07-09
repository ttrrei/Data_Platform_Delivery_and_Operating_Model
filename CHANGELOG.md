# Changelog

本文件记录 L1 文档的显著变更。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循 [语义化版本 SemVer](https://semver.org/lang/zh-CN/)。

All notable changes to this L1 document are recorded here. Format follows Keep a Changelog; versions follow SemVer.

> 版本口径：当前处于 `v0.1-draft`（CN 初稿）。git tag 一律在 `main` 分支创建——`v0.1-draft` 的 tag 待收口合并 `main` 后补打，EN 翻译完成后升 `v1.0`（与 `docs/cn/anchors.md` 发版说明一致）。

## [Unreleased]

### Added
- L1 文档骨架与三层结构（L1 / L2 / L3），中文版全 8 章（Section 0–7）初稿。
  L1 doc skeleton and three-layer structure (L1 / L2 / L3); CN draft of all 8 sections (0–7).
- 锚点注册表 `docs/cn/anchors.md`，供 L2 跨 repo 版本锚定引用。
  Anchor registry `docs/cn/anchors.md` for L2 version-anchored cross-repo references.
- 契约对象独立锚点：`#platform-decision-record`（PDR 模板）、`#value-heat-map`（价值热力图），并登记进注册表与核心契约表。
  Standalone contract anchors `#platform-decision-record` (PDR template) and `#value-heat-map`, registered and added to the contracts table.
- 贡献指南 `CONTRIBUTING.md`（含锚点三处同步纪律、Portfolio 三规则、风格约定）。
  `CONTRIBUTING.md` (three-place anchor-sync discipline, the three Portfolio rules, style conventions).
- 本 `CHANGELOG.md`。
  This `CHANGELOG.md`.
- **CN 定稿前的内容审查修订**：§3 新增「建模范式的选择」（维度建模 / Data Vault / 宽表 + grain / SCD 归属）；§0.6「范围边界」显式声明有意下放的主题（TCO 模型 / 网络与密钥安全 / DR·BCP / 数据契约 / 多区域）；§2.1.4「TCO 构成」因子清单；§2.2.3 增补 Databricks PDR 示例；为借用概念补来源署名（One-Way Door → Amazon、Medallion → Databricks、Analytics Engineer → dbt Labs、DataOps / FinOps）。
  **Pre-finalization content review**: added §3 "Modeling paradigm" (dimensional / Data Vault / one-big-table + grain / SCD ownership); §0.6 "Scope boundaries" (TCO model / network & secrets security / DR·BCP / data contracts / multi-region deliberately deferred); §2.1.4 TCO factor list; a second (Databricks) PDR example in §2.2.3; source attributions for borrowed concepts (One-Way Door → Amazon, Medallion → Databricks, Analytics Engineer → dbt Labs, DataOps / FinOps).

### Changed
- 同步根 `README.md` 与 `docs/cn/README.md` 的三层结构图（Snowflake「已有」标注 + 各平台场景描述）。
  Synced the three-layer diagram across root `README.md` and `docs/cn/README.md` (Snowflake "existing" tag + per-platform scenarios).
- 统一 Requirements Profile 契约字段命名：Section 2 场景映射表字段名与 §1.5 契约对齐；PDR YAML 补维度名 ↔ Profile 字段映射注解。
  Unified `Requirements Profile` field names: §2 scenario-map fields aligned with the §1.5 contract; PDR YAML annotated with dimension ↔ Profile field mapping.
- `docs/cn/anchors.md` 增补发版说明，明确 tag 创建流程。
  Added a release note to `docs/cn/anchors.md` clarifying the tag-creation flow.
- **术语与措辞统一**：统一 `Governance-as-Code` / `Dual Running` / `True Streaming` 写法；`technology-agnostic` 定为方法论伞术语（架构原则处保留 `platform-agnostic`）；§1.4.2「关键创新」→「关键区分轴」并校准 machine-enforced、「实时被高估」两处绝对论断；§2 增补平台范围说明、§2.1.3 标注为 Snowflake 示例；§0.3 补版本 tag 成熟度注、§5.2 补 Value Heat Map 前向引用路标；三处未编号子标题补编号。
  **Terminology & wording**: unified `Governance-as-Code` / `Dual Running` / `True Streaming`; fixed `technology-agnostic` as the methodology umbrella term (kept `platform-agnostic` for the architecture principle); §1.4.2 "key innovation" → "key distinguishing axis" and calibrated two absolute claims (machine-enforced, "real-time is overrated"); added a platform-scope note in §2 and marked §2.1.3 as a Snowflake example; added a version-tag maturity note in §0.3 and a Value-Heat-Map forward-reference signpost in §5.2; numbered three previously unnumbered sub-headings.
- **导航与元信息**：`docs/en/README.md` 章节表改为链接；根 `README.md` 结构树刷新并链接 `CONTRIBUTING.md` / `CHANGELOG.md`；本 CHANGELOG 正文补英文双语；`TASK_BRIEF.md` §3 规格补建模范式。
  **Navigation & meta**: linked the section table in `docs/en/README.md`; refreshed the root `README.md` layout tree and linked `CONTRIBUTING.md` / `CHANGELOG.md`; made this changelog body bilingual; added the modeling paradigm to the §3 spec in `TASK_BRIEF.md`.

### Fixed
- 修正 `TASK_BRIEF.md` DoD 状态：Snowflake L2 外链项由「已完成」改回未完成（正文仍为占位符），消除状态矛盾。
  Corrected `TASK_BRIEF.md` DoD status: the Snowflake L2 link item reverted from "done" to not-done (body still a placeholder), removing a status contradiction.
- 内容审查修缮：补 Landing 层安全边界（未脱敏原始数据的访问最小化 / 保留期 / 落地前 tokenize）；修正 `compliance_regime` 枚举中 GDPR 的归类（通用隐私法 vs 行业监管）；限定 BigQuery「无闲置计费」仅适用按量模式；Data Observability 引言承诺的 data drift 在四支柱中落点；补充迁移对账的「比较语义先行」以避免伪方差。
  Content-review fixes: added the Landing-layer security boundary (access minimization / retention / pre-landing tokenization for un-masked raw data); corrected GDPR's classification in the `compliance_regime` enum (general privacy law vs sector regulation); scoped BigQuery "no idle billing" to on-demand mode only; landed the data-drift promise from the Data Observability intro into the four pillars; added "compare-semantics-first" to migration reconciliation to avoid pseudo-variance.
- docs-integrity CI 触发路径补入根 `*.md`（此前根文件的断链不触发 CI）；规范化两处小写仓库 URL 为 `Data_Platform_Delivery_and_Operating_Model`；修正 `CONTRIBUTING.md` 半/全角括号；修正 §0 指向 `CHANGELOG.md` 的相对路径。
  Added root `*.md` to the docs-integrity CI trigger paths (broken links in root files previously did not trigger CI); normalized two lowercase repo URLs to `Data_Platform_Delivery_and_Operating_Model`; fixed a half/full-width bracket in `CONTRIBUTING.md`; corrected the relative path from §0 to `CHANGELOG.md`.

[Unreleased]: https://github.com/xinglu-lb/Data_Platform_Delivery_and_Operating_Model/commits/main
