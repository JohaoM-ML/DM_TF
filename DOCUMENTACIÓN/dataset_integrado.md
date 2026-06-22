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
make preprocess
# o: python SCRIPTS/run_notebook.py SCRIPTS/notebooks/00_pipeline_integrado.ipynb
```

El notebook ejecuta en orden interno `build_midagri_largo` → `build_mapping` →
`download_nasa_power` → `build_dataset_integrado`. Los notebooks originales 00-03
(detalle celda a celda, versión previa) quedaron archivados en `BORRADORES/`.

---

## Archivos de salida

| Archivo | Filas | Descripción |
|---------|------:|-------------|
| `dataset_integrado.csv` | 2.376 | **Maestro de productos significativos** |
| `dataset_por_cultivo.csv` | 15.120 | Todos los cultivos con mapping |
| `dataset_regional.csv` | 1.008 | Agregado por piso |
| `dataset_por_cultivo_filtrado.csv` | 2.376 | Copia de `dataset_integrado` (compatibilidad) |

**Dimensiones del maestro:** 33 combinaciones × 72 meses = 2.376 filas × 20 columnas.

### Productos significativos por región (mapping v2)

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
| 12 vars clima | float | Ver `RENAME_CLIMA` en `00_pipeline_integrado.ipynb` |

**Unidades climáticas:** `radiacion_solar` MJ/m²/día; `humedad_especifica` kg/kg; `precipitacion` mm/día.

---

## Calidad de datos

| Métrica | Valor |
|---------|------------|
| NaN en `produccion_ton` | 166 (por diseño) |
| NaN en clima | 0 |
| Combos significativos | 33 |
| Distritos únicos | 28 (de 34 en el inventario NASA; 14 originales + 20 refinados con SISAGRI) |

---

## Limitaciones

- Clima idéntico para cultivos que comparten el mismo distrito proxy (persiste para los combos sin
  evidencia SISAGRI: La Libertad-caña, San Martín-palma — ver `EXPERIMENTOS/sisagri_v3/`).
- Producción en volumen (t), no rendimiento t/ha.
- Ver `OUTPUTS/robustez/` para sensibilidad del umbral de productos significativos y estabilidad de clusters.
