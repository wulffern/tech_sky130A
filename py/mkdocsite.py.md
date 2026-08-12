# mkdocsite.py

Builds the site you are reading, from the markdown next to every file in this
repository.

```bash
python3 py/mkdocsite.py            # write docs/
python3 py/mkdocsite.py --check    # report undocumented files only
```

## The convention

```
magic/drc.tcl          the file
magic/drc.tcl.md       what it is, who runs it, what it writes
magic/README.md        what the whole folder is for
```

The prose lives beside the code, so a folder is readable on GitHub without
building anything, and there is no second place where the truth can go stale.

## What it generates

One page per file and one chapter per folder, under `docs/`, as
[just-the-docs](https://just-the-docs.com) pages with the front matter that
theme needs: `parent` for a file page, `parent` plus `grand_parent` for a file
in a nested folder such as `cicsim/cell_spice`, and `has_children` on the
folder pages. Folders are ordered alphabetically, files within a folder too.
The repository `README.md` becomes the landing page.

Each file page gets a link to the source on GitHub inserted under its heading.

Everything in `docs/` is deleted and rewritten on each run except the skeleton
(`_config.yml`, the `Gemfile`, the `.gitignore` and `docs/README.md`), so a
renamed source file cannot leave a stale page behind. `docs/.gitignore` is an
allow list of exactly those files.

## Cross links

Sources link each other the GitHub way, `[drc.tcl](drc.tcl.md)`. Those are
rewritten as the site is built: `.md` becomes `.html`, a `README.md` link
becomes the folder itself, and a leading dot is dropped, since Jekyll ignores
files that start with one and `.magicrc` is therefore published as
`magicrc.html`.

## --check

Exits non-zero, listing:

- a file with no `.md` beside it
- a folder with no `README.md`
- a `.md` documenting a file that has been deleted

The DOCS workflow runs this before building, so a new script that nobody
documented fails CI.

Standard library only, deliberately: the docs job should not need a pip
install. Files are enumerated with `git ls-files`, falling back to a walk when
git is not available.
