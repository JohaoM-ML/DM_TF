# Dataset integrado — documentación técnica

**Proyecto:** Relación clima–producción agrícola en el Perú (2020–2025)  
**Universidad del Pacífico — Data Mining 2026-I**

---

## Propósito

`dataset_integrado.csv` es la **tabla maestra** para clustering, modelado y análisis multivariado. Una fila por `(región, cultivo, año, mes)` con producción mensual y las 12 variables climáticas del distrito asignado al cultivo.

Los notebooks `04_eda_regional.ipynb` y `05_eda_por_cultivo.ipynb` siguen siendo el lugar del EDA exploratorio. Este dataset no reemplaza ese trabajo; concentra el merge corregido en un único CSV reproducible.

---

## Cómo generarlo

### Opción A — Notebook unificado (recomendado)

1. Ejecutar `SCRIPTS/01_midagri_pipeline.ipynb` → `OUTPUTS/midagri_largo.csv`
2. Ejecutar `SCRIPTS/02_nasa_pipeline.ipynb` → `OUTPUTS/nasa_2020_2025.csv`
3. Ejecutar `build_dataset_integrado.ipynb` (raíz del proyecto)

### Opción B — Script Python

```bash
python SCRIPTS/pipeline_integrado.py
```

Ambas rutas usan la misma lógica en `SCRIPTS/pipeline_integrado.py`.

---

## Archivos de salida

| Archivo | Filas | Descripción |
|---------|------:|-------------|
| `dataset_integrado.csv` | 2.160 | **Maestro Pareto-80** — uso principal para ML/clustering |
| `dataset_por_cultivo.csv` | 14.400 | Análisis B completo (todos los cultivos con mapping) |
| `dataset_regional.csv` | 1.008 | Análisis A por piso ecológico |
| `dataset_por_cultivo_filtrado.csv` | 2.160 | Copia legacy de `dataset_integrado` (compatibilidad NB03/05) |

**Dimensiones del maestro:** 30 combinaciones `(región, cultivo)` × 72 meses = 2.160 filas × 20 columnas.

### Pareto-80 por región (corregido)

| Región | Cultivos | % acumulado |
|--------|:--------:|------------:|
| Ica | 7 | 81,3% |
| Junín | 8 | 81,7% |
| La Libertad | 4 | 82,1% |
| Piura | 4 | 90,6% |
| Puno | 3 | 92,0% |
| San Martín | 4 | 84,4% |

Antes del fix (NB03 original): 24 combinaciones y 1.728 filas (~74–80% acumulado por región).

---

## Esquema de columnas

### Metadatos (8)

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `region` | str | Una de las 6 regiones objetivo |
| `piso_ecologico` | str | Piso ecológico del cultivo (costa, sierra, selva, etc.) |
| `distrito` | str | Distrito representativo del clima (14 distritos NASA) |
| `cultivo` | str | Nombre canónico del cultivo |
| `anio` | int | 2020–2025 |
| `numero_mes` | int | 1–12 |
| `mes` | str | Nombre del mes |
| `produccion_ton` | float | Producción mensual real (toneladas), tras `diff` en MIDAGRI |

### Variables climáticas (12)

Nombres legibles en español. El CSV intermedio `nasa_2020_2025.csv` conserva los códigos NASA; el renombrado ocurre al exportar los datasets finales.

| Columna exportada | Código NASA | Unidad / significado |
|-------------------|-------------|----------------------|
| `temp_promedio` | `t2m` | Temperatura media a 2 m (°C) |
| `temp_maxima` | `t2m_max` | Temperatura máxima a 2 m (°C) |
| `temp_minima` | `t2m_min` | Temperatura mínima a 2 m (°C) |
| `precipitacion` | `prectotcorr` | Precipitación corregida (mm/día) |
| `humedad_relativa` | `rh2m` | Humedad relativa a 2 m (%) |
| `radiacion_solar` | `allsky_sfc_sw_dwn` | Radiación solar superficial (MJ/m²/día) |
| `velocidad_viento` | `ws2m` | Velocidad del viento a 2 m (m/s) |
| `presion_atmosferica` | `ps` | Presión superficial (kPa) |
| `humedad_suelo` | `gwetroot` | Humedad del suelo en zona radicular (0–1) |
| `temp_superficie` | `ts` | Temperatura de superficie (°C) |
| `punto_rocio` | `t2mdew` | Punto de rocío a 2 m (°C) |
| `humedad_especifica` | `qv2m` | Humedad específica a 2 m (kg/kg) |

