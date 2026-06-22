# SCRIPTS

Preprocesamiento y clustering, todo en `notebooks/` (notebooks Jupyter, para evidencia de flujo).

```
notebooks/
  00_pipeline_integrado.ipynb  # MIDAGRI + mapping + NASA POWER -> dataset_integrado.csv
  04_eda.ipynb
  06_clustering_final.ipynb    # zonas agroclimaticas + perfiles productivos (consolida 06/06a/06b)
  07_analisis_clusters.ipynb   # analisis profundo por cluster (medias, evolucion anual, cultivos)
```

| Carpeta / archivo | Uso |
|-------------------|-----|
| [`notebooks/00_pipeline_integrado.ipynb`](notebooks/00_pipeline_integrado.ipynb) | Preprocesamiento consolidado (reemplaza los notebooks 00-03 originales) |
| [`notebooks/`](notebooks/) | EDA y clustering (04, 06, 07) |
| [`../BORRADORES/`](../BORRADORES/) | Notebooks 00-03 y 06/06a/06b originales, archivados con detalle paso a paso |
| `run_notebook.py` | Ejecuta un notebook in-place (usado por `make preprocess`/`make cluster`) |
| `viz_style.py` | Paleta de colores y template de Plotly compartidos por los notebooks de EDA |

Orden de ejecución: `make preprocess` (o `python run_notebook.py notebooks/00_pipeline_integrado.ipynb`), luego [`notebooks/README.md`](notebooks/README.md)
