# F3 reproduction targets. Run from anywhere with `make -C studies/f3 <target>`; commands run at the repository root.
ROOT := $(abspath $(CURDIR)/../..)

.PHONY: reproduce-derived rebuild-source check-public check-sources fetch-pbdb

reproduce-derived:
	cd $(ROOT) && uv run studies/f3/tools/reproduce.py derived

rebuild-source:
	cd $(ROOT) && uv run studies/f3/tools/reproduce.py source

check-public: fetch-pbdb
	cd $(ROOT) && uv run --with numpy --with pandas --with scipy --with matplotlib --with pytest python -m pytest studies/f3/models/loop3 tools/test_claims.py studies/f3/tools/test_reproduction.py -q

check-sources:
	cd $(ROOT) && uv run studies/f3/tools/reproduce.py sources

fetch-pbdb:
	cd $(ROOT) && python3 data/external/scripts/fetch_pbdb_snapshot.py
