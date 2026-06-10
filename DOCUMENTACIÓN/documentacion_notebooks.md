# Documentación del Pipeline de Análisis Agroclimático
## Proyecto: Relación Clima-Producción Agrícola en el Perú (2020–2025)
**Universidad del Pacífico — Data Mining 2026-I**

---

## Visión general del pipeline

El proyecto está compuesto por notebooks modulares en `SCRIPTS/` (01–05) más un **notebook de integración** en la raíz que genera el dataset maestro para ML/clustering.

```
Notebook 1 (MIDAGRI)
    ↓ midagri_largo.csv
Notebook 2 (NASA POWER)
    ↓ nasa_2020_2025.csv
build_dataset_integrado.ipynb  (o SCRIPTS/pipeline_integrado.py)
    ↓ dataset_integrado.csv      ← maestro Pareto-80 (2.160 filas)
    ↓ dataset_regional.csv
    ↓ dataset_por_cultivo.csv
    ↓ dataset_por_cultivo_filtrado.csv  (copia legacy del integrado)
Notebook 4 (EDA Regional)     Notebook 5 (EDA por Cultivo)
Clustering_Cultivos.ipynb     → lee dataset_integrado.csv
```

> Detalle técnico del maestro: ver [`dataset_integrado.md`](dataset_integrado.md).

---

## Notebook 1 — Pipeline MIDAGRI (2020–2025)

### Finalidad
Procesar los archivos mensuales de producción agrícola de MIDAGRI (formato `c-18`) y construir un dataset limpio y confiable en formato largo.

### Problema que resuelve
Los archivos Excel de MIDAGRI tienen estructuras inconsistentes: nombres de cultivos con errores tipográficos o saltos de línea, meses faltantes en ciertos años, datos acumulados (no mensuales directos), y revisiones retroactivas que generan valores negativos. Este notebook maneja todos esos casos de forma documentada y reproducible.

### Qué hace paso a paso

| Paso | Descripción |
|------|-------------|
| Configuración | Define rutas, regiones objetivo, mapeo de meses y mapeo canónico de nombres de cultivos |
| Descubrimiento de archivos | Recorre las carpetas de cada año y reporta qué meses están disponibles y cuáles faltan |
| Carga y normalización | Detecta dinámicamente el header de cada Excel, normaliza nombres de regiones y cultivos, aplica el mapeo canónico y filtra a las 6 regiones objetivo |
| Recuperación de Dic-2020 | Extrae el dato de diciembre 2020 desde el archivo de diciembre 2021 (que incluye el total anual comparativo de 2020) |
| Construcción del grid completo | Crea una grilla completa (región × año × mes) e inserta NaN explícitos para los meses faltantes, evitando que el cálculo posterior infle datos |
| Cálculo de producción mensual | Aplica diferencias consecutivas (`diff`) para convertir acumulados en producción mensual real; conserva enero tal cual; convierte negativos a NaN |
| Conversión a formato largo | Pasa de una fila por (región, año, mes) con N columnas de cultivos, a una fila por (región, cultivo, año, mes) |
| Diagnóstico de variantes | Carga los archivos sin aplicar el mapeo canónico para mostrar los nombres originales del Excel y cómo se transforman |
| Exportación | Guarda dos archivos: producción mensual y producción acumulada |

### Decisiones metodológicas clave
- Meses faltantes (Mayo-2021, Marzo-2022) → NaN explícito, nunca se inventa data
- Valores negativos por revisiones retroactivas de MIDAGRI → NaN
- Solo se conservan las 6 regiones objetivo: Piura, La Libertad, Ica, San Martín, Junín, Puno
- El filtrado Pareto-80 ocurre en el Notebook 3, no aquí (todos los cultivos pasan)

### Output al finalizar
- **`midagri_largo.csv`** — Dataset principal de producción mensual real en formato largo
- **`midagri_acumulado_largo.csv`** — Dataset con los valores acumulados originales (antes del diff)

---

## Notebook 2 — Pipeline NASA POWER (2020–2025)

### Finalidad
Descargar datos climáticos mensuales para los 14 distritos representativos seleccionados y construir un dataset climático limpio en formato largo.

### Problema que resuelve
La producción agrícola no tiene una variable climática "regional" directa: cada cultivo crece en un piso ecológico específico con su propio clima. Este notebook descarga el clima histórico mensual para 14 distritos cuidadosamente elegidos, uno por cada piso ecológico relevante del proyecto.

### Qué hace paso a paso

| Paso | Descripción |
|------|-------------|
| Configuración | Define los 14 distritos con sus coordenadas (lat/lon), región asociada y piso ecológico |
| Descarga desde API | Llama a la API de NASA POWER para cada distrito, solicitando 10 variables climáticas mensuales para el período 2020-2025 |
| Limpieza | Elimina el resumen anual que NASA agrega automáticamente (mes=13), reemplaza el centinela `-999` por NaN, y parsea las fechas en formato YYYYMM |
| Consolidación | Une todos los distritos en un único DataFrame largo |
| Validación | Verifica cobertura temporal completa (14 distritos × 72 meses = 1,008 filas esperadas) y reporta NaN por variable |
| Exportación | Guarda el dataset climático |

