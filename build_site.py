from __future__ import annotations

import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = Path(os.environ.get("BUILD_OUTPUT", ROOT / "_site"))

SITE_URL = "https://heroeemprendedor.github.io/"

EXCLUDE_NAMES = {
    ".git",
    ".github",
    "_site",
    "__pycache__",
    "content",
    "README.md",
    "build_site.py",
}


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_NAMES for part in path.parts)


def iter_site_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if path.is_dir() or should_skip(path.relative_to(ROOT)):
            continue
        files.append(path)
    return sorted(files)


def copy_site() -> list[str]:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    routes: list[str] = []

    for src in iter_site_files():
        relative = src.relative_to(ROOT)
        dest = OUTPUT / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

        if src.name == "index.html":
            route = "/" + str(relative.parent).replace(os.sep, "/").strip(".")
            routes.append(route if route != "/." else "/")

    return sorted(set("/" if route in {"", "/."} else route.rstrip("/") + "/" for route in routes))


def write_sitemap(routes: list[str]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for route in routes:
        absolute = f"{SITE_URL.rstrip('/')}{route}"
        lines.extend(["  <url>", f"    <loc>{absolute}</loc>", "  </url>"])

    lines.append("</urlset>")
    (OUTPUT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_robots() -> None:
    robots_path = OUTPUT / "robots.txt"
    lines = ["User-agent: *", "Allow: /", f"Sitemap: {SITE_URL}sitemap.xml", ""]
    robots_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    routes = copy_site()
    write_sitemap(routes)
    update_robots()


if __name__ == "__main__":
    main()
