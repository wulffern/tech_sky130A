#!/usr/bin/env python3
"""Convert an IP README.md into a Tiny Tapeout ``docs/info.md``.

The IP ``README.md`` references images with paths relative to the IP root
(e.g. ``sim/foo/bar.png``). The tapeout ``docs`` folder is flat: images must
live next to ``info.md`` and be referenced by filename only. This script copies
every locally-resolvable image into the docs folder (flattening the path) and
rewrites the markdown references accordingly.
"""

import os
import re
import shutil
import subprocess

import click

try:
    from PIL import Image
except ImportError:
    Image = None

# Tiny Tapeout image constraints
MAX_IMAGE_BYTES = 512 * 1024
MAX_TOTAL_BYTES = 1024 * 1024

# Matches markdown images: ![alt](path "optional title")
IMG_RE = re.compile(r"!\[[^\]]*\]\(\s*([^)\s]+)(\s+\"[^\"]*\")?\s*\)")

# Matches a badge line: a clickable image link, e.g.
# [![GDS](../../actions/workflows/gds.yaml/badge.svg)](../../actions/workflows/gds.yaml)
BADGE_LINE_RE = re.compile(r"^\s*\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)\s*$", re.MULTILINE)


def is_remote(path):
    return path.startswith(("http://", "https://", "//"))


def compress_png(path, max_bytes):
    """Shrink a PNG in place until it is <= ``max_bytes``.

    First re-encodes with optimization, then progressively downscales. Returns
    the final size in bytes. Requires Pillow; a no-op if it is unavailable.
    """
    if Image is None:
        return os.path.getsize(path)

    with Image.open(path) as img:
        img = img.convert("RGBA") if img.mode == "P" else img
        img.save(path, optimize=True)

        while os.path.getsize(path) > max_bytes:
            w, h = img.size
            if w <= 320 or h <= 320:  # don't shrink below something readable
                break
            img = img.resize((int(w * 0.85), int(h * 0.85)), Image.LANCZOS)
            img.save(path, optimize=True)

    return os.path.getsize(path)


def github_links(repo_dir):
    """Return (repo_url, pages_url) from the git ``origin`` remote, or (None, None)."""
    try:
        url = subprocess.check_output(
            ["git", "-C", repo_dir, "remote", "get-url", "origin"],
            stderr=subprocess.DEVNULL, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None

    # Normalise git@github.com:owner/repo.git and https://github.com/owner/repo.git
    m = re.search(r"github\.com[:/]+([^/]+)/(.+?)(?:\.git)?$", url)
    if not m:
        return None, None
    owner, repo = m.group(1), m.group(2)
    repo_url = f"https://github.com/{owner}/{repo}"
    pages_url = f"https://{owner}.github.io/{repo}"
    return repo_url, pages_url


@click.command()
@click.option("--readme", default="../README.md", show_default=True,
              help="Source README.md to convert.")
@click.option("--out", default="../tapeout/docs/info.md", show_default=True,
              help="Destination info.md (images are copied to its folder).")
@click.option("--compress/--no-compress", default=True, show_default=True,
              help="Compress PNGs to fit the Tiny Tapeout size limits.")
@click.option("--max-image-kb", default=MAX_IMAGE_BYTES // 1024, show_default=True,
              help="Per-image size cap (kB) when compressing.")
def main(readme, out, compress, max_image_kb):
    """Copy README.md to info.md and flatten/copy referenced images."""
    max_image_bytes = max_image_kb * 1024
    if not os.path.isfile(readme):
        raise click.ClickException(f"README not found: {readme}")

    readme_dir = os.path.dirname(os.path.abspath(readme))
    out_dir = os.path.dirname(os.path.abspath(out))
    os.makedirs(out_dir, exist_ok=True)

    with open(readme, encoding="utf-8") as f:
        text = f.read()

    # Drop CI badge lines and replace them with repo / documentation links.
    text = BADGE_LINE_RE.sub("", text)
    repo_url, pages_url = github_links(readme_dir)
    if repo_url:
        links = f"- **Repository:** [{repo_url}]({repo_url})\n"
        if pages_url:
            links += f"- **Documentation:** [{pages_url}]({pages_url})\n"
        text = links + "\n" + text.lstrip("\n")
        click.echo(f"  links: repo={repo_url} pages={pages_url}")
    else:
        click.secho("  warn: could not determine github remote for links",
                    fg="yellow")

    used_names = {}   # basename -> source path (collision detection)
    total_bytes = 0

    def replace(match):
        nonlocal total_bytes
        src = match.group(1)
        title = match.group(2) or ""

        if is_remote(src):
            return match.group(0)

        src_path = os.path.normpath(os.path.join(readme_dir, src))
        if not os.path.isfile(src_path):
            click.secho(f"  skip (missing): {src}", fg="yellow")
            return match.group(0)

        name = os.path.basename(src)
        # Avoid clobbering distinct files that share a basename.
        if name in used_names and used_names[name] != src_path:
            stem, ext = os.path.splitext(name)
            parent = os.path.basename(os.path.dirname(src_path))
            name = f"{parent}_{stem}{ext}"
        used_names[name] = src_path

        dst_path = os.path.join(out_dir, name)
        shutil.copyfile(src_path, dst_path)

        orig = os.path.getsize(dst_path)
        size = orig
        if compress and name.lower().endswith(".png") and orig > max_image_bytes:
            if Image is None:
                click.secho("  warn: Pillow not installed, cannot compress",
                            fg="yellow")
            else:
                size = compress_png(dst_path, max_image_bytes)

        total_bytes += size
        note = f" (from {orig // 1024} kB)" if size < orig else ""
        if size > max_image_bytes:
            click.secho(f"  warn (>{max_image_kb}kB): {name} "
                        f"({size // 1024} kB){note}", fg="red")
        else:
            click.echo(f"  copied: {src} -> {name} ({size // 1024} kB){note}")

        return f"![]({name}{title})"

    new_text = IMG_RE.sub(replace, text)

    with open(out, "w", encoding="utf-8") as f:
        f.write(new_text)

    click.echo(f"Wrote {out} ({len(used_names)} images, "
               f"{total_bytes // 1024} kB total)")
    if total_bytes > MAX_TOTAL_BYTES:
        click.secho(
            f"warn: combined image size {total_bytes // 1024} kB exceeds "
            f"Tiny Tapeout 1 MB limit", fg="red")


if __name__ == "__main__":
    main()
