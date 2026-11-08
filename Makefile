.PHONY: reproduce-derived rebuild-source check-public check-sources fetch-pbdb

reproduce-derived:
	uv run tools/reproduce.py derived

rebuild-source:
	uv run tools/reproduce.py source

check-public: fetch-pbdb
	uv run --with numpy --with pandas --with scipy --with matplotlib --with pytest python -m pytest models/f3/loop3 tools/test_claims.py tools/test_reproduction.py -q

check-sources:
	uv run tools/reproduce.py sources

fetch-pbdb:
	python3 data/external/scripts/fetch_pbdb_snapshot.py
