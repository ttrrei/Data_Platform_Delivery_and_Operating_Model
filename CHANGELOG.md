# Changelog

本文件记录 L1 文档的显著变更。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循 [语义化版本 SemVer](https://semver.org/lang/zh-CN/)。

All notable changes to this L1 document are recorded here. Format follows Keep a Changelog; versions follow SemVer.

> 版本口径：当前处于 `v0.1-draft`（CN 初稿）。git tag 一律在 `main` 分支创建——`v0.1-draft` 的 tag 待收口合并 `main` 后补打，EN 翻译完成后升 `v1.0`（与 `docs/cn/anchors.md` 发版说明一致）。

## [Unreleased]

### Added
- L1 文档骨架与三层结构（L1 / L2 / L3），中文版全 8 章（Section 0–7）初稿。
- 锚点注册表 `docs/cn/anchors.md`，供 L2 跨 repo 版本锚定引用。
- 契约对象独立锚点：`#platform-decision-record`（PDR 模板）、`#value-heat-map`（价值热力图），并登记进注册表与核心契约表。
- 贡献指南 `CONTRIBUTING.md`（含锚点三处同步纪律、Portfolio 三规则、风格约定）。
- 本 `CHANGELOG.md`。

### Changed
- 同步根 `README.md` 与 `docs/cn/README.md` 的三层结构图（Snowflake「已有」标注 + 各平台场景描述）。
- 统一 Requirements Profile 契约字段命名：Section 2 场景映射表字段名与 §1.5 契约对齐；PDR YAML 补维度名 ↔ Profile 字段映射注解。
- `docs/cn/anchors.md` 增补发版说明，明确 tag 创建流程。

### Fixed
- 修正 `TASK_BRIEF.md` DoD 状态：Snowflake L2 外链项由「已完成」改回未完成（正文仍为占位符），消除状态矛盾。
- 内容审查修缮：补 Landing 层安全边界（未脱敏原始数据的访问最小化 / 保留期 / 落地前 tokenize）；修正 `compliance_regime` 枚举中 GDPR 的归类（通用隐私法 vs 行业监管）；限定 BigQuery「无闲置计费」仅适用按量模式；Data Observability 引言承诺的 data drift 在四支柱中落点；补充迁移对账的「比较语义先行」以避免伪方差。

[Unreleased]: https://github.com/xinglu-lb/data_platform_delivery_and_operating_model/commits/main
