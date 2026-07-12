.PHONY: audit validate generate test check

audit:
	python3 tools/corpus.py audit

validate: audit
	python3 scripts/validate_youtube.py
	python3 scripts/validate_web_media.py
	python3 scripts/validate_saturation.py

generate:
	python3 tools/corpus.py generate

test:
	python3 -m unittest discover -s tests -v

check: test audit validate
	python3 tools/corpus.py generate
	git diff --exit-code -- README.md metadata/sources.csv metadata/rejected-sources.csv metadata/statistics.json
