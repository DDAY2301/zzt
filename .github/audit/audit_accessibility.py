"""Inspect accessibility of the public ZZT routes and the shared mobile navigation."""
import json
import os
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen
from xml.etree import ElementTree

from playwright.sync_api import sync_playwright

base = os.environ.get("ZZT_AUDIT_URL", "https://zavod-zzt.eu/")
axe = os.environ["AXE_SCRIPT"]
with urlopen(urljoin(base, "sitemap.xml"), timeout=20) as response:
    sitemap = ElementTree.fromstring(response.read())
routes = [urljoin(base, "/" + e.text.split("/", 3)[-1]) for e in sitemap.findall(".//{*}loc")]
assert len(routes) == 11 and len(set(routes)) == 11, routes
tags = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]

results = []
keyboard = []
reflow = []
issues = defaultdict(lambda: {"views": set(), "examples": {}})
manual = defaultdict(set)

def scan(page, mode):
    report = page.evaluate(
        "(tags) => axe.run({runOnly: {type: 'tag', values: tags}})", tags
    )
    view = f"{page.url.removeprefix(base.rstrip('/'))} {mode}"
    results.append({"view": view, "passed_rules": len(report["passes"])})
    for violation in report["violations"]:
        key = violation["id"]
        group = issues[key]
        group["views"].add(view)
        for node in violation["nodes"]:
            selector = " ".join(map(str, node["target"]))
            if len(group["examples"]) < 14:
                group["examples"].setdefault(selector, node["failureSummary"])
    for item in report["incomplete"]:
        manual[item["id"]].add(view)

def skip_link(page):
    page.keyboard.press("Tab")
    first = page.evaluate("document.activeElement.getAttribute('href')")
    page.keyboard.press("Enter")
    skipped = page.evaluate("location.hash") == "#main"
    page.keyboard.press("Tab")
    in_main = page.evaluate("Boolean(document.activeElement.closest('main'))")
    return first == "#main" and skipped and in_main

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for mode, size in (("desktop", 1440), ("mobile", 390)):
        page = browser.new_page(viewport={"width": size, "height": 850})
        for url in routes:
            response = page.goto(url, wait_until="load", timeout=25000)
            assert response and response.ok, url
            page.add_script_tag(path=axe)
            scan(page, mode)
            if mode == "mobile":
                page.set_viewport_size({"width": 320, "height": 850})
                widths = page.evaluate(
                    "[document.documentElement.scrollWidth, document.documentElement.clientWidth]"
                )
                reflow.append({"route": url, "pass": widths[0] <= widths[1] + 1,
                               "content": widths[0], "viewport": widths[1]})
                page.set_viewport_size({"width": size, "height": 850})
            if url == base:
                keyboard.append({"test": f"skip to content on {mode}", "pass": skip_link(page)})
                if mode == "mobile":
                    page.goto(base, wait_until="load")
                    page.add_script_tag(path=axe)
                    menu = page.get_by_role("button", name="Odpri navigacijo")
                    menu.press("Enter")
                    opened = page.locator(".menu-toggle").get_attribute("aria-expanded") == "true"
                    scan(page, "mobile menu open")
                    page.keyboard.press("Tab")
                    focused_nav = page.evaluate("Boolean(document.activeElement.closest('#main-nav'))")
                    page.keyboard.press("Escape")
                    closed = page.locator(".menu-toggle").get_attribute("aria-expanded") == "false"
                    restored = page.evaluate("document.activeElement.matches('.menu-toggle')")
                    keyboard.append({"test": "mobile menu keyboard operation",
                                     "pass": opened and focused_nav and closed and restored})
        page.close()
    page = browser.new_page()
    page.goto(base, wait_until="load")
    expected_titles = (
        "Okolje in primerljivi podatki",
        "Razumljive okoljske odločitve",
        "Dediščina in lokalni materiali",
    )
    for title in expected_titles:
        page.goto(base, wait_until="load")
        page.get_by_role("link", name=f"Metoda in ozadje: {title}", exact=True).press("Enter")
        heading = page.locator("h2:target")
        keyboard.append({"test": title, "pass": heading.inner_text() == title and
                         heading.evaluate("(h) => h === document.activeElement")})
    browser.close()

summary = {
    "routes": len(routes), "scans": len(results), "keyboard": keyboard, "reflow": reflow,
    "violations": {name: {"views": sorted(item["views"]), "examples": item["examples"]}
                   for name, item in sorted(issues.items())},
    "requires_manual_review": {name: sorted(views) for name, views in sorted(manual.items())},
}
Path("audit-results").mkdir(exist_ok=True)
Path("audit-results/accessibility.json").write_text(
    json.dumps({"summary": summary, "scans": results}, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(summary, ensure_ascii=False, indent=2))
