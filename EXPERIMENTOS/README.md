# Experimentos

Carpeta para análisis comparativos aislados del pipeline principal.

## `ablation_v1/`

Comparación histórica del merge con **mapping v1 legacy** contra el canónico v2. El script que la generó
(`run_ablation.py`) dependía de módulos `SCRIPTS/*.py` retirados al consolidar el pipeline en notebooks y
ya no funciona; se eliminó. Las salidas (`OUTPUTS/v1/`) quedan como evidencia histórica.

Conclusión: [`DOCUMENTACIÓN/reporte_mapping_v1_vs_v2.md`](../DOCUMENTACIÓN/reporte_mapping_v1_vs_v2.md)

## `asociacion_v1/`

Explora si vale la pena agregar reglas de asociación (clima → caída de producción) al trabajo
final. Apriori implementado a mano, sin dependencias nuevas. Veredicto: señal real pero débil
(lift ≤1.4) — no se incorporó al informe. Detalle: [`asociacion_v1/RESUMEN.md`](asociacion_v1/RESUMEN.md)

## `anomalias_v1/`

Explora si Isolation Forest detecta por sí solo la sequía Puno 2022 y El Niño 2023–2024.
Veredicto: detección limpia del pico de El Niño en Piura (abr-2023), moderada para la sequía
de Puno; más prometedor que las reglas de asociación pero no incorporado todavía. Detalle:
[`anomalias_v1/RESUMEN.md`](anomalias_v1/RESUMEN.md)
