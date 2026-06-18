# Agentes de auditoría — Pipeline notebooks DM_TF

Cinco agentes especializados en **Data Mining** para analizar, criticar y proponer mejoras sobre el pipeline Jupyter (`SCRIPTS/notebooks/01–06`).

Diseñados para pulir **trazabilidad, lógica y coherencia** del preprocesamiento al clustering — sin auditar informe LaTeX ni rúbrica Blackboard.

---

## Agentes

| # | Rol | Alcance | Archivo |
|---|-----|---------|---------|
| **1** | Arquitecto de pipeline y trazabilidad | 01→06, cadena I/O, reproducibilidad | `agente_1.md` |
| **2** | Auditor de ingeniería de datos | 01–03 MIDAGRI, NASA, merge, Pareto | `agente_2.md` |
| **3** | Crítico de EDA y minería asociativa | 04–05 correlaciones, claims | `agente_3.md` |
| **4** | Especialista en clustering y evaluación | 06 KMeans, DBSCAN, PCA, métricas | `agente_4.md` |
| **5** | Integrador de coherencia y plan de pulido | Transversal + síntesis accionable | `agente_5.md` |

---

## Orden de ejecución recomendado

```
Paralelo:  Agente 1 + 2 + 3 + 4  (cada uno su dominio)
           ↓
Secuencial: Agente 5  (integra hallazgos → plan de pulido)
           ↓
Salida:    agentes/INFORME_PULIDO.md  (consolidar manualmente o con LLM)
```

### Ejecución en paralelo (Cursor / LLM)

Copiar el contenido de cada `agente_N.md` como prompt a un agente con acceso al repositorio completo. Cada agente debe **leer los notebooks reales**, no asumir documentación.

### Consolidación

Tras los 5 informes, crear `INFORME_PULIDO.md` con:
1. Top 10 bloqueantes (de todos los agentes)
2. Backlog por notebook (celda + fix)
3. Checklist pre-exposición (Agente 5)
4. Veredicto: ¿pipeline listo para mostrar?

---

## Qué auditan

- `SCRIPTS/notebooks/01_midagri_pipeline.ipynb`
- `SCRIPTS/notebooks/02_nasa_pipeline.ipynb`
- `SCRIPTS/notebooks/03_build_dataset_integrado.ipynb`
- `SCRIPTS/notebooks/04_eda_regional.ipynb`
- `SCRIPTS/notebooks/05_eda_por_cultivo.ipynb`
- `SCRIPTS/notebooks/06_clustering_cultivos.ipynb`
- `ENTREGAS/LIMITACIONES.md`
- `BDS/mapping/` (insumos)

## Qué NO auditan

- Entregables LaTeX / PPTX (fase anterior)
- Tests pytest (eliminados del flujo principal)
- Carpetas `EXPERIMENTOS/`, `legacy/` (referencia histórica)

---

## Principios compartidos

1. **Trazabilidad:** cada CSV debe generarse en un notebook anterior visible.
2. **Honestidad:** tipología exploratoria, no causalidad ni predicción.
3. **Crítica constructiva:** cada hallazgo lleva fix concreto (notebook + celda).
4. **Cifras verificables:** 33 perfiles, 2376 filas, K=6, NaN=166, Sil≈0,51.
