
.PHONY: docs docs-docker

AICEX_DOCKER_IMAGE ?= wulffern/aicex:26.04_latest

docs:
	../jnw-actions/doc/gendoc

docs-docker:
	docker run --rm \
		-e PUID=$$(id -u) -e PGID=$$(id -g) \
		-e TAKE_UID_FROM_DIR=/home/aicex/ip/$(notdir $(CURDIR)) \
		-v $(abspath ..):/home/aicex/ip \
		-w /home/aicex/ip/$(notdir $(CURDIR)) \
		$(AICEX_DOCKER_IMAGE) \
		bash -lc 'git config --global --add safe.directory "$$PWD" && make docs'

JEKYLL_VERSION=3.8
SITE=${shell pwd}/docs

jstart:
	docker run --rm --name ${LIB}_docs --volume="${SITE}:/srv/jekyll" -p 3000:4000 -it jekyll/jekyll:${JEKYLL_VERSION} jekyll serve --watch --drafts
