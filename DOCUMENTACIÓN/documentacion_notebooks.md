# Documentación de notebooks

Todo el pipeline vive en notebooks (`SCRIPTS/notebooks/`) para conservar evidencia de
ejecución celda a celda. Los notebooks 00-03 originales (versión previa, mismo detalle
paso a paso) quedaron archivados en `BORRADORES/`.

## Orden de ejecución

`make preprocess` (ejecuta `00_pipeline_integrado.ipynb`), luego ver
[`SCRIPTS/notebooks/README.md`](../SCRIPTS/notebooks/README.md).

## Entregables

| Notebook | Salidas principales |
|----------|---------------------|
| 00 (`pipeline_integrado`) | `BDS/mapping/mapping_cultivo_distrito_v2_pipeline.csv`, `OUTPUTS/midagri_largo.csv`, `OUTPUTS/nasa_2020_2025.csv`, `OUTPUTS/dataset_integrado.csv` (2.376 filas × 20 cols) |
| 04 (`eda`) | Figuras EDA regional y por cultivo, correlaciones |
| 06 | `clustering_perfiles.csv`, `mapa_clusters_folium.html` |
| 06a | Tipologías por zona climática, `06a_mapa_zonas.html` |
| 06b | Tipologías por estacionalidad productiva |

## Esquema del dataset integrado

Ver [`dataset_integrado.md`](dataset_integrado.md).

## Mantenimiento

