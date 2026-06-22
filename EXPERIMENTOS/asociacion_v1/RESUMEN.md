# Resumen — ¿vale la pena un módulo de reglas de asociación?

## Metodología

- Insumo: `OUTPUTS/dataset_por_cultivo.csv` (14,038 filas usables, sin tocar el dataset original).
- Variables climáticas discretizadas en terciles (bajo/medio/alto) **por piso ecológico**, para no
  comparar costa con sierra.
- Evento objetivo: `caida_fuerte` = producción mensual ≥25% por debajo de la mediana histórica de
  ese mismo (región, cultivo). Ocurre en el 24.3% de las filas.
- Apriori implementado a mano (sin librerías nuevas): soporte mínimo 2%, confianza mínima 30%.

## Resultado

12 reglas superan el umbral. Las más fuertes:

| Regla | Soporte | Confianza | Lift |
|---|---:|---:|---:|
| radiación baja & temp. máxima alta & temp. media alta → caída fuerte | 3.1% | 34.7% | **1.42** |
| humedad de suelo media & temp. máxima alta & temp. media alta → caída fuerte | 2.4% | 33.0% | 1.35 |
| radiación baja & temp. media alta → caída fuerte | 3.5% | 32.8% | 1.35 |

Todas las reglas top comparten un patrón: **temperatura alta** (máxima y/o media) combinada con
algún otro factor (radiación baja, humedad de suelo media, humedad relativa alta) eleva la
probabilidad de caída fuerte de ~24% (base) a ~30–35% — un **lift de 1.25 a 1.42**.

## Veredicto

**Señal real, pero débil.** El patrón "calor + algo más → caída de producción" es agronómicamente
sensato (estrés térmico), y el experimento corre rápido y sin fricción. Pero un lift máximo de 1.42
significa que el clima discretizado en bins explica poco de la varianza de las caídas de
producción — la mayoría de las caídas fuertes (genuinamente) no calzan en ninguna de estas reglas,
y la mayoría de los meses con estas condiciones climáticas NO terminan en caída fuerte.

**Recomendación:** no incorporarlo como sección nueva del informe — el aporte marginal no
justifica el espacio ni el riesgo de que parezca una pieza forzada para "cumplir cuota de tareas
DM". Si se quisiera mencionar, alcanza con una frase en *Trabajo futuro*: la asociación
clima–caída de producción se exploró informalmente y mostró una señal débil (lift ≤1.4),
sugiriendo que haría falta una definición de "evento extremo" más fina (por cultivo, no por
terciles genéricos) para que sea explotable.

Esto queda documentado aquí como evidencia de que se exploró la posibilidad, sin tocar el
informe ni los notebooks del entregable.
