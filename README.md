# DM_TF — Tipología agroclimática y producción agrícola en el Perú (2020–2025)

Proyecto de **Data Mining** (Universidad del Pacífico, 2026-I): pipeline reproducible en **notebooks Jupyter** que integra producción MIDAGRI y clima NASA POWER.

> **Contribución:** ingeniería de datos + tipología descriptiva (~33 perfiles Pareto-80).  
> **No demuestra:** causalidad clima→producción, rendimiento t/ha, ni predicción operativa.

## Inicio rápido

```bash
pip install -r requirements.txt
make preprocess
jupyter lab SCRIPTS/notebooks/
```

`00_pipeline_integrado.ipynb` (notebook, evidencia de flujo celda a celda) genera los insumos (MIDAGRI, mapping, NASA, dataset integrado); luego se ejecutan los notebooks de exploración y clustering **en orden** (ver tabla abajo). Los CSV en `OUTPUTS/` se regeneran al correr el pipeline; no se versionan en git.

## Pipeline

| Paso | Genera |
|------|--------|
| `SCRIPTS/notebooks/00_pipeline_integrado.ipynb` | `OUTPUTS/midagri_largo.csv`, `BDS/mapping/mapping_cultivo_distrito_v2*.csv`, `OUTPUTS/nasa_2020_2025.csv`, `dataset_integrado.csv` (+ regional, por_cultivo) |

Detalle paso a paso de esta etapa (notebooks 00-03 originales, archivados): [`BORRADORES/`](BORRADORES/)

| # | Notebook | Genera |
|---|----------|--------|
| 04 | `04_eda.ipynb` | Figuras EDA regional y por cultivo, correlaciones exploratorias |
| 06 | `06_clustering_final.ipynb` | Clustering consolidado: zonas agroclimáticas (clima puro, 28 distritos) + perfiles productivos (patrón estacional por cultivo), con mapas Folium y ARI por método |
| 07 | `07_analisis_clusters.ipynb` | Análisis profundo por cluster (medias clima/producción, evolución anual, cultivos representativos) |

Detalle: [`SCRIPTS/notebooks/README.md`](SCRIPTS/notebooks/README.md)

Guía completa: [`REPRODUCIBILIDAD.md`](REPRODUCIBILIDAD.md)

## Estructura del repositorio

```
DM_TF/
├── BDS/
│   └── mapping/              # mapping v2 (canónico: *_v2_pipeline.csv)
├── SCRIPTS/
│   ├── notebooks/            # 00 preprocesamiento, 04 EDA, 06 clustering (consolidado), 07 analisis por cluster
│   ├── run_notebook.py       # Ejecuta un notebook in-place
│   └── viz_style.py          # Paleta y template de Plotly compartidos
├── BORRADORES/                # Notebooks 00-03 y 06/06a/06b originales, archivados
├── OUTPUTS/                  # Artefactos generados (CSV/PNG gitignored)
│   └── figures/              # PNG + mapas HTML (Folium, 06a/06b)
├── DOCUMENTACIÓN/            # Esquemas, defensa
├── ENTREGAS/                 # Informe LaTeX, presentación, figuras finales
├── EXPERIMENTOS/             # Ablación mapping v1 vs v2
├── tests/                    # Layout repo + validación OUTPUTS (integración)
└── agentes/                  # Prompts de auditoría del pipeline
```

## Insumos

| Insumo | Ubicación |
|--------|-----------|
| MIDAGRI C-18 (Excel) | `BDS/YYYY/` (local; `.xlsx` gitignored) |
| Mapping activo | `BDS/mapping/mapping_cultivo_distrito_v2_pipeline.csv` |
| NASA POWER | Descargado por `00_pipeline_integrado.ipynb` (requiere red) |

## Tests

```bash
pytest tests/ -v                    # layout del repo (siempre)
pytest tests/ -v -m integration   # requiere OUTPUTS/ ya generados
```

## Limitaciones

Ver [ENTREGAS/LIMITACIONES.md](ENTREGAS/LIMITACIONES.md)

## Fuentes

- MIDAGRI — Agro en Cifras (cuadro C-18)
- NASA POWER — 12 variables, 34 distritos proxy (14 originales + 20 refinados con SISAGRI)
