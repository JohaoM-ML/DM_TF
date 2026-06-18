# Guion de defensa — respuestas a preguntas críticas

## 1. Si cada cultivo del mismo piso comparte clima, ¿qué descubre el clustering?

**Respuesta:** El clima discrimina entre ~12 entornos distintos (distritos/pisos), no entre cultivos del mismo piso. El clustering segmenta **perfiles productivos** (volumen, variabilidad de cosecha) dentro de esos entornos. No es un descubrimiento de sensibilidad climática por cultivo.

**Evidencia:** Abrir `OUTPUTS/dataset_integrado.csv` — Ica espárrago e Ica uva en enero 2020 tienen `temp_promedio` idéntica (21,96).

---

## 2. K cambió de 7 (v1) a 6 (v2) solo cambiando el mapeo. ¿Cómo es un hallazgo?

**Respuesta:** No es invariante al mapeo. Reportamos sensibilidad: ARI entre etiquetas v1 y v2 en perfiles comunes (`OUTPUTS/robustez/ari_v1_v2.csv`, ARI ≈ 0,87). El clustering es **exploratorio**, no un descubrimiento estable.

---

## 3. ¿Puedes regenerar todo ahora?

**Respuesta:** Sí — demo en vivo:

```bash
pip install -r requirements.txt
python SCRIPTS/pipeline_integrado.py
make cluster
```

---

## 4. Producción en toneladas — ¿clima o hectáreas?

**Respuesta:** Volumen total regional, no rendimiento. MIDAGRI C-18 no provee área sembrada en este pipeline. Sin t/ha no podemos aislar respuesta climática. Es limitación explícita del diseño.

---

## 5. Silhouette 0,53 vs DBSCAN 0,89 — ¿cuál es el resultado?

**Respuesta:** KMeans sobre 33 perfiles: Silhouette ≈ 0,51 (estructura moderada). DBSCAN descarta ~63% como ruido — la métrica alta es sobre el subconjunto restante y **no es método válido** aquí. Reportamos `% ruido` en `clustering_metricas.csv`.

---

## 6. ¿Por qué Pareto 80%?

**Respuesta:** Convención de concentración productiva. Sensibilidad documentada en `OUTPUTS/robustez/pareto_sensibilidad.csv`: 70% → 24 combos; 80% → 33; 90% → 49.

---

## Slide obligatorio: Lo que este trabajo NO demuestra

- Causalidad clima → producción  
- Dirección del efecto  
- Predicción operativa  
- Rendimiento agrícola (t/ha)  
- Granularidad finca/parcela  
