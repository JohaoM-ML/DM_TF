# OUTPUTS

Esta carpeta **no debe contener CSV commiteados**: los artefactos se generan ejecutando los notebooks en orden:

`SCRIPTS/notebooks/01` → `02` → `03` → `04` → `05` → `06`

Tras ejecutar el pipeline completo aparecerán aquí:

- `midagri_largo.csv`, `nasa_2020_2025.csv`
- `dataset_integrado.csv`, `dataset_regional.csv`, `dataset_por_cultivo.csv`
- `clustering_perfiles.csv`, `clustering_metricas.csv`
- `figures/*.png`
