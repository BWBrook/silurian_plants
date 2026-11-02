# Builds through makedoc (~/work/makedoc). uv supplies a python3 with PyYAML, leaving system Python untouched.
MAKEDOC ?= $(HOME)/work/makedoc
CONFIG := $(CURDIR)/settings/build.yaml
PROFILES := main supplement brief
RUN := uv run --no-project --with pyyaml

.PHONY: all check $(PROFILES)

all: $(PROFILES)

$(PROFILES):
	$(RUN) $(MAKE) -C "$(MAKEDOC)" CONFIG="$(CONFIG)" PROFILE=$@ all

check:
	$(foreach p,$(PROFILES),$(RUN) $(MAKE) -C "$(MAKEDOC)" CONFIG="$(CONFIG)" PROFILE=$(p) lint-manuscript refs-audit &&) true
