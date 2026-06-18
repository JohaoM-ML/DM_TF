# Pipeline Jupyter — orden de ejecución

Ejecutar **en orden** para trazabilidad completa (cada notebook consume los CSV del anterior).

## Fase 1 — Datos

| # | Notebook | Genera | Requiere |
|---|----------|--------|----------|
| 01 | `01_midagri_pipeline.ipynb` | `OUTPUTS/midagri_largo.csv` | Excel en `BDS/YYYY/` |
| 00 | `00_build_mapping_cultivo_distrito.ipynb` | `mapping_cultivo_distrito_v2*.csv` | 01, mapping v1 ref. |
| 02 | `02_nasa_pipeline.ipynb` | `OUTPUTS/nasa_2020_2025.csv` | Red (API NASA POWER) |
| 03 | `03_build_dataset_integrado.ipynb` | `dataset_integrado.csv`, `dataset_regional.csv`, `dataset_por_cultivo.csv` | 01, 00, 02 |

## Fase 2 — Exploración

| # | Notebook | Genera |
|---|----------|--------|
| 04 | `04_eda_regional.ipynb` | Figuras EDA en `OUTPUTS/figures/` |
| 05 | `05_eda_por_cultivo.ipynb` | Correlaciones por cultivo |

## Fase 3 — Clustering (tres enfoques)

| # | Notebook | Unidad | Pregunta que responde |
|---|----------|--------|----------------------|
| 06 | `06_clustering_cultivos.ipynb` | 33 perfiles `(región, cultivo)` | Tipología clima + producción (KMeans, jerárquico, DBSCAN) + **mapa Folium** |
| 06a | `06a_zonas_agroclimaticas.ipynb` | ~12 zonas climáticas | ¿Qué tipos de clima hay en el territorio? |
| 06b | `06b_perfiles_productivos.ipynb` | 33 perfiles | ¿Qué cultivos comparten patrón productivo estacional? |

Comparativa metodológica: [`DOCUMENTACIÓN/comparacion_clustering.md`](../../DOCUMENTACIÓN/comparacion_clustering.md)

## Salidas clave en OUTPUTS/

- `clustering_perfiles.csv`, `clustering_metricas.csv` (notebook 06)
- `figures/mapa_clusters_folium.html` — abrir con **Live Server** en Cursor
- `figures/06a_mapa_zonas.html` (notebook 06a)

## Notas

- Toda la lógica está en notebooks; no hay `pipeline_integrado.py`.
- Mapping canónico para el merge: `mapping_cultivo_distrito_v2_pipeline.csv`.
