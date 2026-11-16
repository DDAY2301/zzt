#!/usr/bin/env python3
"""Synchronize the deployed static site into repository root.

GitHub Pages supports branch-root publishing as well as Actions publishing.
Keeping both root and site/ identical prevents a branch-based Pages build
from serving README.md instead of the actual ZZT website.
Only files originating under site/ are copied.
"""
from pathlib import Path
import shutil
import json

root = Path(__file__).resolve().parents[1]
site = root / "site"
manifest_path = root / ".pages-root-manifest.json"
if not (site / "index.html").is_file():
    raise SystemExit("Expected generated site/index.html")

new_paths = set()
for source in sorted(site.rglob("*")):
    if not source.is_file():
        continue
    relative = source.relative_to(site)
    target = root / relative
    if ".git" in relative.parts or relative.parts[0] in ("src", "docs", ".github"):
        raise SystemExit(f"Unsafe site path: {relative}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    new_paths.add(relative.as_posix())

old_paths = set(json.loads(manifest_path.read_text(encoding="utf-8"))) if manifest_path.exists() else set()
for relative in old_paths - new_paths:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise SystemExit("Unsafe previous manifest entry")
    target = root / path
    if target.is_file():
        target.unlink()

manifest_path.write_text(json.dumps(sorted(new_paths), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
assert (root / "index.html").read_bytes() == (site / "index.html").read_bytes()
assert (root / "assets" / "site.css").read_bytes() == (site / "assets" / "site.css").read_bytes()
assert (root / "assets" / "site.js").read_bytes() == (site / "assets" / "site.js").read_bytes()
print(f"Mirrored {len(new_paths)} public assets in root; branch publishing can serve the same website.")
