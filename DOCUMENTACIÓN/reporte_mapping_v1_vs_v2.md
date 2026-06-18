# Reporte mapping v1 vs v2 (post-regeneración)

**Fecha de regeneración:** pipeline canónico con mapping v2 en `OUTPUTS/`.  
**Ablación v1:** `EXPERIMENTOS/ablation_v1/OUTPUTS/v1/` y `OUTPUTS/robustez/v1_run/`.

## Datasets

| Archivo | v1 legacy | v2 canónico |
|---------|----------:|------------:|
| `dataset_integrado.csv` | (2.088, 20) | (2.376, 20) |
| Combos Pareto | 29 | 33 |
| NaN `produccion_ton` | ~140 | 166 |

## Clustering perfiles

| Versión | K | Silhouette | Perfiles |
|---------|--:|-----------:|---------:|
| v1 | 7 | ~0.53 | 29 |
| v2 | 6 | ~0.51 | 33 |

## Estabilidad de etiquetas (ARI)

Perfiles comunes entre v1 y v2: **29**.  
**Adjusted Rand Index (KMeans): 0.8653** — alta concordancia en solapamiento, pero K y membresía cambian al ampliar el set Pareto.

## Sensibilidad Pareto (v2)

| Umbral | Combos | Filas |
|--------|-------:|------:|
| 70% | 24 | 1.728 |
| 80% | 33 | 2.376 |
| 90% | 49 | 3.528 |

Fuente: `OUTPUTS/robustez/pareto_sensibilidad.csv`

## Hopkins statistic

0.5437 — cercano a aleatorio (0.5); estructura de cluster moderada, no fuerte.

## Combos nuevos en Pareto v2 (ejemplos)

- Ica / papa  
- Junín / cafe_pergamino  
- Piura / platano, uva  

Ver ablación completa: `python EXPERIMENTOS/ablation_v1/run_ablation.py`
