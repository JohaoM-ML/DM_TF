# Documentación de notebooks

Pipeline **notebook-only** en `SCRIPTS/notebooks/`. No existen módulos Python (`pipeline_integrado.py`, `clustering.py`) en el repositorio.

## Orden de ejecución

Ver [`SCRIPTS/notebooks/README.md`](../SCRIPTS/notebooks/README.md).

## Entregables por notebook

| Notebook | Salidas principales |
|----------|---------------------|
| 00 | `BDS/mapping/mapping_cultivo_distrito_v2_pipeline.csv` |
| 01 | `OUTPUTS/midagri_largo.csv` |
| 02 | `OUTPUTS/nasa_2020_2025.csv` |
| 03 | `OUTPUTS/dataset_integrado.csv` (2.376 filas × 20 cols) |
| 04 | `OUTPUTS/figures/eda_regional_*.png` |
| 05 | Correlaciones por cultivo |
| 06 | `clustering_perfiles.csv`, `mapa_clusters_folium.html` |
| 06a | Tipologías por zona climática, `06a_mapa_zonas.html` |
| 06b | Tipologías por estacionalidad productiva |

## Esquema del dataset integrado

Ver [`dataset_integrado.md`](dataset_integrado.md).

## Comparativa de enfoques de clustering

Ver [`comparacion_clustering.md`](comparacion_clustering.md).

## Mantenimiento

Scripts en `tools/` y `SCRIPTS/annotate_notebooks.py` — solo para inyectar comentarios en celdas, no para ejecutar el pipeline.
