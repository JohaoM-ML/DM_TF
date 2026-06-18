.PHONY: install notebooks-help

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

# El pipeline se ejecuta manualmente en Jupyter, en orden 01 → 00 → 02 → 03 → 06.
# Ver SCRIPTS/notebooks/README.md
notebooks-help:
	@echo Pipeline: ejecutar en orden SCRIPTS/notebooks/
	@echo   01 -> OUTPUTS/midagri_largo.csv
	@echo   00 -> BDS/mapping/mapping_cultivo_distrito_v2*.csv
	@echo   02 -> OUTPUTS/nasa_2020_2025.csv
	@echo   03 -> OUTPUTS/dataset_integrado.csv (+ regional, por_cultivo)
	@echo   04-05 -> EDA y correlaciones
	@echo   06 -> clustering_perfiles.csv
