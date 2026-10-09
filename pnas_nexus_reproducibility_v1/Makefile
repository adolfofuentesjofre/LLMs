PYTHON ?= python3
TECTONIC ?= tectonic
LATEX_OUTPUT ?= /tmp/pnas-nexus-reproducibility-latex

.PHONY: verify reproduce-analysis test-notebooks render

verify:
	PYTHONPATH=src "$(PYTHON)" scripts/verify_release.py

reproduce-analysis:
	PYTHONPATH=src "$(PYTHON)" scripts/reproduce_analysis.py

test-notebooks:
	PYTHONPATH=src "$(PYTHON)" scripts/test_notebooks.py

render:
	mkdir -p $(LATEX_OUTPUT)/main $(LATEX_OUTPUT)/supplement
	cd manuscript && "$(TECTONIC)" -X compile main.tex --outdir "$(LATEX_OUTPUT)/main" --keep-logs
	cd manuscript && "$(TECTONIC)" -X compile supplement.tex --outdir "$(LATEX_OUTPUT)/supplement" --keep-logs
