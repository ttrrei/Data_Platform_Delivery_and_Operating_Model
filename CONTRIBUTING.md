# 贡献指南 / Contributing

> 本文档是 **L1 — technology-agnostic 方法论**。它的价值在于**稳定、可版本锚定、无死链**的跨 repo 引用契约(见 [Portfolio 宪法](docs/cn/sections/00-what-this-document-is.md#portfolio-constitution)）。贡献前请先读完本指南。
>
> This repo is an **L1 technology-agnostic methodology**. Its value is a **stable, version-anchored, dead-link-free** cross-repo reference contract. Please read this guide before contributing.

先读一遍总览 [`README.md`](README.md) 与写作 SOP [`TASK_BRIEF.md`](TASK_BRIEF.md)，理解文档定位与章节产出规划。

---

## 1. 语言与权威源 / Language & source of truth

| 约定 | 说明 |
|---|---|
| **中文为权威源（single source of truth）** | 先完成 [中文版](docs/cn/README.md) 并作为定稿依据；表述冲突时以 CN 为准。 |
| **英文版为镜像** | EN 待 CN 定稿后统一翻译，**结构与锚点（slug）与 CN 逐一对齐**，便于 L2 跨语言引用。 |
| **中文叙述 + 英文术语** | 术语首次出现给英文，后续可中英混用。 |

---

## 2. 三条不可破坏的规则 / The three hard rules

完整论述见 [Portfolio 宪法](docs/cn/sections/00-what-this-document-is.md#portfolio-constitution) 与[三层结构](docs/cn/sections/00-what-this-document-is.md#three-layer-structure)。

1. **L1 定义原则，L2 只写差异。** 任何 platform-agnostic 的方法论只在 L1 定义一次；非权威章节只引用、不重写。
2. **横切章节是唯一权威源。** L1 与某个 L2 冲突时以 L1 为准；L2 若发现原则不适用，走 issue 修订 L1，不在 L2 私自改写。
3. **跨 repo 引用必须版本锚定。** L2 外链 L1 用带版本 tag 的稳定锚点 `L1@<tag>#<slug>`，不链 `main` 浮动内容。

---

## 3. 锚点纪律（最容易踩的坑）/ Anchor discipline

每个可被 L2 引用的锚点是一份**契约**，登记在 [`docs/cn/anchors.md`](docs/cn/anchors.md)。**新增或改动锚点时，必须同步三处，缺一即为不一致：**

| # | 位置 | 内容 |
|---|---|---|
| ① | section 正文 | `<a id="your-slug"></a>` 标签（置于对应标题前） |
| ② | 该 section 文件顶部 | `<!-- slug-anchors: ... -->` 注释中列出该文件全部 slug |
| ③ | 注册表 | [`docs/cn/anchors.md`](docs/cn/anchors.md) 增加一行 |

规则：

- **新增只能 append**，不复用已废弃 slug。
- **改一个已登记的 slug = breaking change**：必须升版本 tag，并在 `anchors.md` 的 Deprecated 区留记录与替代项。
- 契约对象命名（如 [Requirements Profile](docs/cn/sections/01-strategic-alignment.md#requirements-profile) 的字段、Medallion 层名、PDR）**不得随意改名或翻译**——下游按同名引用。

---

## 4. 风格约定 / Style

- **表优于 bullet**：决策维度、对比、映射用表格。
- 平台特定内容走「各平台实现差异」附注，或剥离到 L2，不进 L1 正文。
- 详见 [`TASK_BRIEF.md`](TASK_BRIEF.md) 第 1 节全局约束。

---

## 5. 提交前自检 / Before you open a PR

- 本仓库配有 docs-integrity 检查器 `scripts/check_anchors.py`（纯标准库，离线）：校验锚点注册表双向一致、CN/EN 对等、内部链接与 `#fragment` 无死链。提交前本地运行一次：`python3 scripts/check_anchors.py`。CI 也会在 PR 上自动跑。
- 逐条对照 PR 模板 `.github/pull_request_template.md` 的纪律 checklist。
- 涉及锚点新增/变更或 L1 原则修订，请用 `.github/ISSUE_TEMPLATE/` 下对应模板先开 issue。
- 若发生版本变更，更新 [`CHANGELOG.md`](CHANGELOG.md) 与 [`docs/cn/anchors.md`](docs/cn/anchors.md) 的版本行。

> 说明：上述 `scripts/` 与 `.github/` 的脚手架随 docs-integrity 分支合入 `main` 后生效；本文件先行落地以消除对它的悬空引用。
