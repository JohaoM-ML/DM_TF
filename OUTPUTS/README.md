# OUTPUTS

Artefactos **generados** por los notebooks. Los CSV y PNG no se versionan (ver `.gitignore`).

## Orden de generación

`01 → 00 → 02 → 03 → 04 → 05 → 06` (opcional: `06a`, `06b`)

## Archivos principales

| Archivo | Notebook |
|---------|----------|
| `midagri_largo.csv` | 01 |
| `nasa_2020_2025.csv` | 02 |
| `dataset_integrado.csv` | 03 |
| `dataset_regional.csv`, `dataset_por_cultivo.csv` | 03 |
| `clustering_perfiles.csv`, `clustering_metricas.csv` | 06 |

## Figuras

| Archivo | Origen |
|---------|--------|
| `figures/mapa_clusters_folium.html` | 06 — mapa interactivo (Live Server) |
| `figures/06a_mapa_zonas.html` | 06a |
| `figures/*.png` | 04–06 (dendrogramas, heatmaps, EDA) |

Copias para el informe: `ENTREGAS/figures/`
