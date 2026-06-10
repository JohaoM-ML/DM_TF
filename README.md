# DM_TF — Clima y producción agrícola en el Perú (2020–2025)

Proyecto de **Data Mining** (Universidad del Pacífico, 2026-I): relación entre variables climáticas (NASA POWER) y producción agrícola (MIDAGRI) en seis regiones del Perú.

## Estructura

| Carpeta / archivo | Contenido |
|-------------------|-----------|
| `SCRIPTS/01–05` | Pipelines MIDAGRI, NASA, merge legacy y EDA |
| `build_dataset_integrado.ipynb` | Genera el dataset maestro |
| `SCRIPTS/pipeline_integrado.py` | Misma lógica por línea de comandos |
| `Clustering/` | Análisis de clustering agroclimático |
| `OUTPUTS/` | CSV y figuras generadas |
| `BDS/` | Datos originales MIDAGRI (Excel) y mapping |
| `DOCUMENTACIÓN/` | Documentación técnica del pipeline |

## Ejecución rápida

```bash
# 1. Datos intermedios (si ya existen en OUTPUTS/, saltar NB01)
jupyter nbconvert --execute SCRIPTS/02_nasa_pipeline.ipynb

# 2. Dataset integrado
python SCRIPTS/pipeline_integrado.py

# 3. Clustering
jupyter nbconvert --execute Clustering/Clustering_Cultivos.ipynb
```

## Dataset maestro

`OUTPUTS/dataset_integrado.csv` — 2.160 filas (30 cultivos Pareto-80 × 72 meses), 20 columnas.

Ver `DOCUMENTACIÓN/dataset_integrado.md` para el esquema completo.
