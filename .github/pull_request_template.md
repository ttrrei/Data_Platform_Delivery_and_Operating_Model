<!--
  L1 文档 PR。请对照勾选下列纪律项——CI (docs-integrity) 会自动校验锚点与死链，
  但版本/契约/翻译纪律需要人来确认。
  L1 docs PR. Tick the discipline checklist below. CI checks anchors & dead links;
  the versioning / contract / translation discipline needs a human.
-->

## 这个 PR 改了什么 / What this changes


## 纪律检查 / Discipline checklist

- [ ] **只写差异，不重复 L3**：横切原则未在非权威章节被重写，只做引用（Portfolio Rule 1）。/ Cross-cutting principles referenced, not re-explained.
- [ ] **锚点**：新增/改动的 `<a id>` 已在 `docs/cn/anchors.md` 同步登记。/ Anchors registered in anchors.md.
- [ ] **slug 未破坏契约**：没有改动已登记的 slug；若改了，已按 breaking change 升版本并在 `docs/cn/anchors.md` 的 Deprecated 区留记录（Rule 3）。/ No registered slug renamed without a version bump + Deprecated entry.
- [ ] **契约字段名一致**：Requirements Profile / PDR / Medallion 层名等契约对象未被改名或翻译。/ Contract field names unchanged.
- [ ] **CN/EN 同步**：改了中文正文的，英文版对应内容与锚点已同步（或已在描述中说明将随后翻译）。/ EN mirror updated (or follow-up noted).
- [ ] **版本影响**：如需升版本，已更新 `CHANGELOG.md` 与 `docs/cn/anchors.md` 的版本行。/ CHANGELOG + anchors version line updated if bumping.
- [ ] `python3 scripts/check_anchors.py` 本地通过。/ Passes locally.

## 版本影响 / Version impact
<!-- none / patch / minor / major，并简述理由 -->
