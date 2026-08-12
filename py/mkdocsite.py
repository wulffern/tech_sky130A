#!/usr/bin/env python3
"""Build the just-the-docs site under ``docs/`` from the markdown in this
repository.

The site has two halves. The guides in ``guide/`` say how to use the
repository, and are ordinary numbered markdown files:

    guide/01-getting-started.md

The reference is the repository itself, documented in place:

    magic/drc.tcl          the file
    magic/drc.tcl.md       what it is, who runs it, what it writes
    magic/README.md        what the whole folder is for

This script turns both into a Jekyll site: the guides first, then one chapter
per folder and one page per file, with the sidebar, search and prev/next
navigation of ``just-the-docs``. Keeping the reference prose beside the code
means a folder is readable on GitHub without building anything, and the site
never drifts into a second copy of the truth.

    python3 py/mkdocsite.py            # write docs/
    python3 py/mkdocsite.py --check    # only report undocumented files

``--check`` exits non-zero when a file has no ``.md`` beside it, when a folder
has no ``README.md``, or when a ``.md`` documents a file that no longer exists,
so CI notices a new script that nobody wrote about.

Only the standard library is used: the docs job should not need a pip install.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

GITHUB_BLOB = "https://github.com/wulffern/tech_sky130A/blob/main"

#- Hand written files in docs/. Everything else there is generated and is
#- deleted on every run, so a renamed source file cannot leave a stale page.
DOCS_KEEP = {".gitignore", "_config.yml", "Gemfile", "Gemfile.lock", "README.md"}

#- Hand written guides, numbered to fix their order. Not sidecars: these
#- describe the flow rather than a single file.
GUIDES = "guide"

#- Directories that hold no documented sources.
SKIP_DIRS = {".git", ".github", "docs", GUIDES}

#- Files that are not documented with a sidecar (they are the documentation,
#- or they are git/infrastructure).
SKIP_FILES = {".gitignore", "README.md", "LICENSE"}

#- just-the-docs has parent / grand_parent, and nothing below that.
MAX_DEPTH = 2


def tracked_files():
    """Every file git knows about, repo relative, with '/' separators."""
    try:
        out = subprocess.check_output(
            ["git", "-C", ROOT, "ls-files", "-z"], text=True)
        files = [f for f in out.split("\0") if f]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            rel = os.path.relpath(dirpath, ROOT)
            parts = [] if rel == "." else rel.split(os.sep)
            if parts and parts[0] in SKIP_DIRS:
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for f in filenames:
                files.append("/".join(parts + [f]))
    return sorted(files)


def is_source(path):
    """True for a file that should have a ``<file>.md`` beside it."""
    parts = path.split("/")
    if parts[0] in SKIP_DIRS:
        return False
    if path.endswith(".md"):
        return False
    if parts[-1] in SKIP_FILES:
        return False
    return True


def collect():
    """Return (sources, docs) keyed by directory.

    sources[dir] -> sorted list of repo relative file paths in that directory
    docs         -> set of every tracked .md path
    """
    sources = {}
    docs = set()
    for path in tracked_files():
        if path.split("/")[0] in SKIP_DIRS:
            continue
        if path.endswith(".md"):
            docs.add(path)
            continue
        if not is_source(path):
            continue
        d = os.path.dirname(path)
        sources.setdefault(d, []).append(path)
    for d in sources:
        sources[d].sort()
    return sources, docs


#- A markdown link whose target is relative and ends in .md.
LINK_RE = re.compile(r"\]\((?!https?://|/|#)([^)\s]+\.md)(#[^)\s]*)?\)")


def site_path(md_path):
    """Where a repo markdown file ends up on the site, relative to its root."""
    d, base = os.path.split(md_path)
    if base == "README.md":
        return (d + "/") if d else "./"
    if d == GUIDES:
        return guide_slug(base) + ".html"
    return os.path.join(d, base.lstrip(".")[:-3] + ".html")


def relative_href(href, out_dir):
    """Rebase a site-root-relative href against the page that links to it."""
    start = out_dir or "."
    if href == "./":
        return os.path.relpath("index.html", start)
    rel = os.path.relpath(href.rstrip("/"), start)
    return rel + "/" if href.endswith("/") else rel


def rewrite_links(text, src_dir, out_dir):
    """Point ``.md`` cross links at the generated pages.

    The sources link each other the way GitHub wants,
    ``[drc.tcl](drc.tcl.md)``, so a folder reads correctly without building
    the site. Here that is resolved against the source's own directory and
    then re-expressed relative to the generated page, which is not the same
    place: a guide lives in ``guide/`` but is published at the site root.
    """
    def sub(m):
        target, anchor = m.group(1), m.group(2) or ""
        resolved = os.path.normpath(os.path.join(src_dir, target))
        return f"]({relative_href(site_path(resolved), out_dir)}{anchor})"

    return LINK_RE.sub(sub, text)


def read_body(path, out_dir=None):
    """Read a documentation source, stripping a trailing newline run.

    ``out_dir`` is the directory of the generated page inside ``docs/``, and
    defaults to the source's own directory.
    """
    src_dir = os.path.dirname(path)
    if out_dir is None:
        out_dir = src_dir
    with open(os.path.join(ROOT, path), encoding="utf-8") as fi:
        return rewrite_links(fi.read().rstrip("\n"), src_dir, out_dir)


def front_matter(**fields):
    lines = ["---"]
    for key, value in fields.items():
        if value is None:
            continue
        if isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, int):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f'{key}: "{value}"')
    lines.append("---")
    return "\n".join(lines) + "\n"


def page_name(basename):
    """Output file name for a page.

    Jekyll ignores files that start with a dot, so ``.magicrc`` is written as
    ``magicrc.md``. The page title keeps the real name.
    """
    return basename.lstrip(".") + ".md"


#- guide/01-getting-started.md -> getting-started
GUIDE_RE = re.compile(r"^(\d+)[-_](.+)\.md$")


def guide_slug(basename):
    m = GUIDE_RE.match(basename)
    return m.group(2) if m else basename[:-3]


def guide_files():
    """The guides, in the order their number prefix asks for."""
    d = os.path.join(ROOT, GUIDES)
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if GUIDE_RE.match(f))


def first_heading(body, fallback):
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def with_source_link(path, body):
    """Put a link to the file on GitHub under the page heading."""
    link = f"[{path}]({GITHUB_BLOB}/{path})\n{{: .fs-3 .fw-300 }}\n"
    head, sep, rest = body.partition("\n")
    if head.startswith("# "):
        return f"{head}\n{sep}{link}{rest}"
    return link + "\n" + body


def write(relpath, text):
    out = os.path.join(DOCS, relpath)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fo:
        fo.write(text)


def clean_docs():
    """Delete every generated file, keep the hand written skeleton."""
    if not os.path.isdir(DOCS):
        os.makedirs(DOCS)
        return
    for entry in os.listdir(DOCS):
        if entry in DOCS_KEEP or entry.startswith("_"):
            continue
        target = os.path.join(DOCS, entry)
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.unlink(target)


def check(sources, docs):
    """Report documentation that is missing or points at a deleted file."""
    problems = []

    for d, files in sorted(sources.items()):
        readme = f"{d}/README.md" if d else "README.md"
        if readme not in docs:
            problems.append(f"missing folder overview: {readme}")
        for path in files:
            if f"{path}.md" not in docs:
                problems.append(f"missing documentation: {path}.md")

    for doc in sorted(docs):
        if os.path.basename(doc) == "README.md":
            d = os.path.dirname(doc)
            if d and d not in sources:
                problems.append(f"orphan folder overview: {doc} (no files)")
            continue
        target = doc[:-3]
        if not os.path.exists(os.path.join(ROOT, target)):
            problems.append(f"orphan documentation: {doc} (no {target})")

    return problems


def build(sources, docs):
    """Write the whole site under docs/."""
    clean_docs()

    #- Landing page: the repository README.
    write("index.md",
          front_matter(layout="default", title="tech_sky130A", nav_order=0)
          + "\n" + read_body("README.md") + "\n")

    #- Guides first, in their numbered order, published at the site root.
    guides = guide_files()
    for i, base in enumerate(guides):
        body = read_body(f"{GUIDES}/{base}", out_dir="")
        write(guide_slug(base) + ".md",
              front_matter(layout="default",
                           title=first_heading(body, guide_slug(base)),
                           nav_order=i + 1)
              + "\n" + body + "\n")

    dirs = sorted(sources)
    toplevel = [d for d in dirs if "/" not in d]

    #- Then the reference, after every guide.
    base_order = len(guides) + 1
    order = {d: (base_order + i) * 10 for i, d in enumerate(toplevel)}

    for d in dirs:
        parts = d.split("/")
        if len(parts) - 1 > MAX_DEPTH:
            raise SystemExit(
                f"ERROR: {d} is nested deeper than just-the-docs can show")

        name = parts[-1]
        parent = parts[-2] if len(parts) > 1 else None
        grand = parts[-3] if len(parts) > 2 else None

        #- Sub folders sort before the files of their parent folder.
        nav = order.get(d, 1)

        body = read_body(f"{d}/README.md")
        write(f"{d}/index.md",
              front_matter(layout="default", title=name, parent=parent,
                           grand_parent=grand, nav_order=nav,
                           has_children=True)
              + "\n" + body + "\n")

        for i, path in enumerate(sources[d]):
            base = os.path.basename(path)
            body = read_body(f"{path}.md")
            write(f"{d}/{page_name(base)}",
                  front_matter(layout="default", title=base, parent=name,
                               grand_parent=parent, nav_order=100 + i)
                  + "\n" + with_source_link(path, body) + "\n")

    pages = sum(len(v) for v in sources.values()) + len(dirs) + len(guides) + 1
    print(f"INFO: wrote {pages} pages to docs/ "
          f"({len(guides)} guides, {len(dirs)} folders)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="only report missing or orphan documentation")
    args = ap.parse_args()

    sources, docs = collect()
    problems = check(sources, docs)

    for p in problems:
        print(f"ERROR: {p}", file=sys.stderr)

    if args.check:
        if problems:
            print(f"\n{len(problems)} problem(s)", file=sys.stderr)
            return 1
        print("INFO: every file is documented")
        return 0

    if problems:
        print("\nWARNING: building anyway, pages above will be missing",
              file=sys.stderr)

    build(sources, docs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