**Dataset regional** (`dataset_regional.csv`): mismas variables climáticas; metadatos `produccion_piso_ton` y `num_cultivos` en lugar de `produccion_ton` y `cultivo`.

---

## Correcciones respecto a `03_merge_y_filtrado.ipynb`

### 1. Pareto-80

**Problema:** `acum[acum <= 0.80]` cortaba antes de alcanzar el 80% (p. ej. Ica quedaba en 74,4% con 6 cultivos).

**Solución:** incluir cultivos hasta el primero con acumulado **≥ 80%**:

```python
if (acum >= umbral).any():
    idx = (acum >= umbral).idxmax()
else:
    idx = acum.index[-1]
cultivos_top = acum.loc[:idx].index.tolist()
```

### 2. Agregado regional (Análisis A)

**Problema:** `groupby().sum()` convertía meses 100% NaN (may-2021, mar-2022) en `0.0`.

**Solución:** `sum(min_count=1)` — si todos los valores del grupo son NaN, el resultado es NaN.

### Validación tras la ejecución (2026-06-09)

| Métrica | Valor |
|---------|-------|
| `max_diff_a_b` | ~2,3×10⁻¹⁰ (coherencia A ↔ B) |
| NaN en variables climáticas | 0 |
| NaN en `produccion_ton` (integrado) | 170 |
| NaN en `produccion_piso_ton` (regional) | 70 |

Los NaN en producción son **esperados**: meses sin dato MIDAGRI o revisiones negativas convertidas a NaN en NB01. No se imputan.

---

## Uso en clustering

**Input:** `OUTPUTS/dataset_integrado.csv` (2.160 filas mensuales).

**Notebook:** `Clustering/Clustering_Cultivos.ipynb`

| Enfoque | Unidad | Descripción |
|---------|--------|-------------|
| **Principal** | 30 perfiles `(región, cultivo)` | Agrega clima (media/std) y producción sin `fillna(0)`; KMeans, jerárquico y DBSCAN |
| Complementario | 2.160 filas mensuales | Solo variables climáticas; métricas pueden inflarse por repetición temporal |

**Outputs del clustering:**

| Archivo | Contenido |
|---------|-----------|
| `OUTPUTS/clustering_perfiles.csv` | Asignación de cluster por `(región, cultivo)` |
| `OUTPUTS/clustering_metricas.csv` | Comparativa Silhouette / Davies-Bouldin / % ruido |
| `OUTPUTS/figures/` | Dendrograma, heatmap y comparativa (PNG) |

**Nota:** no aplicar remoción de outliers (IQR/Z-score) ni imputar NaN de producción con cero.

---

## Relación con el pipeline modular

```
01_midagri_pipeline.ipynb  →  midagri_largo.csv
02_nasa_pipeline.ipynb     →  nasa_2020_2025.csv
build_dataset_integrado.ipynb / pipeline_integrado.py
    →  dataset_integrado.csv  (+ auxiliares)
04_eda_regional.ipynb      →  visualizaciones (Análisis A)
05_eda_por_cultivo.ipynb   →  visualizaciones (Análisis B)
Clustering_Cultivos.ipynb  →  clustering sobre dataset_integrado
```

Los notebooks `01–05` en `SCRIPTS/` se conservan como referencia modular. `03_merge_y_filtrado.ipynb` queda obsoleto para generación de datos; usar `build_dataset_integrado.ipynb` o `pipeline_integrado.py`.

---

## Insumos requeridos

| Archivo | Origen |
|---------|--------|
| `OUTPUTS/midagri_largo.csv` | NB01 |
| `OUTPUTS/nasa_2020_2025.csv` | NB02 |
| `BDS/mapping_cultivo_distrito.csv` | Tabla de mapeo (región, cultivo) → distrito/piso |

Si falta el Excel MIDAGRI local, basta con tener los CSV intermedios en `OUTPUTS/`.
