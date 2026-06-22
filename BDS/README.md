# BDS — Base de datos e insumos

| Carpeta / archivo | Descripción |
|-------------------|-------------|
| `mapping/mapping_cultivo_distrito_v2_pipeline.csv` | **Mapping canónico** — distrito proxy por `(región, cultivo)` |
| `mapping/mapping_cultivo_distrito_v2.csv` | Mapping con metadatos de confianza |
| `mapping/mapping_cultivo_distrito_v1_legacy.csv` | Versión legacy (ablación) |
| `YYYY/*.xlsx` | Excel MIDAGRI C-18 (local; gitignored) |

Generación del mapping v2: `SCRIPTS/notebooks/00_pipeline_integrado.ipynb` (sección "Mapping").
El notebook original con detalle paso a paso quedó archivado en `BORRADORES/00_build_mapping_cultivo_distrito.ipynb`.
