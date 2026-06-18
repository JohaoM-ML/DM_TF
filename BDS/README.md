# BDS — Datos de entrada

## `mapping/`

Tablas de asignación región×cultivo → distrito/piso:

| Archivo | Uso |
|---------|-----|
| `mapping_cultivo_distrito_v2_pipeline.csv` | **Canónico** — insumo del notebook 03 |
| `mapping_cultivo_distrito_v2.csv` | Metadatos (confianza, justificación) |
| `mapping_cultivo_distrito_v1_legacy.csv` | Respaldo v1 |
| `mapping_cultivo_distrito.csv` | v1 histórico (referencia para comparación en notebook 00) |

**Generador:** `SCRIPTS/notebooks/00_build_mapping_cultivo_distrito.ipynb` (requiere `OUTPUTS/midagri_largo.csv`).

## Excel MIDAGRI (opcional)

Colocar archivos `BDS/YYYY/MES.xlsx` (cuadro C-18) y ejecutar notebook 01.

Si no hay Excel, usar `OUTPUTS/midagri_largo.csv` ya generado.
