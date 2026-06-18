# Pipeline Jupyter — orden de ejecución

Ejecutar **en orden** para trazabilidad completa (cada notebook genera los CSV que consume el siguiente).

| # | Notebook | Genera | Requiere |
|---|----------|--------|----------|
| 01 | `01_midagri_pipeline.ipynb` | `OUTPUTS/midagri_largo.csv` | Excel en `BDS/YYYY/` |
| 02 | `02_nasa_pipeline.ipynb` | `OUTPUTS/nasa_2020_2025.csv` | Red (API NASA POWER) |
| 03 | `03_build_dataset_integrado.ipynb` | `dataset_integrado.csv`, `dataset_regional.csv`, `dataset_por_cultivo.csv` | 01, 02, mapping en `BDS/mapping/` |
| 04 | `04_eda_regional.ipynb` | Figuras en `OUTPUTS/figures/` | 03 |
| 05 | `05_eda_por_cultivo.ipynb` | `eda_correlaciones_por_cultivo.csv` | 03 |
| 06 | `06_clustering_cultivos.ipynb` | `clustering_perfiles.csv`, `clustering_metricas.csv`, figuras | 03 |

**Mapping (insumo fijo):** `BDS/mapping/mapping_cultivo_distrito_v2_pipeline.csv` — tabla de asignación cultivo→distrito/piso.

**Nota:** No hay módulos `.py` en `SCRIPTS/`; toda la lógica está en estos notebooks para legibilidad y auditoría.
