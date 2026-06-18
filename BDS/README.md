# BDS — Base de datos e insumos

| Carpeta / archivo | Descripción |
|-------------------|-------------|
| `mapping/mapping_cultivo_distrito_v2_pipeline.csv` | **Mapping canónico** — distrito proxy por `(región, cultivo)` |
| `mapping/mapping_cultivo_distrito_v2.csv` | Mapping con metadatos de confianza |
| `mapping/mapping_cultivo_distrito_v1_legacy.csv` | Versión legacy (ablación) |
| `mapping/mapping_cultivo_distrito.csv` | Referencia v1 |
| `YYYY/*.xlsx` | Excel MIDAGRI C-18 (local; gitignored) |

Generación del mapping v2: notebook `SCRIPTS/notebooks/00_build_mapping_cultivo_distrito.ipynb`.
