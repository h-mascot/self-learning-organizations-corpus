.PHONY: audit generate test check

audit:
	python3 tools/corpus.py audit

generate:
	python3 tools/corpus.py generate

test:
	python3 -m unittest discover -s tests -v

check: test audit
	python3 tools/corpus.py generate
	git diff --exit-code -- README.md metadata/sources.csv metadata/rejected-sources.csv metadata/statistics.json
