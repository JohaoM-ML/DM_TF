# Pipeline Jupyter — orden de ejecución

## Fase 1 — Datos

Consolidada en un único notebook: `00_pipeline_integrado.ipynb` (`make preprocess`, o
`python SCRIPTS/run_notebook.py SCRIPTS/notebooks/00_pipeline_integrado.ipynb`).
Genera `OUTPUTS/midagri_largo.csv`, `BDS/mapping/mapping_cultivo_distrito_v2*.csv`,
`OUTPUTS/nasa_2020_2025.csv` y `dataset_integrado.csv`/`dataset_regional.csv`/`dataset_por_cultivo.csv`,
en ese orden interno. Requiere Excel en `BDS/YYYY/` y acceso a la API NASA POWER.

Los 4 notebooks originales (`00`-`03`) con el detalle celda a celda quedan archivados en
[`BORRADORES/`](../../BORRADORES/) para revisión paso a paso; no forman parte del pipeline canónico.

## Fase 2 — Exploración

| # | Notebook | Genera |
|---|----------|--------|
| 04 | `04_eda.ipynb` | Figuras EDA regional y por cultivo, correlaciones, en `OUTPUTS/figures/` |

## Fase 3 — Clustering (consolidado, dos enfoques)

Consolidado en un único notebook: `06_clustering_final.ipynb` (`make cluster`, o
`python SCRIPTS/run_notebook.py SCRIPTS/notebooks/06_clustering_final.ipynb`).

| Sección | Unidad | Pregunta que responde |
|---|--------|----------------------|
| A — Zonas agroclimáticas | 28 zonas climáticas (distrito) | ¿Qué tipos de clima hay en el territorio? |
| B — Perfiles productivos | perfiles `(región, cultivo)` | ¿Qué cultivos comparten patrón productivo estacional? |

Cada sección sigue el mismo orden: explicación breve → métricas (Silhouette, ARI
KMeans-vs-Jerárquico) → mapa Folium de los clusters → gráficos complementarios
(clima/producción por cluster).

El notebook original (`06_clustering_cultivos.ipynb`, mezcla clima+producción con
barridos DBSCAN/PCA/NMF) quedó archivado en
[`BORRADORES/`](../../BORRADORES/) junto con `06a_zonas_agroclimaticas.ipynb` y
`06b_perfiles_productivos.ipynb` (detalle paso a paso de cada análisis individual,
ya integrados en `06_clustering_final.ipynb`); la razón del descarte del enfoque mixto
está documentada en la primera celda de `06_clustering_cultivos.ipynb`.

## Fase 4 — Análisis profundo por cluster

`07_analisis_clusters.ipynb` no vuelve a clusterizar: consume los CSV de
`06_clustering_final.ipynb` y profundiza en cada cluster (medias de clima/producción,
evolución anual 2020–2025, cultivos representativos), separado por sección A (zona) /
B (perfil), más allá de la visualización geográfica de puntos.

## Fase 5 — Modelo clasificador (validación de la tipología de zona)

`08_modelo_clasificador.ipynb` (autocontenido, solo lee `OUTPUTS/06a_zonas_clusters.csv`):
entrena Random Forest y KNN para recuperar el cluster de zona de cada distrito a partir
de su clima (validación cruzada Leave-One-Out + split train/test), y deja una función
(`clasificar_distrito_nuevo`) para clasificar un distrito que no esté entre los 28
originales, devolviendo el cluster más probable, el margen de confianza y el riesgo
cualitativo asociado.

## Salidas clave en OUTPUTS/

- `06a_zonas_clusters.csv`, `06a_produccion_por_zona.csv` (notebook 06, sección A)
- `06b_perfiles_productivos_clusters.csv` (notebook 06, sección B)
- `figures/06a_mapa_zonas.html`, `figures/06b_mapa_perfiles.html` — abrir con **Live Server** en Cursor
- `figures/07a_evolucion_cultivos_zona.png`, `figures/07b_evolucion_cultivos_perfil.png` (notebook 07)

## Notas

- Preprocesamiento (00-03) consolidado en `00_pipeline_integrado.ipynb`; clustering consolidado en `06_clustering_final.ipynb`. Versiones originales paso a paso (00-03 y 06/06a/06b) en `BORRADORES/`.
- Mapping canónico para el merge: `mapping_cultivo_distrito_v2_pipeline.csv`.
