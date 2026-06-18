# Pipeline Jupyter — orden de ejecución

Ejecutar **en orden** para trazabilidad completa (cada notebook genera los CSV que consume el siguiente).

| # | Notebook | Genera | Requiere |
|---|----------|--------|----------|
| 01 | `01_midagri_pipeline.ipynb` | `OUTPUTS/midagri_largo.csv` | Excel en `BDS/YYYY/` |
| 00 | `00_build_mapping_cultivo_distrito.ipynb` | `mapping_cultivo_distrito_v2.csv`, `mapping_cultivo_distrito_v2_pipeline.csv` | 01, `mapping_cultivo_distrito.csv` (v1 ref.) |
| 02 | `02_nasa_pipeline.ipynb` | `OUTPUTS/nasa_2020_2025.csv` | Red (API NASA POWER) |
| 03 | `03_build_dataset_integrado.ipynb` | `dataset_integrado.csv`, `dataset_regional.csv`, `dataset_por_cultivo.csv` | 01, 00, 02 |
| 04 | `04_eda_regional.ipynb` | Figuras en `OUTPUTS/figures/` | 03 |
| 05 | `05_eda_por_cultivo.ipynb` | `eda_correlaciones_por_cultivo.csv` | 03 |
| 06 | `06_clustering_cultivos.ipynb` | `clustering_perfiles.csv`, `clustering_metricas.csv`, figuras | 03 |

**Mapping v2:** generado por el notebook **00** (`mapping_cultivo_distrito_v2.csv` con metadatos; `mapping_cultivo_distrito_v2_pipeline.csv` para el merge en 03).

**Nota:** No hay módulos `.py` en `SCRIPTS/`; toda la lógica está en estos notebooks para legibilidad y auditoría.