### Variables climáticas descargadas
Códigos NASA en `nasa_2020_2025.csv`: `t2m`, `t2m_max`, `t2m_min`, `prectotcorr`, `rh2m`, `allsky_sfc_sw_dwn`, `ws2m`, `ps`, `gwetroot`, `ts`, `t2mdew`, `qv2m`. En los datasets finales se exportan como `temp_promedio`, `temp_maxima`, `precipitacion`, `humedad_relativa`, etc. (ver `dataset_integrado.md`).

### Output al finalizar
- **`nasa_2020_2025.csv`** — Dataset climático mensual para los 14 distritos representativos

---

## Notebook de integración — `build_dataset_integrado.ipynb`

### Finalidad
Generar `dataset_integrado.csv` y los datasets auxiliares con la lógica corregida de merge y Pareto-80, sin duplicar el EDA de los notebooks 04–05.

### Correcciones vs Notebook 3 original
- Pareto-80: cultivos hasta alcanzar **≥ 80%** de producción regional (30 combinaciones vs 24 antes)
- Agregado regional: `sum(min_count=1)` para no convertir meses sin dato en cero

### Output al finalizar
- **`dataset_integrado.csv`** — Tabla maestra para clustering/ML
- **`dataset_regional.csv`**, **`dataset_por_cultivo.csv`**, **`dataset_por_cultivo_filtrado.csv`**

Equivalente por línea de comandos: `python SCRIPTS/pipeline_integrado.py`

---

## Notebook 3 — Merge Agroclimático y Filtrado *(legacy)*

### Finalidad
Combinar el dataset agrícola (Notebook 1) con el dataset climático (Notebook 2) y producir los datasets finales listos para el análisis exploratorio.

> **Nota:** para regenerar datos usar `build_dataset_integrado.ipynb` o `pipeline_integrado.py`. Este notebook se conserva como referencia histórica.

### Problema que resuelve
Cada cultivo de cada región necesita ser asociado al clima del distrito que mejor representa su piso ecológico (no un promedio regional genérico). Este notebook aplica ese mapeo y genera dos versiones del dataset: una por piso ecológico (análisis agregado) y otra por cultivo individual.

### Qué hace paso a paso

| Paso | Descripción |
|------|-------------|
| Carga de insumos | Lee los tres archivos: producción MIDAGRI, clima NASA, y tabla de mapeo `(región, cultivo) → distrito` |
| Análisis B — por cultivo | Join de MIDAGRI con el mapeo para asignar un distrito a cada (región, cultivo); luego join con NASA usando (distrito, año, mes) |
| Análisis A — por piso | Agrega la producción de todos los cultivos del mismo piso y asigna el clima de ese piso |
| Filtrado Pareto-80 | Para cada región, conserva los cultivos que acumulan el 80% de la producción total (elimina cultivos marginales) |
| Validaciones | Verifica coherencia entre datasets A y B, cobertura temporal completa, y ausencia de NaN en variables climáticas |
| Exportación | Guarda los tres datasets de salida |

### Decisiones metodológicas clave
- Cultivos sin asignación ecológica se descartan (por ejemplo, cacao en Ica)
- El clima se asigna por piso ecológico, no como promedio regional (decisión metodológica "Camino D")
- El filtrado Pareto-80 es por región, no global

### Output al finalizar
- **`dataset_regional.csv`** — Una fila por (región, piso, año, mes) con producción agregada del piso y su clima
- **`dataset_por_cultivo.csv`** — Una fila por (región, cultivo, año, mes) con producción específica y clima del distrito asignado
- **`dataset_por_cultivo_filtrado.csv`** — Igual que el anterior pero solo con los cultivos del Pareto-80

---

## Notebook 4 — EDA Análisis A (Regional por Piso Ecológico)

### Finalidad
Explorar el dataset agregado por piso ecológico para entender volúmenes, estacionalidad, perfiles climáticos y una primera mirada a correlaciones clima-producción a nivel regional.

### Problema que resuelve
Antes de modelar, necesitamos entender la estructura del dataset: qué unidades producen más, cuándo producen, cómo varía el clima entre pisos, y si hay eventos históricos (como la sequía de 2022-2023) que el dataset captura correctamente.

### Qué hace paso a paso

| Sección | Descripción |
|---------|-------------|
| Volumen total por unidad | Ranking de las 14 unidades por producción acumulada 2020-2025 (en millones de toneladas) |
| Series temporales | Evolución mensual de producción por región, separada por piso ecológico |
| Heatmaps de estacionalidad | Mapa de calor mes × año para ver las ventanas de cosecha de cada unidad |
| Patrón estacional promedio | Producción promedio por mes (firmando el calendario agrícola de cada piso) |
| El Niño 2023-2024 | Comparación producción + temperatura + precipitación durante el evento climático extremo |
| Perfil climático | Promedios de variables climáticas por piso ecológico; boxplots de temperatura y precipitación |
| Validación sequía Puno | Gráfico de producción vs humedad del suelo en Puno para confirmar que el dataset capturó el evento de 2022-2023 |
| Correlaciones clima-producción | Heatmap de correlaciones de Pearson entre producción mensual y cada variable climática, por unidad regional |

