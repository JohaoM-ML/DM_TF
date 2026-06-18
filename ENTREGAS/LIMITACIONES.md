# Limitaciones del entregable

## Lo que este proyecto NO demuestra

1. **Impacto causal** de variables climáticas en la producción.
2. **Dirección** del efecto (clima → producción vs producción → decisiones de área).
3. **Predicción** de cosechas o shocks climáticos.
4. **Rendimiento** (t/ha) — solo volumen en toneladas.
5. **Granularidad finca** — nivel región×cultivo×mes.

## Limitaciones de diseño

| Limitación | Implicación |
|------------|-------------|
| Clima por distrito/piso | Cultivos del mismo piso comparten serie climática |
| n ≈ 33 perfiles Pareto | Clusters con pocos puntos por grupo |
| Correlaciones Pearson | Sin desestacionalización ni corrección BH |
| Mapping con overrides | Decisiones agronómicas del analista influyen en asignación |

## Claims retirados (no usar en slides)

- "VPD" / "estrés calórico" — variable no calculada en el pipeline.
- "408 × 71 variables, cero nulos" — irreconciliable con artefactos reales.
- "Impacto de variables climáticas" — reemplazar por "caracterización / tipología".

## Fortalezas defendibles

- Pipeline reproducible MIDAGRI + NASA con disciplina de NaN.
- Reconstrucción acumulado→mensual documentada y validada (coherencia A/B).
- Mapping v2 con metadatos de confianza y ablación v1 documentada.
- Análisis de robustez en `OUTPUTS/robustez/`.
