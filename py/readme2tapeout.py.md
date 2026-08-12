# readme2tapeout.py

Converts an IP `README.md` into a Tiny Tapeout `docs/info.md`.

```bash
python3 ../tech/py/readme2tapeout.py --readme ../README.md \
                                     --out ../tapeout/docs/info.md
```

Run by `make deliver`, which then also renders it to a self contained
`info.html` with pandoc.

## The problem it solves

An IP README references images relative to the IP root, `sim/foo/bar.png`. The
tapeout `docs` folder is flat: every image must sit next to `info.md` and be
referenced by filename alone.

So every locally resolvable image is copied into the output folder with its
path flattened, and the markdown reference is rewritten. Remote images
(`http://`, `https://`, `//`) are left alone, and a missing file is reported
and skipped rather than breaking the build. When two images from different
directories share a basename, the parent directory name is prefixed so neither
is clobbered.

## Badges and links

CI badge lines are stripped, since they mean nothing in a submitted document,
and replaced with a repository and documentation link derived from the git
`origin` remote. Both the `git@github.com:owner/repo.git` and
`https://github.com/owner/repo.git` forms are understood, and the pages URL is
built as `https://<owner>.github.io/<repo>`.

## Size limits

Tiny Tapeout caps images at 512 kB each and 1 MB in total. PNGs over the limit
are re-encoded with optimization and then progressively scaled down by 15% at a
time until they fit, stopping at 320 px so the result stays readable.
Compression needs [Pillow](https://python-pillow.org); without it the sizes are
reported but not changed.

| Option | Default | Meaning |
|:-|:-|:-|
| `--readme` | `../README.md` | Source |
| `--out` | `../tapeout/docs/info.md` | Destination; images are copied beside it |
| `--compress` / `--no-compress` | compress | Shrink PNGs to fit |
| `--max-image-kb` | 512 | Per-image cap |
