.PHONY: install test test-integration notebooks-help ablation

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	pytest tests/ -v -m "not integration"

test-integration:
	pytest tests/ -v -m integration

notebooks-help:
	@echo Pipeline: SCRIPTS/notebooks/ en orden
	@echo   01 - midagri_largo.csv
	@echo   00 - mapping v2
	@echo   02 - nasa_2020_2025.csv
	@echo   03 - dataset_integrado.csv
	@echo   04-05 - EDA y correlaciones
	@echo   06 / 06a / 06b - clustering (tres enfoques)

ablation:
	$(PYTHON) EXPERIMENTOS/ablation_v1/run_ablation.py
