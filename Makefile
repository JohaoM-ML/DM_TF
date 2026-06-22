.PHONY: install test test-integration notebooks-help preprocess cluster

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	pytest tests/ -v -m "not integration"

test-integration:
	pytest tests/ -v -m integration

notebooks-help:
	@echo Pipeline:
	@echo   preprocess - SCRIPTS/notebooks/00_pipeline_integrado.ipynb (midagri, mapping, nasa, dataset_integrado.csv)
	@echo   04 - EDA y correlaciones, regional y por cultivo (SCRIPTS/notebooks/)
	@echo   06_clustering_final - clustering, dos enfoques consolidados: zonas agroclimaticas + perfiles productivos
	@echo   07_analisis_clusters - analisis profundo por cluster (medias, evolucion anual, cultivos)
	@echo   BORRADORES/ - notebooks 00-03 y 06/06a/06b originales (version previa, detalle paso a paso)

preprocess:
	$(PYTHON) SCRIPTS/run_notebook.py SCRIPTS/notebooks/00_pipeline_integrado.ipynb

cluster:
	$(PYTHON) SCRIPTS/run_notebook.py SCRIPTS/notebooks/04_eda.ipynb
	$(PYTHON) SCRIPTS/run_notebook.py SCRIPTS/notebooks/06_clustering_final.ipynb
	$(PYTHON) SCRIPTS/run_notebook.py SCRIPTS/notebooks/07_analisis_clusters.ipynb
