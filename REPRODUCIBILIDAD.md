# Reproducibilidad

Guía para clonar y ejecutar el pipeline en **cualquier computadora**.

## 1. Clonar

```bash
git clone https://github.com/JohaoM-ML/DM_TF.git
cd DM_TF
```

## 2. Entorno Python 3.12

**Opción A — pip**

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

**Opción B — conda**

```bash
conda env create -f environment.yml
conda activate dmtf
```

## 3. Insumos obligatorios

| Insumo | Ubicación | En git |
|--------|-----------|--------|
| Mapping v2 | `BDS/mapping/mapping_cultivo_distrito_v2_pipeline.csv` | Sí |
| Excel MIDAGRI C-18 | `BDS/YYYY/2020.xlsx` … `2025.xlsx` | No — ver [`BDS/YYYY/README.md`](../BDS/YYYY/README.md) |
| NASA POWER | Descargado por `00_pipeline_integrado.ipynb` | No — requiere internet |

## 4. Ejecutar pipeline

```bash
make preprocess        # ejecuta SCRIPTS/notebooks/00_pipeline_integrado.ipynb: midagri_largo, mapping, nasa, dataset_integrado
```

Luego, en Jupyter, correr en orden: `SCRIPTS/notebooks/04 → 06_clustering_final`.

Detalle: [`SCRIPTS/notebooks/README.md`](../SCRIPTS/notebooks/README.md)

## 5. Verificar

```bash
make test                  # estructura del repo (sin OUTPUTS)
make test-integration      # tras generar OUTPUTS/ (requiere CSV locales)
```

## 6. Mapas interactivos

- `OUTPUTS/figures/06a_mapa_zonas.html`, `OUTPUTS/figures/06b_mapa_perfiles.html` — notebook 06_clustering_final
- Abrir con extensión **Live Server** en Cursor/VS Code, o doble clic en el navegador

## Qué no va en git

- CSV/PNG generados en `OUTPUTS/` (se regeneran con los notebooks)
- Excel MIDAGRI en `BDS/YYYY/`
- `.ipynb_checkpoints/`, entornos virtuales

## Versiones fijadas

Dependencias pinneadas en `requirements.txt` y `environment.yml` (Python 3.12, pandas 2.2.3, scikit-learn 1.5.2, folium 0.19.5, etc.).
