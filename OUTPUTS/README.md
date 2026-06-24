# OUTPUTS

Artefactos **generados** por los notebooks. Los CSV y PNG no se versionan (ver `.gitignore`).

## Orden de generación

`00_pipeline_integrado.ipynb` (midagri → mapping → nasa → integrado) → notebooks `04 → 06_clustering_final`

## Archivos principales

| Archivo | Origen |
|---------|--------|
| `midagri_largo.csv` | notebook 00 |
| `nasa_2020_2025.csv` | notebook 00 |
| `dataset_integrado.csv` | notebook 00 |
| `dataset_regional.csv`, `dataset_por_cultivo.csv` | notebook 00 |
| `06a_zonas_clusters.csv`, `06a_produccion_por_zona.csv` | notebook 06 (sección A) |
| `06b_perfiles_productivos_clusters.csv` | notebook 06 (sección B) |

## Figuras

| Archivo | Origen |
|---------|--------|
| `figures/06a_mapa_zonas.html` | 06 — sección A, mapa interactivo (Live Server) |
| `figures/06b_mapa_perfiles.html` | 06 — sección B, mapa interactivo (Live Server) |
| `figures/*.png` | 04, 06 (dendrogramas, heatmaps, EDA) |

Copias para el informe: `ENTREGAS/figures/`
