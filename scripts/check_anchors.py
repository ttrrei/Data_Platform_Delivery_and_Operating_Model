#!/usr/bin/env python3
"""
Docs-integrity checker for the L1 Data Platform Delivery & Operating Model.

This repo's core promise is *stable, version-anchored, dead-link-free* cross
references (see Section 0 "Portfolio Constitution"). Those anchors are currently
maintained by hand in docs/cn/anchors.md. This script is the automated guard
that keeps that promise from silently rotting.

It checks, using only the Python standard library (no third-party deps, runs
offline):

  1. Registry parity     — every slug registered in docs/cn/anchors.md exists as
                           an <a id="..."> in the correct section file, and vice
                           versa (no orphan anchors, no ghost registrations).
  2. Comment consistency — each section's `<!-- slug-anchors: ... -->` header
                           lists exactly the <a id="..."> anchors in that file.
  3. CN/EN parity        — the English tree mirrors the Chinese one anchor-for-
                           anchor (skipped while EN is still placeholder text).
  4. Internal links      — every relative Markdown link resolves to an existing
                           file, and every `#fragment` resolves to a real anchor.
  5. Placeholder scan    — <L2-*-REPO-URL> style tokens are reported as warnings
                           (intentional until the L2 repos exist), never errors.

Exit code is non-zero if any error (not warning) is found, so CI fails loudly.

Usage:
    python3 scripts/check_anchors.py
    python3 scripts/check_anchors.py --root .
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# --- regexes ---------------------------------------------------------------

# `#slug` appearing inside a Markdown table cell (registry rows start with "|").
REGISTRY_SLUG_RE = re.compile(r"`#([a-z0-9][a-z0-9-]*)`")
A_ID_RE = re.compile(r'<a id="([a-z0-9][a-z0-9-]*)">')
SLUG_ANCHORS_COMMENT_RE = re.compile(r"<!--\s*slug-anchors:\s*(.+?)\s*-->")
# Markdown inline link: [text](target)  — target captured, images (![]) excluded.
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
# Placeholder tokens that are intentional until L2 repos land.
PLACEHOLDER_RE = re.compile(r"<L2-[A-Z0-9-]+-REPO-URL>")
# ATX heading line, e.g. "## 3.1 Medallion ...".
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")

SECTION_GLOB = "sections/[0-9][0-9]-*.md"


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.info.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def github_heading_slug(text: str) -> str:
    """Approximate GitHub's heading -> anchor slug algorithm.

    Lowercase, drop characters that are not word chars / spaces / hyphens
    (this strips punctuation and emoji), collapse spaces to hyphens. CJK code
    points are word characters under re.UNICODE, so headings keep their CJK
    which is fine — we only need this as an *extra* set of valid anchors so a
    link to a heading-without-<a id> is not falsely flagged.
    """
    text = text.strip().lower()
    text = re.sub(r"[^\w \-一-鿿]", "", text)
    text = text.replace(" ", "-")
    return text


def parse_registry(anchors_md: Path, rep: Report) -> set[str]:
    """Extract the registered slug set from docs/cn/anchors.md.

    Only slugs appearing in table rows (lines starting with '|') are counted, so
    example references like `L1@v1.2#governance-as-code` in prose are ignored.
    """
    slugs: set[str] = set()
    for line in read(anchors_md).splitlines():
        if not line.lstrip().startswith("|"):
            continue
        for m in REGISTRY_SLUG_RE.finditer(line):
            slugs.add(m.group(1))
    if not slugs:
        rep.error(f"{anchors_md}: no registered slugs found (registry parse failed).")
    return slugs


def anchors_in_file(path: Path) -> list[str]:
    return A_ID_RE.findall(read(path))


def declared_anchors_comment(path: Path) -> list[str] | None:
    m = SLUG_ANCHORS_COMMENT_RE.search(read(path))
    if not m:
        return None
    return [s.strip() for s in m.group(1).split(",") if s.strip()]


def valid_fragments(path: Path) -> set[str]:
    """All anchors that a `#fragment` may legitimately target in `path`."""
    text = read(path)
    frags = set(A_ID_RE.findall(text))
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            frags.add(github_heading_slug(m.group(1)))
    return frags


def check_tree_anchors(tree: Path, registry: set[str], lang: str, rep: Report) -> dict[str, list[str]]:
    """Check one language tree's anchors. Returns {filename: [anchors]}.

    For EN, placeholder sections (no <a id>) are tolerated: the tree is only
    held to full registry/comment parity once it is fully translated.
    """
    section_files = sorted(tree.glob(SECTION_GLOB))
    if not section_files:
        rep.error(f"[{lang}] no section files found under {tree}")
        return {}

    per_file: dict[str, list[str]] = {}
    for f in section_files:
        per_file[f.name] = anchors_in_file(f)

    files_with_anchors = [name for name, a in per_file.items() if a]

    # EN may be mid-translation. Decide the enforcement mode.
    if lang == "en" and len(files_with_anchors) == 0:
        rep.warn(f"[en] all {len(section_files)} sections are placeholders (pending translation) — anchor parity checks deferred.")
        return per_file
    if lang == "en" and len(files_with_anchors) != len(section_files):
        missing = [n for n in per_file if not per_file[n]]
        rep.error(f"[en] partially translated: {len(files_with_anchors)}/{len(section_files)} sections have anchors; still placeholder: {', '.join(missing)}")
        # keep going to surface more issues

    # Per-file: <a id> set must equal the slug-anchors comment set.
    for f in section_files:
        if not per_file[f.name]:
            continue  # placeholder, already accounted for
        ids = per_file[f.name]
        if len(ids) != len(set(ids)):
            dupes = sorted({x for x in ids if ids.count(x) > 1})
            rep.error(f"[{lang}] {f.name}: duplicate <a id>: {', '.join(dupes)}")
        declared = declared_anchors_comment(f)
        if declared is None:
            rep.error(f"[{lang}] {f.name}: missing top-of-file <!-- slug-anchors: ... --> comment.")
        elif set(declared) != set(ids):
            only_comment = set(declared) - set(ids)
            only_body = set(ids) - set(declared)
            detail = []
            if only_comment:
                detail.append(f"in comment but no <a id>: {', '.join(sorted(only_comment))}")
            if only_body:
                detail.append(f"has <a id> but not in comment: {', '.join(sorted(only_body))}")
            rep.error(f"[{lang}] {f.name}: slug-anchors comment out of sync ({'; '.join(detail)}).")

    # Whole-tree: union of anchors must equal the registry (only when complete).
    complete = not (lang == "en" and len(files_with_anchors) != len(section_files))
    if complete:
        found = set()
        for a in per_file.values():
            found.update(a)
        missing = registry - found
        extra = found - registry
        if missing:
            rep.error(f"[{lang}] registered slugs with no <a id> in any section: {', '.join(sorted(missing))}")
        if extra:
            rep.error(f"[{lang}] <a id> anchors not registered in anchors.md: {', '.join(sorted(extra))}")
        if not missing and not extra:
            rep.note(f"[{lang}] {len(found)}/{len(registry)} anchors match the registry.")

    return per_file


def doc_markdown_files(root: Path) -> list[Path]:
    """The documentation set this checker owns.

    Everything under docs/ plus the top-level doc files. `.github/` templates are
    excluded on purpose: their relative links resolve in GitHub's issue/PR
    rendering context, not against the filesystem, so static path resolution
    would produce false positives.
    """
    files = [p for p in (root / "docs").rglob("*.md") if ".git" not in p.parts]
    for name in ("README.md", "TASK_BRIEF.md", "CONTRIBUTING.md", "CHANGELOG.md"):
        p = root / name
        if p.exists():
            files.append(p)
    return sorted(files)


def check_links(root: Path, rep: Report) -> None:
    """Resolve every relative Markdown link + fragment across the doc set."""
    md_files = doc_markdown_files(root)
    frag_cache: dict[Path, set[str]] = {}

    checked = 0
    for md in md_files:
        base = md.parent
        for m in LINK_RE.finditer(read(md)):
            target = m.group(1).strip()
            # Skip autolinks/anchors we do not resolve here.
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if PLACEHOLDER_RE.search(target):
                continue  # handled by placeholder scan
            path_part, _, frag = target.partition("#")
            checked += 1

            if path_part == "":
                # Same-file fragment link.
                dest = md
            else:
                dest = (base / path_part).resolve()
                if not dest.exists():
                    rep.error(f"{md.relative_to(root)}: broken link -> {target} (no such file)")
                    continue

            if frag:
                if dest not in frag_cache:
                    frag_cache[dest] = valid_fragments(dest) if dest.suffix == ".md" else set()
                if dest.suffix == ".md" and frag not in frag_cache[dest]:
                    rep.error(f"{md.relative_to(root)}: broken anchor -> {target} (no #{frag} in {dest.name})")
    rep.note(f"resolved {checked} internal links across {len(md_files)} markdown files.")


def scan_placeholders(root: Path, rep: Report) -> None:
    count = 0
    for md in doc_markdown_files(root):
        for i, line in enumerate(read(md).splitlines(), 1):
            for m in PLACEHOLDER_RE.finditer(line):
                count += 1
                rep.warn(f"{md.relative_to(root)}:{i}: placeholder {m.group(0)} (intentional until L2 repo exists).")
    if count:
        rep.note(f"{count} known L2-URL placeholder(s) present — fill in when the L2 repos land.")


def main() -> int:
    ap = argparse.ArgumentParser(description="L1 docs integrity checker")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    rep = Report()

    anchors_md = root / "docs" / "cn" / "anchors.md"
    if not anchors_md.exists():
        print(f"FATAL: {anchors_md} not found (run from repo root or pass --root).", file=sys.stderr)
        return 2

    registry = parse_registry(anchors_md, rep)

    cn_anchors = check_tree_anchors(root / "docs" / "cn", registry, "cn", rep)
    en_anchors = check_tree_anchors(root / "docs" / "en", registry, "en", rep)

    # CN/EN parity — only when EN is fully translated.
    en_has_content = any(en_anchors.get(name) for name in en_anchors)
    en_complete = en_has_content and all(en_anchors.get(name) for name in en_anchors)
    if en_complete:
        cn_set = {a for v in cn_anchors.values() for a in v}
        en_set = {a for v in en_anchors.values() for a in v}
        if cn_set != en_set:
            only_cn = cn_set - en_set
            only_en = en_set - cn_set
            detail = []
            if only_cn:
                detail.append(f"only in CN: {', '.join(sorted(only_cn))}")
            if only_en:
                detail.append(f"only in EN: {', '.join(sorted(only_en))}")
            rep.error(f"CN/EN anchor parity broken ({'; '.join(detail)}).")
        else:
            rep.note(f"CN/EN anchor parity OK ({len(cn_set)} anchors mirror across languages).")

    check_links(root, rep)
    scan_placeholders(root, rep)

    # --- print report ---
    for msg in rep.info:
        print(f"  ok   {msg}")
    for msg in rep.warnings:
        print(f"  warn {msg}")
    for msg in rep.errors:
        print(f"  ERR  {msg}")

    print()
    if rep.errors:
        print(f"FAILED: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s).")
        return 1
    print(f"PASSED: 0 errors, {len(rep.warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
