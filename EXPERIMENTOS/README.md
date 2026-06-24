# Experimentos

Carpeta para análisis comparativos aislados del pipeline principal.

## `sisagri_v3/`

Compara la asignación distrito-cultivo del mapping v2 contra evidencia medida SISAGRI.
Es la base del refinamiento SISAGRI ya incorporado al pipeline (`00_pipeline_integrado.ipynb`,
documentado en `DOCUMENTACIÓN/dataset_integrado.md`).

## `anomalias_v1/`

Explora si Isolation Forest detecta por sí solo la sequía Puno 2022 y El Niño 2023–2024.
Veredicto: detección limpia del pico de El Niño en Piura (abr-2023), moderada para la sequía
de Puno. Las mismas variables se reutilizan en `04_eda.ipynb` (Sección 2.3) para reproducir
las cifras citadas en el informe. Detalle: [`anomalias_v1/RESUMEN.md`](anomalias_v1/RESUMEN.md)

## `clasificacion_v1/`

Valida los clusters ya definidos (06a zona, 06b perfil) como problema de clasificación
supervisada (Random Forest + KNN, Leave-One-Out, probabilidad/margen por registro), un
chequeo de robustez independiente de la relación clima-producción. Veredicto: Modelo A muy
bien separado (96.4% accuracy, idéntico en dos clasificadores) y valida cuantitativamente el
caso ya conocido de Jilili-Piura (margen 0.04); Modelo B débil, no aporta nada nuevo. Paso 2
(escenario de calentamiento hipotético +1°C/+2°C, solo Modelo A): Random Forest no cambia
ningún distrito; KNN cambia 2, pero solo 1 (Huamachuco) es un hallazgo genuino y físicamente
plausible. Ya incorporado como `SCRIPTS/notebooks/08_modelo_clasificador.ipynb` (validación +
demo de clasificación de un distrito nuevo). Detalle:
[`clasificacion_v1/RESUMEN.md`](clasificacion_v1/RESUMEN.md)

## Experimentos descartados (eliminados)

`ablation_v1` (comparación mapping v1 legacy vs v2 — conclusión archivada en
`DOCUMENTACIÓN/reporte_mapping_v1_vs_v2.md`), `asociacion_v1` (reglas de asociación,
señal débil) y `sensibilidad_v1` (regresión/RF de sensibilidad climática por cluster,
métodos se contradecían) se exploraron y descartaron — sin incorporarse al informe ni
tener referencias vigentes en el pipeline, se borraron para no confundir con lo que sí
se usa.
