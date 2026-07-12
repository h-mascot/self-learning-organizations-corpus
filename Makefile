.PHONY: audit validate generate test check

audit:
	python3 tools/corpus.py audit

validate: audit
	python3 scripts/validate_youtube.py
	python3 scripts/validate_web_media.py
	python3 scripts/generate_organization_index.py
	python3 scripts/validate_public_competitor_benchmark.py
	python3 scripts/validate_saturation.py
	python3 scripts/validate_web_media_followup.py
	python3 scripts/validate_web_media_saturation_4.py
	python3 scripts/validate_native_saturation_3.py
	python3 scripts/validate_native_saturation_4.py
	python3 scripts/validate_academic_saturation_5.py
	python3 scripts/validate_academic_saturation_6.py
	python3 scripts/generate_saturation_dashboard.py --check

generate:
	python3 tools/corpus.py generate
	python3 scripts/generate_organization_index.py
	python3 scripts/generate_saturation_dashboard.py

test:
	python3 -m unittest discover -s tests -v

check: test audit validate
	python3 tools/corpus.py generate
	python3 scripts/generate_organization_index.py
	python3 scripts/generate_saturation_dashboard.py
	git diff --exit-code -- README.md metadata/sources.csv metadata/rejected-sources.csv metadata/statistics.json metadata/organization-index.json metadata/mechanism-dashboard.json metadata/saturation.json research/company-index.md research/mechanism-dashboard.md research/saturation-dashboard.md
