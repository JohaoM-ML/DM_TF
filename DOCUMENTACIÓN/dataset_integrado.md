# Dataset integrado — documentación técnica

**Proyecto:** Tipología agroclimática y producción agrícola en el Perú (2020–2025)  
**Universidad del Pacífico — Data Mining 2026-I**  
**Mapping canónico:** v2 (`mapping_cultivo_distrito_v2_pipeline.csv`)

---

## Propósito

`dataset_integrado.csv` es la **tabla maestra** para clustering y EDA. Una fila por `(región, cultivo, año, mes)` con producción mensual y 12 variables climáticas del distrito asignado.

---

## Cómo generarlo

```bash
jupyter execute SCRIPTS/notebooks/03_build_dataset_integrado.ipynb
# o ejecutar el notebook 03 en Jupyter tras 01, 00 y 02
```

Opciones CLI: `--mapping`, `--output-dir`, `--pareto-threshold`.

---

## Archivos de salida

| Archivo | Filas | Descripción |
|---------|------:|-------------|
| `dataset_integrado.csv` | 2.376 | **Maestro Pareto-80** |
| `dataset_por_cultivo.csv` | 15.120 | Todos los cultivos con mapping |
| `dataset_regional.csv` | 1.008 | Agregado por piso |
| `dataset_por_cultivo_filtrado.csv` | 2.376 | Copia de `dataset_integrado` (compatibilidad) |

**Dimensiones del maestro:** 33 combinaciones × 72 meses = 2.376 filas × 20 columnas.

### Pareto-80 por región (mapping v2)

| Región | Cultivos | % acumulado |
|--------|:--------:|------------:|
| Ica | 8 | 80,7% |
| Junín | 9 | 82,2% |
| La Libertad | 4 | 81,8% |
| Piura | 5 | 82,8% |
| Puno | 3 | 89,9% |
| San Martín | 4 | 83,8% |

---

## Esquema de columnas

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `region` | str | Región MIDAGRI |
| `piso_ecologico` | str | costa / sierra / selva / etc. |
| `distrito` | str | Distrito NASA POWER asignado |
| `cultivo` | str | Cultivo normalizado |
| `anio` | int | 2020–2025 |
| `numero_mes` | int | 1–12 |
| `mes` | str | Nombre del mes |
| `produccion_ton` | float | Producción mensual (ton); NaN = mes sin dato |
| 12 vars clima | float | Ver `RENAME_CLIMA` en `pipeline_integrado.py` |

**Unidades climáticas:** `radiacion_solar` MJ/m²/día; `humedad_especifica` kg/kg; `precipitacion` mm/día.

---

## Calidad de datos

| Métrica | Valor (v2) |
|---------|------------|
| NaN en `produccion_ton` | 166 (por diseño) |
| NaN en clima | 0 |
| Combos Pareto | 33 |
| Distritos únicos | 12 |

---

## Limitaciones

- Clima idéntico para cultivos del mismo (región, piso).
- Producción en volumen (t), no rendimiento t/ha.
- Ver `OUTPUTS/robustez/` para sensibilidad Pareto y estabilidad de clusters.
