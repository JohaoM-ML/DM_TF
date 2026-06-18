# DM_TF — Tipología agroclimática y producción agrícola en el Perú (2020–2025)

Proyecto de **Data Mining** (Universidad del Pacífico, 2026-I): pipeline reproducible en **notebooks Jupyter** que integra producción MIDAGRI y clima NASA POWER.

> **Contribución:** ingeniería de datos + tipología descriptiva (~33 perfiles Pareto-80).  
> **No demuestra:** causalidad clima→producción, rendimiento t/ha, ni predicción operativa.

## Inicio rápido

```bash
pip install -r requirements.txt
jupyter lab SCRIPTS/notebooks/
```

Ejecutar notebooks **en orden** (ver tabla abajo). Los CSV en `OUTPUTS/` se regeneran al correr el pipeline; no se versionan en git.

## Pipeline (notebooks)

Ubicación canónica: `SCRIPTS/notebooks/`

| # | Notebook | Genera |
|---|----------|--------|
| 01 | `01_midagri_pipeline.ipynb` | `OUTPUTS/midagri_largo.csv` |
| 00 | `00_build_mapping_cultivo_distrito.ipynb` | `BDS/mapping/mapping_cultivo_distrito_v2*.csv` |
| 02 | `02_nasa_pipeline.ipynb` | `OUTPUTS/nasa_2020_2025.csv` |
| 03 | `03_build_dataset_integrado.ipynb` | `dataset_integrado.csv` (+ regional, por_cultivo) |
| 04 | `04_eda_regional.ipynb` | Figuras EDA regional |
| 05 | `05_eda_por_cultivo.ipynb` | Correlaciones exploratorias |
| 06 | `06_clustering_cultivos.ipynb` | Clustering clima+producción, mapa Folium |
| 06a | `06a_zonas_agroclimaticas.ipynb` | Tipologías por **zona climática** (12 distritos) |
| 06b | `06b_perfiles_productivos.ipynb` | Tipologías por **patrón productivo** estacional |

Detalle: [`SCRIPTS/notebooks/README.md`](SCRIPTS/notebooks/README.md)

Guía completa: [`REPRODUCIBILIDAD.md`](REPRODUCIBILIDAD.md)

## Estructura del repositorio

```
DM_TF/
├── BDS/
│   └── mapping/              # mapping v2 (canónico: *_v2_pipeline.csv)
├── SCRIPTS/
│   ├── notebooks/            # Pipeline 00–06, 06a, 06b
│   └── legacy/               # Referencia de notebooks retirados
├── OUTPUTS/                  # Artefactos generados (CSV/PNG gitignored)
│   └── figures/              # PNG + mapas HTML (Folium, 06a)
├── DOCUMENTACIÓN/            # Esquemas, defensa, comparativa clustering
├── ENTREGAS/                 # Informe LaTeX, presentación, figuras finales
├── EXPERIMENTOS/             # Ablación mapping v1 vs v2
├── tests/                    # Layout repo + validación OUTPUTS (integración)
├── tools/                    # Scripts de mantenimiento de notebooks
└── agentes/                  # Prompts de auditoría del pipeline
```

## Insumos

| Insumo | Ubicación |
|--------|-----------|
| MIDAGRI C-18 (Excel) | `BDS/YYYY/` (local; `.xlsx` gitignored) |
| Mapping activo | `BDS/mapping/mapping_cultivo_distrito_v2_pipeline.csv` |
| NASA POWER | Descargado en notebook 02 (requiere red) |

## Tests

```bash
pytest tests/ -v                    # layout del repo (siempre)
pytest tests/ -v -m integration   # requiere OUTPUTS/ ya generados
```

## Limitaciones

Ver [ENTREGAS/LIMITACIONES.md](ENTREGAS/LIMITACIONES.md)

## Fuentes

- MIDAGRI — Agro en Cifras (cuadro C-18)
- NASA POWER — 12 variables, 14 distritos proxy