### Output al finalizar
No genera archivos nuevos. Produce visualizaciones para interpretar el comportamiento agroclimático a nivel de piso ecológico y establece hipótesis para el modelado posterior.

**Hallazgos principales documentados:**
- La Libertad costa concentra los mayores volúmenes del dataset
- Estacionalidad clara y diferenciada por piso ecológico
- La sequía 2022-2023 se captura correctamente en Puno (caída de producción correlacionada con baja humedad del suelo)
- Correlaciones clima-producción heterogéneas entre unidades

---

## Notebook 5 — EDA Análisis B (Por Cultivo)

### Finalidad
Explorar el dataset desagregado por cultivo para entender qué cultivos dominan cada región, cuándo se cosechan, cuáles son más sensibles al clima, y cómo respondieron los cultivos andinos a la sequía de 2022.

### Problema que resuelve
El análisis regional agrega todos los cultivos, lo que puede ocultar comportamientos diferenciados. Este notebook desagrega por cultivo para identificar sensibilidades climáticas específicas y patrones que no son visibles a nivel de piso.

### Qué hace paso a paso

| Sección | Descripción |
|---------|-------------|
| Panorama general | Dimensiones del dataset, cultivos únicos, combinaciones (región, cultivo) con producción real |
| Top 10 por región | Ranking horizontal de los cultivos más producidos en cada región (2020-2025) |
| Curva de concentración | Curva acumulativa por región para mostrar cuántos cultivos acumulan el 80% de la producción |
| Calendarios agrícolas | Heatmap mes × cultivo (normalizado) por región: cuándo se cosecha cada cultivo |
| Sensibilidad climática | Correlaciones de Pearson entre producción y variables climáticas, para cada par (región, cultivo) del Pareto-80 |
| Top correlaciones | Lista de los 20 pares (cultivo, variable climática) con mayor correlación absoluta |
| Caso Puno-sequía 2022 | Producción anual relativa a 2020 para cultivos de puna alta: cuáles cayeron más durante la sequía |
| Validación cruzada | Comparación del impacto de la sequía entre Puno (altiplano sur) y La Libertad sierra (norte): confirma que fue un fenómeno regional específico |

### Output al finalizar
No genera archivos nuevos. Produce visualizaciones para interpretar el comportamiento agroclimático a nivel de cultivo individual.

**Hallazgos principales documentados:**
- Alta concentración productiva: 2-3 cultivos acumulan el 80% en regiones como La Libertad y Piura
- Estacionalidad bien definida por cultivo (espárrago, uva, café, quinua, etc.)
- Cultivos andinos tradicionales mucho más vulnerables a la sequía que los forrajeros: quinua −64%, oca −62%, olluco −55%, papa −47% vs avena forrajera −29%
- La sequía 2022-2023 fue un fenómeno específico del altiplano sur, no andino general

---

## Notebook de clustering — `Clustering/Clustering_Cultivos.ipynb`

### Finalidad
Agrupar las 30 combinaciones Pareto-80 `(región, cultivo)` según perfil agroclimático y productivo, con análisis mensual complementario.

### Enfoque principal (perfiles)
- Agrega `dataset_integrado.csv` a una fila por `(región, cultivo)` con medias/std de clima y métricas de producción **sin imputar NaN con cero**
- KMeans, clustering jerárquico (dendrograma) y DBSCAN
- Tabla interpretativa y heatmap de centroides

### Análisis complementario (mensual)
- Solo variables climáticas sobre 2.160 filas
- KMeans, DBSCAN, PCA+NMF — documentado como limitado por repetición temporal (72 meses por cultivo)

### Outputs
- `clustering_perfiles.csv`, `clustering_metricas.csv`, figuras en `OUTPUTS/figures/`

---

## Resumen de archivos generados

| Archivo | Generado en | Descripción |
|---------|-------------|-------------|
| `midagri_largo.csv` | Notebook 1 | Producción mensual real por (región, cultivo, año, mes) |
| `midagri_acumulado_largo.csv` | Notebook 1 | Producción acumulada original (antes del diff) |
| `nasa_2020_2025.csv` | Notebook 2 | Variables climáticas mensuales para los 14 distritos |
| `dataset_integrado.csv` | `build_dataset_integrado.ipynb` | **Maestro** Pareto-80 para clustering/ML (2.160 filas) |
| `dataset_regional.csv` | Integración | Dataset A: producción + clima por piso ecológico |
| `dataset_por_cultivo.csv` | Integración | Dataset B: producción + clima por cultivo individual |
| `dataset_por_cultivo_filtrado.csv` | Integración | Copia legacy de `dataset_integrado.csv` |
| `clustering_perfiles.csv` | `Clustering_Cultivos.ipynb` | Clusters por (región, cultivo) |
| `clustering_metricas.csv` | `Clustering_Cultivos.ipynb` | Comparativa de métodos de clustering |
