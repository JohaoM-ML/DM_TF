# DM_TF — Tipología agroclimática y producción agrícola en el Perú (2020–2025)

Proyecto de **Data Mining** (Universidad del Pacífico, 2026-I): pipeline reproducible en **notebooks Jupyter** que integra producción MIDAGRI y clima NASA POWER.

> **Contribución:** ingeniería de datos + tipología descriptiva (~33 perfiles Pareto-80).  
> **No demuestra:** causalidad clima→producción, rendimiento t/ha, ni predicción operativa.

## Pipeline (notebooks 01 → 06)

Toda la lógica está en `SCRIPTS/notebooks/` — **sin módulos `.py`**. Ejecutar en orden:

| # | Notebook | Genera |
|---|----------|--------|
| 01 | `01_midagri_pipeline.ipynb` | `OUTPUTS/midagri_largo.csv` |
| 02 | `02_nasa_pipeline.ipynb` | `OUTPUTS/nasa_2020_2025.csv` |
| 03 | `03_build_dataset_integrado.ipynb` | `dataset_integrado.csv` (+ regional, por cultivo) |
| 04 | `04_eda_regional.ipynb` | Figuras EDA regional |
| 05 | `05_eda_por_cultivo.ipynb` | Correlaciones exploratorias |
| 06 | `06_clustering_cultivos.ipynb` | `clustering_perfiles.csv`, métricas, figuras |

Detalle: [`SCRIPTS/notebooks/README.md`](SCRIPTS/notebooks/README.md)

```bash
pip install -r requirements.txt
# Abrir Jupyter y ejecutar 01 → 06 en orden
jupyter lab SCRIPTS/notebooks/
```

Los CSV en `OUTPUTS/` **no se versionan** — se regeneran con los notebooks.

## Estructura

```
DM_TF/
├── BDS/                    # Excel MIDAGRI + mapping (insumo)
│   └── mapping/            # mapping_cultivo_distrito_v2_pipeline.csv
├── SCRIPTS/notebooks/      # Pipeline completo (01–06)
├── OUTPUTS/                # Artefactos generados (vacío hasta ejecutar)
├── DOCUMENTACIÓN/
└── ENTREGAS/
```

## Insumos fijos

- **MIDAGRI:** Excel cuadro C-18 en `BDS/YYYY/`
- **Mapping:** `BDS/mapping/mapping_cultivo_distrito_v2_pipeline.csv`
- **NASA POWER:** descargado en notebook 02 (requiere red)

## Limitaciones

Ver [ENTREGAS/LIMITACIONES.md](ENTREGAS/LIMITACIONES.md)

## Fuentes

- MIDAGRI — Agro en Cifras (cuadro C-18)
- NASA POWER — 12 variables, 14 distritos
