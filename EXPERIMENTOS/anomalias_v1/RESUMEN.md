# Resumen — ¿vale la pena un módulo de detección de anomalías?

## Metodología

- Insumo: `OUTPUTS/dataset_regional.csv` (2,291 filas usables, 34 unidades región×piso×distrito, sin tocar el dataset original).
- Cada variable (clima + `produccion_piso_ton`) normalizada por z-score **dentro de su propia
  unidad** (para que "anómalo" signifique "atípico para ese lugar", no solo "es Puno").
- `IsolationForest` (sklearn, ya dependencia del proyecto), `contamination=5%`.
- Validación: ¿el modelo flaggea más seguido los meses que el informe ya identifica como
  eventos extremos (sequía Puno 2022, El Niño Ica/La Libertad/Piura/San Martín 2023–2024)
  que el resto del dataset?

## Resultado

| | Tasa base (todo el dataset) | Tasa dentro de las anomalías detectadas |
|---|---:|---:|
| Evento conocido (sequía o Niño) | 22.6% | **38.3%** |

Hay lift real: los eventos conocidos están sobrerrepresentados entre las anomalías detectadas.
Desglosado:

- **El Niño Piura, abril 2023**: detección muy limpia — 7 de los 14 distritos de Piura
  aparecen entre las **top 7** anomalías de todo el dataset (2,291 filas). Esto valida con un
  método no supervisado independiente la afirmación del informe de que Piura tuvo la mayor
  anomalía de precipitación.
- **Sequía Puno 2022**: 12.5% de detección (5 de 40 filas) — señal moderada, por encima del 5%
  base pero no tan limpia como Piura.
- **El Niño 2023–2024 en conjunto** (las 4 regiones, 24 meses): 8.2% de detección — el efecto
  está concentrado en el pico de abril 2023 en Piura, no distribuido parejo en los 2 años.

**Hallazgo no buscado:** varias filas de **2025** (Junín selva/sierra, Ica/La Libertad costa,
meses de marzo, junio, julio) aparecen entre las anomalías más fuertes, sin corresponder a
ningún evento documentado en el informe. Verifiqué que no es un artefacto de datos
incompletos (los 12 meses de 2025 tienen valores reales, no placeholders) — podría ser una
señal climática real de 2025 todavía no investigada, o un efecto de que NASA POWER usa datos
provisionales (no la reanálisis final) para los meses más recientes. **No se investigó más a
fondo** porque excede el alcance de este experimento rápido.

## Veredicto

**Más prometedor que las reglas de asociación.** La detección de El Niño en Piura es limpia y
fuerte; la de la sequía de Puno es moderada. A diferencia de las reglas de asociación (lift
débil ~1.4 en general), aquí el modelo SÍ aísla con precisión el evento más fuerte del dataset
sin que se le diga dónde buscar.

**Recomendación:** vale la pena considerarlo, pero como **complemento**, no como sección nueva
grande: podría usarse para reforzar la Sección "Eventos climáticos extremos" del informe con
una frase del tipo *"un detector de anomalías no supervisado (Isolation Forest) confirma
independientemente que abril 2023 en Piura es la anomalía más fuerte del dataset (de 2,291
filas), validando el hallazgo cualitativo"*. El hallazgo de 2025 es interesante pero **no se
debe incluir** sin investigarlo más — mencionarlo sin explicación generaría más preguntas que
respuestas en la sustentación.
