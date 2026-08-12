# main.make

Documentation targets for an *IP* repository. Included from the IP root
`Makefile`, not from `work/`:

```make
LIB=MY_IP_SKY130A
CELL=MY_CELL

include tech/make/main.make
```

| Target | What it does |
|:-|:-|
| `docs` | Runs `../jnw-actions/doc/gendoc`, the same script the DOCS action runs in CI |
| `docs-docker` | The same, inside the aicex container, so the local run matches CI exactly |
| `jstart` | Serves the generated `docs/` with the `jekyll/jekyll` image on <http://localhost:3000> |

`docs` needs a checkout of
[analogicus/jnw-actions](https://github.com/analogicus/jnw-actions) beside the
IP. `docs-docker` does not: it mounts the parent directory into
`$(AICEX_DOCKER_IMAGE)`, defaulting to `wulffern/aicex:26.04_latest`, maps the
calling user's uid and gid so the generated files are not owned by root, and
marks the working tree as a safe git directory before running `make docs`
inside.

Note this is the IP documentation flow, which builds a site describing a
design's cells and simulations. The site for *this* repository is built by
[py/mkdocsite.py](../py/mkdocsite.py.md) instead.
