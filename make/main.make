
.PHONY: docs

docs:
	../jnw-actions/doc/gendoc

JEKYLL_VERSION=3.8
SITE=${shell pwd}/docs

jstart:
	docker run --rm --name ${LIB}_docs --volume="${SITE}:/srv/jekyll" -p 3000:4000 -it jekyll/jekyll:${JEKYLL_VERSION} jekyll serve --watch --drafts
