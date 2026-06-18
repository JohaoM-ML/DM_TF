# Documentación de notebooks

## Flujo canónico (mapping v2)

```
SCRIPTS/notebooks/01_midagri_pipeline.ipynb   → OUTPUTS/midagri_largo.csv
SCRIPTS/notebooks/02_nasa_pipeline.ipynb      → OUTPUTS/nasa_2020_2025.csv
        ↓
SCRIPTS/pipeline_integrado.py                 → dataset_integrado.csv
        ↓
SCRIPTS/notebooks/03_build_dataset_integrado.ipynb
SCRIPTS/notebooks/04_eda_regional.ipynb
SCRIPTS/notebooks/05_eda_por_cultivo.ipynb
SCRIPTS/notebooks/06_clustering_cultivos.ipynb
```

**Orquestación:** `python SCRIPTS/run_all_notebooks.py`

## Módulos Python (preferir sobre lógica en notebooks)

- `pipeline_integrado.py`, `clustering.py`, `robustez.py`, `paths.py`

## Legacy

`SCRIPTS/legacy/03_merge_y_filtrado.ipynb` — obsoleto.

Ver `DOCUMENTACIÓN/dataset_integrado.md` para esquema de columnas.
