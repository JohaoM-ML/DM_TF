# Experimentos

Carpeta para análisis comparativos aislados del pipeline principal.

## `ablation_v1/`

Comparación histórica del merge con **mapping v1 legacy** contra el canónico v2. El script que la generó
(`run_ablation.py`) dependía de módulos `SCRIPTS/*.py` retirados al consolidar el pipeline en notebooks y
ya no funciona; se eliminó. Las salidas (`OUTPUTS/v1/`) quedan como evidencia histórica.

Conclusión: [`DOCUMENTACIÓN/reporte_mapping_v1_vs_v2.md`](../DOCUMENTACIÓN/reporte_mapping_v1_vs_v2.md)
