# SCRIPTS

Pipeline del proyecto en **`notebooks/`** únicamente.

```
notebooks/
  00_build_mapping_cultivo_distrito.ipynb
  01_midagri_pipeline.ipynb
  02_nasa_pipeline.ipynb
  03_build_dataset_integrado.ipynb
  04_eda_regional.ipynb
  05_eda_por_cultivo.ipynb
  06_clustering_cultivos.ipynb
  06a_zonas_agroclimaticas.ipynb
  06b_perfiles_productivos.ipynb
```

| Carpeta / archivo | Uso |
|-------------------|-----|
| [`notebooks/`](notebooks/) | Pipeline canónico |
| [`legacy/`](legacy/) | Referencia de notebooks retirados de la raíz |
| `annotate_notebooks.py`, `add_hash_comments.py` | Mantenimiento (inyectar comentarios); ver también [`tools/`](../tools/) |

Orden de ejecución: [`notebooks/README.md`](notebooks/README.md)
