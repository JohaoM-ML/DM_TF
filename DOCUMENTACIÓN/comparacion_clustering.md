# Comparación de los cuadernos de clustering

Comparación de los tres enfoques de clustering agroclimático del proyecto DM_TF
(datos 2020–2025, `OUTPUTS/dataset_integrado.csv`). Las métricas se calcularon sobre
los mismos datos para que sean reproducibles.

| Cuaderno | Enfoque | Unidad de análisis |
|---|---|---|
| `06_clustering_cultivos.ipynb` | Original | 33 perfiles `(región, cultivo)` |
| `06a_zonas_agroclimaticas.ipynb` | Tipologías agroclimáticas | 12 zonas `(distrito)` |
| `06b_perfiles_productivos.ipynb` | Patrones de producción | 33 perfiles `(región, cultivo)` |

## Tabla comparativa

| Criterio | **06 (original)** | **06a (zonas)** | **06b (perfiles productivos)** |
|---|---|---|---|
| Unidad de análisis | 33 perfiles `(región, cultivo)` | 12 zonas `(distrito)` | 33 perfiles `(región, cultivo)` |
| Qué entra al clustering | 10 clima + 3 producción | 10 clima | 12 estacionalidad + 4 escala + 2 clima-PCA |
| K elegido | 6 | 5 | 6 |
| **Silhouette** | **0.514** | 0.415 | 0.297 |
| **Davies–Bouldin** | 0.604 | 0.674 | 0.896 |
| ARI(cluster, región) | **0.588** | ≈1 (es la zona) | **0.062** |
| ¿Qué separa los grupos? | Geografía / clima | Clima | **Patrón de producción** |
| Producción | input (pero casi irrelevante) | descriptiva *a posteriori* | input dominante |
| Interpretación | ambigua | limpia | rica pero exigente |
| Outlier caña Virú | cluster propio (C3, n=1) | dentro de costa | absorbido por `log1p` |

## La prueba clave

ARI (Adjusted Rand Index) entre las particiones, sobre los mismos 33 cultivos:

- **ARI(06 vs 06b) = 0.184** → 06 y 06b agrupan los cultivos de forma casi no
  relacionada. **No son dos versiones de lo mismo**: responden preguntas distintas.
- **06 → ARI 0.588 con la región** → *clusteriza geografía*. La etiqueta "clustering de
  cultivos" es engañosa; el cultivo apenas mueve la asignación.
- **06b → ARI 0.062 con la región** → ha roto el vínculo con la geografía. Cultivos de
  Ica, La Libertad, Piura y San Martín caen juntos porque comparten *calendario
  productivo*, no clima. Aquí el cultivo sí manda.
- **06a** reconoce que solo hay 12 unidades climáticas reales y las clusteriza sin
  duplicar perfiles.

## Cómo leer las métricas (importante)

El Silhouette más alto de 06 **no significa que sea mejor**. Es alto porque:

1. Mide separación en un espacio donde 10 de 13 features solo toman 11 valores distintos
   (los distritos), generando grupos artificialmente "limpios".
2. Premiar ese Silhouette es premiar la redundancia geográfica.

06b tiene Silhouette más bajo (0.30) porque resuelve un problema genuinamente más difícil
y honesto. **El Silhouette solo es comparable dentro del mismo espacio de features**, no
entre los tres cuadernos.

## Resultados por cuaderno

### 06a — Tipologías agroclimáticas (K=5, Silhouette 0.415)

| Cluster | Zonas | Clima | Cultivos dominantes |
|---|---|---|---|
| C0 | El Tambo, Huamachuco | Sierra templada, 10.4 °C | papa, alfalfa, avena, maíz choclo |
| C1 | Moyobamba, Perené, Río Tambo, Tocache | Selva húmeda, 22.7 °C | arroz, plátano, palma, piña, naranja |
| C2 | Chincha Alta, Virú | Costa árida, 0.27 precip | caña, uva, palta, arroz, mandarina |
| C3 | Sullana, Tambogrande | Costa norte / bosque seco, 25.6 °C | caña, arroz, plátano, mango, uva |
| C4 | Ayaviri, Ilave | Altiplano frío, 8.3 °C | avena forrajera, alfalfa, papa |

La producción se describe *a posteriori* (boxplots + top cultivos por zona).

### 06b — Perfiles productivos (K=6, Silhouette 0.297)

| Cluster | n | Patrón | Ejemplos |
|---|---|---|---|
| C0 | 4 | Pico en diciembre | tomate Ica, uva Ica/Piura, mango Piura |
| C1 | 10 | Pico en mayo, ~11 meses | maíz Ica, café Junín, arroz La Libertad/Piura |
| C2 | 1 | Pico agosto concentrado | papa Ica |
| C3 | 2 | Cosecha concentrada abril, 7 meses | avena y papa de Puno |
| C4 | 14 | **Permanente / plano** (concentración 0.13) | espárrago Ica, caña La Libertad **y** Piura, palma, plátano |
| C5 | 2 | Pico abril | maíz choclo Junín, alfalfa Puno |

El cluster lo determina el calendario productivo; `log1p` neutraliza el outlier de la caña
de Virú (28 M t).

## Síntesis y recomendación

| Si el objetivo es… | Usar | Por qué |
|---|---|---|
| Tipificar el **territorio** (qué clima hay y qué se cultiva en él) | **06a** | Interpretación incuestionable, sin perfiles duplicados |
| Tipificar **patrones productivos de cultivos** | **06b** | Único donde el cultivo determina el grupo |
| — | ~~06~~ | Mezcla ambos objetivos sin lograr ninguno limpiamente; conservar solo como referencia |

En una frase: **06 promete clusterizar cultivos pero clusteriza regiones; 06a clusteriza
regiones y lo admite; 06b sí clusteriza cultivos.** 06a y 06b son los dos resultados
defendibles, cada uno respondiendo una pregunta distinta y complementaria.

---

### Reproducibilidad

Métricas calculadas con `KMeans(n_init=10, random_state=42)`, `StandardScaler`, y
`silhouette_score` / `davies_bouldin_score` de scikit-learn sobre
`OUTPUTS/dataset_integrado.csv`. El ARI usa `adjusted_rand_score`.
