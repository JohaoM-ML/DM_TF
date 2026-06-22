"""Grafico de soporte: tasa de deteccion de anomalias (Isolation Forest) por evento conocido,
vs. la tasa base del dataset completo. Sigue las convenciones de SCRIPTS/viz_style.py.

No modifica el informe ni el pipeline; guarda su salida en EXPERIMENTOS/anomalias_v1/OUTPUTS/.
"""
from pathlib import Path
import sys

import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "SCRIPTS"))
from viz_style import PLOTLY_TEMPLATE  # noqa: E402

OUT = Path(__file__).resolve().parent / "OUTPUTS"
df = pd.read_csv(OUT / "anomalias_detectadas.csv", encoding="utf-8")

tasa_base = df["anomalia"].mean()
puno = df[df["evento_conocido"] == "sequia_puno_2022"]["anomalia"].mean()
nino = df[df["evento_conocido"] == "nino_costero_2023_2024"]["anomalia"].mean()

marzo_2025 = (
    ((df["region"] == "Junin") | ((df["region"] == "Ica") & (df["piso_ecologico"] == "costa")))
    & (df["anio"] == 2025) & (df["numero_mes"].isin([2, 3, 4, 5]))
)
lluvias_2025 = df[marzo_2025]["anomalia"].mean()

categorias = [
    "Resto del dataset<br>(línea base)",
    "Sequía Puno<br>2022",
    "El Niño costero<br>2023–2024",
    "Lluvias Junín/Ica<br>feb–may 2025",
]
valores = [tasa_base, puno, nino, lluvias_2025]
colores = ["#B0B0B0", "#9D5B8B", "#E45756", "#4C78A8"]

fig = go.Figure(go.Bar(
    x=valores,
    y=categorias,
    orientation="h",
    marker_color=colores,
    text=[f"{v:.1%}" for v in valores],
    textposition="outside",
))
fig.update_layout(
    title=dict(text="<b>Tasa de detección de anomalías por evento</b>", x=0.5, xanchor="center"),
    xaxis_title="% de filas marcadas como anomalía (Isolation Forest)",
    xaxis=dict(tickformat=".0%", range=[0, max(valores) * 1.18]),
    template=PLOTLY_TEMPLATE,
    width=750, height=380,
    margin=dict(l=160, r=40),
)
fig.write_image(str(OUT / "tasa_deteccion_eventos.png"), scale=2)
print("Guardado:", OUT / "tasa_deteccion_eventos.png")
print(f"Base: {tasa_base:.1%} | Puno 2022: {puno:.1%} | Nino 2023-24: {nino:.1%} | Lluvias 2025: {lluvias_2025:.1%}")
