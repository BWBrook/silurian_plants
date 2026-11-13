# Builds through makedoc (~/work/makedoc). uv supplies a python3 with PyYAML, leaving system Python untouched.
MAKEDOC ?= $(HOME)/work/makedoc
CONFIG := $(CURDIR)/settings/build.yaml
PROFILES := main supplement brief
RUN := uv run --no-project --with pyyaml

.PHONY: all check check-makedoc $(PROFILES)

all: $(PROFILES)

$(PROFILES): check-makedoc
	$(RUN) $(MAKE) -C "$(MAKEDOC)" CONFIG="$(CONFIG)" PROFILE=$@ all

check-makedoc:
	@test "$$(git -C "$(MAKEDOC)" rev-parse HEAD)" = "$$(python3 -c 'import json; print(json.load(open("makedoc.lock.json"))["commit"])')" || { echo "makedoc revision differs from makedoc.lock.json"; exit 1; }
	@git -C "$(MAKEDOC)" diff --quiet HEAD -- || { echo "makedoc has tracked modifications"; exit 1; }

check: check-makedoc
	python3 ../tools/claims.py check claims.csv text/main.md text/supplement.md text/brief.md text/for-agents.md
	$(foreach p,$(PROFILES),$(RUN) $(MAKE) -C "$(MAKEDOC)" CONFIG="$(CONFIG)" PROFILE=$(p) lint-manuscript refs-audit &&) true
