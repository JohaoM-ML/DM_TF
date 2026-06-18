# -*- coding: utf-8 -*-
"""
Reemplaza el código de los notebooks 04 (EDA regional) y 05 (EDA por cultivo)
con versiones idénticas en lógica pero anotadas extensamente en español.

Uso:
    python tools/apply_comments_04_05.py
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Notebook 04 — EDA regional (Análisis A)
# Diez celdas de código en orden de aparición (índices 1,3,5,7,9,11,13,15,17,19)
# ---------------------------------------------------------------------------

CELLS_04 = [
    # --- Celda 1: Setup ---
    '''\
# =============================================================================
# CELDA 1 — Configuración inicial y carga de dataset_regional.csv
# =============================================================================
# Propósito:
#   Preparar el entorno del Análisis A (EDA regional): importar librerías,
#   resolver la raíz del repositorio desde distintos directorios de ejecución,
#   validar que exista el insumo generado por 03_build_dataset_integrado.ipynb
#   y construir columnas derivadas (unidad territorial, fecha, mes ordenado).
# Sección del análisis: Setup / Análisis A — EDA regional (Pareto-80 por piso).
# Salidas esperadas:
#   - Impresión en consola: dimensiones, unidades, regiones y conteo de NaN.
#   - Vista previa df.head(3) en el notebook.
#   - No genera figuras ni CSV en esta celda.
# =============================================================================

# sys queda disponible por si se necesita ajustar sys.path en entornos locales
import sys
from pathlib import Path

# Visualización y estadística para todo el notebook regional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# --- Resolución de ROOT según desde dónde se ejecute el kernel Jupyter ---
# Caso notebooks/  → subir dos niveles hasta la raíz del repo (DM_TF)
# Caso SCRIPTS/    → subir un nivel (copia duplicada del notebook en SCRIPTS/)
# Caso cwd sin OUTPUTS pero el padre sí lo tiene → asumir subdirectorio del repo
ROOT = Path(".").resolve()
if ROOT.name == "notebooks":
    ROOT = ROOT.parent.parent
elif ROOT.name == "SCRIPTS":
    ROOT = ROOT.parent
elif not (ROOT / "OUTPUTS").exists() and (ROOT.parent / "OUTPUTS").exists():
    ROOT = ROOT.parent

# Rutas de salida: CSVs en OUTPUTS/ y figuras en OUTPUTS/figures/
RUTA_OUTPUT = ROOT / "OUTPUTS"
RUTA_OUTPUT.mkdir(parents=True, exist_ok=True)
RUTA_FIGURES = RUTA_OUTPUT / "figures"
RUTA_FIGURES.mkdir(parents=True, exist_ok=True)
DATASET_REGIONAL = RUTA_OUTPUT / "dataset_regional.csv"

# El pipeline integrado debe haber corrido antes; sin este archivo no hay EDA
if not DATASET_REGIONAL.exists():
    raise FileNotFoundError(
        f"No se encontró {DATASET_REGIONAL}. Ejecutar primero 03_build_dataset_integrado.ipynb"
    )

# Carga del panel mensual agregado por unidad territorial (región|piso|distrito)
df = pd.read_csv(DATASET_REGIONAL)

# Etiqueta legible para gráficos: región | piso (distrito)
df["unidad"] = (
    df["region"] + " | " + df["piso_ecologico"] + " (" + df["distrito"] + ")"
)

# Eje temporal continuo para series mensuales (primer día de cada mes)
df["fecha"] = pd.to_datetime(
    df["anio"].astype(str) + "-" + df["numero_mes"].astype(str).str.zfill(2) + "-01"
)

# Subconjunto reducido de variables climáticas usadas en correlaciones y perfiles
CLIMA_EDA = [
    "temp_promedio", "precipitacion", "humedad_relativa",
    "radiacion_solar", "humedad_suelo",
]

# Orden cronológico de meses para heatmaps y patrones estacionales
MESES_ORDEN = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
df["mes"] = pd.Categorical(df["mes"], categories=MESES_ORDEN, ordered=True)

# Estilo uniforme para todas las figuras del notebook
sns.set_theme(style="whitegrid", context="notebook")

print(f"Filas: {len(df):,} | Unidades: {df['unidad'].nunique()} | Regiones: {df['region'].nunique()}")
print(f"NaN produccion_piso_ton: {df['produccion_piso_ton'].isna().sum()}")
df.head(3)
''',

    # --- Celda 3: §1 Volumen ---
    '''\
# =============================================================================
# CELDA 2 — §1 Volumen productivo acumulado por unidad territorial
# =============================================================================
# Propósito:
#   Cuantificar la producción total 2020–2025 por unidad Pareto-80 y su peso
#   relativo (% del total nacional del subconjunto) para priorizar territorios.
# Sección del análisis: Análisis A — §1 Concentración productiva (Pareto).
# Salidas esperadas:
#   - Consola: top 5 unidades por toneladas y porcentaje.
#   - Figura: OUTPUTS/figures/eda_regional_volumen_unidad.png
# =============================================================================

# Suma de produccion_piso_ton por unidad; min_count=1 evita sumar filas 100% NaN
vol_unidad = (
    df.groupby(["region", "piso_ecologico", "distrito", "unidad"], observed=True)["produccion_piso_ton"]
    .sum(min_count=1)
    .reset_index(name="produccion_total_ton")
    .sort_values("produccion_total_ton", ascending=False)
)
# Participación porcentual de cada unidad respecto al total agregado
vol_unidad["pct_total"] = 100 * vol_unidad["produccion_total_ton"] / vol_unidad["produccion_total_ton"].sum()

print("=== Top 5 unidades por volumen ===")
print(vol_unidad.head(5)[["unidad", "produccion_total_ton", "pct_total"]].to_string(index=False))

# Barras horizontales: una barra por unidad, color implícito por región (hue)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=vol_unidad, y="unidad", x="produccion_total_ton",
    hue="region", dodge=False, legend=False, ax=ax,
)
ax.set_title("Producción acumulada 2020–2025 por unidad (Pareto-80)")
ax.set_xlabel("Toneladas")
ax.set_ylabel("")
fig.tight_layout()
fig.savefig(RUTA_FIGURES / "eda_regional_volumen_unidad.png", dpi=150, bbox_inches="tight")
plt.show()
''',

    # --- Celda 5: §2 Series temporales ---
    '''\
# =============================================================================
# CELDA 3 — §2 Series temporales de producción (anual y mensual)
# =============================================================================
# Propósito:
#   Visualizar la evolución interanual por unidad territorial y la suma mensual
#   por región para detectar tendencias, quiebres y estacionalidad agregada.
# Sección del análisis: Análisis A — §2 Dinámica temporal.
# Salidas esperadas:
#   - Figura con dos subplots: OUTPUTS/figures/eda_regional_produccion_anual.png
#     (arriba: líneas anuales por unidad; abajo: mensual por región)
# =============================================================================

# Panel anual: una fila por (unidad, año) con producción sumada en el año
prod_anual = (
    df.groupby(["region", "piso_ecologico", "distrito", "unidad", "anio"], observed=True)["produccion_piso_ton"]
    .sum(min_count=1)
    .reset_index()
)

fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=False)

# Subplot superior: tendencia anual de cada unidad Pareto
for unidad, g in prod_anual.groupby("unidad"):
    axes[0].plot(g["anio"], g["produccion_piso_ton"], marker="o", label=unidad, linewidth=1.2)
axes[0].set_title("Producción anual agregada por unidad")
axes[0].set_xlabel("Año")
axes[0].set_ylabel("Toneladas")
axes[0].legend(bbox_to_anchor=(1.02, 1), fontsize=7, ncol=1)

# Subplot inferior: suma mensual de todas las unidades dentro de cada región
for region, g in df.groupby("region"):
    m = g.groupby("fecha", observed=True)["produccion_piso_ton"].sum(min_count=1)
    axes[1].plot(m.index, m.values, label=region, linewidth=1.2)
axes[1].set_title("Producción mensual sumada por región (todas las unidades)")
axes[1].set_ylabel("Toneladas")
axes[1].legend(fontsize=8)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(RUTA_FIGURES / "eda_regional_produccion_anual.png", dpi=150, bbox_inches="tight")
plt.show()
''',

    # --- Celda 7: §3 Heatmaps ---
    '''\
# =============================================================================
# CELDA 4 — §3 Heatmaps de estacionalidad mes × año por región
# =============================================================================
# Propósito:
#   Mostrar en cada región cómo se distribuye la producción entre meses y años,
#   resaltando picos de cosecha y años atípicos (sequía, Niño, etc.).
# Sección del análisis: Análisis A — §3 Estacionalidad regional.
# Salidas esperadas:
#   - Figura 2×3 (una por región): OUTPUTS/figures/eda_regional_heatmap_estacionalidad.png
# =============================================================================

regiones = sorted(df["region"].unique())
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.ravel()

for ax, region in zip(axes, regiones):
    sub = df[df["region"] == region]
    # Matriz mes (fila) × año (columna) con suma de toneladas
    pivot = sub.pivot_table(
        index="mes", columns="anio", values="produccion_piso_ton",
        aggfunc=lambda x: x.sum(min_count=1), observed=True,
    )
    # Reordenar filas según MESES_ORDEN definido en el setup
    pivot = pivot.reindex(MESES_ORDEN)
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", cbar_kws={"label": "ton"}, linewidths=0.2)
    ax.set_title(region)
    ax.set_xlabel("Año")
    ax.set_ylabel("Mes")

fig.suptitle("Estacionalidad productiva — mes × año (agregado regional)", y=1.02)
fig.tight_layout()
fig.savefig(RUTA_FIGURES / "eda_regional_heatmap_estacionalidad.png", dpi=150, bbox_inches="tight")
plt.show()
''',

    # --- Celda 9: §4 Patrón estacional ---
    '''\
# =============================================================================
# CELDA 5 — §4 Patrón estacional promedio (curva mes a mes por unidad)
# =============================================================================
# Propósito:
#   Promediar la producción de cada mes del calendario por unidad para ver el
#   ciclo típico de cosecha independiente del año (perfil fenológico agregado).
# Sección del análisis: Análisis A — §4 Ciclo estacional medio.
# Salidas esperadas:
#   - Figura de líneas: OUTPUTS/figures/eda_regional_patron_estacional.png
# =============================================================================

# Media mensual histórica por unidad (todos los años del panel)
patron = (
    df.groupby(["unidad", "mes"], observed=True)["produccion_piso_ton"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(11, 5))
for unidad, g in patron.groupby("unidad"):
    g = g.sort_values("mes")
    ax.plot(g["mes"].astype(str), g["produccion_piso_ton"], marker="o", label=unidad, linewidth=1)
ax.set_title("Patrón estacional promedio por unidad")
ax.set_xlabel("Mes")
ax.set_ylabel("Toneladas (promedio mensual)")
ax.tick_params(axis="x", rotation=45)
ax.legend(bbox_to_anchor=(1.02, 1), fontsize=7)
fig.tight_layout()
fig.savefig(RUTA_FIGURES / "eda_regional_patron_estacional.png", dpi=150, bbox_inches="tight")
plt.show()
''',

    # --- Celda 11: §5 Perfil climático ---
    '''\
# =============================================================================
# CELDA 6 — §5 Perfil climático promedio por unidad y boxplot de temperatura
# =============================================================================
# Propósito:
#   Comparar el clima medio 2020–2025 entre unidades Pareto (barras por variable)
#   y la dispersión mensual de temperatura por región y piso ecológico.
# Sección del análisis: Análisis A — §5 Contexto agroclimático.
# Salidas esperadas:
#   - OUTPUTS/figures/eda_regional_perfil_climatico.png (5 paneles CLIMA_EDA)
#   - OUTPUTS/figures/eda_regional_boxplot_temp.png (distribución temp_promedio)
# =============================================================================

# Promedio multianual de cada variable en CLIMA_EDA por unidad territorial
clima_mean = (
    df.groupby(["unidad", "region"], observed=True)[CLIMA_EDA]
    .mean()
    .reset_index()
)

# Panel de barras horizontales: una subfigura por variable climática
fig, axes = plt.subplots(1, len(CLIMA_EDA), figsize=(16, 5))
for ax, var in zip(axes, CLIMA_EDA):
    sns.barplot(
        data=clima_mean.sort_values(var, ascending=False),
        x=var, y="unidad", hue="region", dodge=False, ax=ax, legend=False,
    )
    ax.set_title(var)
    ax.set_ylabel("")
fig.suptitle("Perfil climático promedio por unidad (2020–2025)", y=1.02)
fig.tight_layout()
fig.savefig(RUTA_FIGURES / "eda_regional_perfil_climatico.png", dpi=150, bbox_inches="tight")
plt.show()

# Boxplot: variabilidad intra-anual de temperatura según región y piso
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df, x="region", y="temp_promedio", hue="piso_ecologico", ax=ax)
ax.set_title("Distribución mensual de temperatura por región y piso")
fig.tight_layout()
fig.savefig(RUTA_FIGURES / "eda_regional_boxplot_temp.png", dpi=150, bbox_inches="tight")
plt.show()
''',

    # --- Celda 13: §6 Correlaciones ---
    '''\
# =============================================================================
# CELDA 7 — §6 Correlaciones de Pearson producción–clima por unidad
# =============================================================================
# Propósito:
#   Estimar asociación lineal exploratoria entre produccion_piso_ton y cada
#   variable de CLIMA_EDA dentro de cada unidad (≥12 meses válidos). Incluye
#   ranking top-5 y correlación pooled sobre todas las unidades juntas.
# Sección del análisis: Análisis A — §6 Correlaciones (sin corrección BH).
# Salidas esperadas:
#   - CSV: OUTPUTS/eda_correlaciones_regional.csv
#   - Consola: top 5 |r| por unidad y tabla agregada pooled
# =============================================================================

rows = []
# Una correlación por (unidad, variable_clima) con metadatos territoriales
for unidad, g in df.groupby("unidad"):
    sub = g.dropna(subset=["produccion_piso_ton"] + CLIMA_EDA)
    if len(sub) < 12:
        continue
    region = g["region"].iloc[0]
    piso = g["piso_ecologico"].iloc[0]
    distrito = g["distrito"].iloc[0]
    for var in CLIMA_EDA:
        r, p = stats.pearsonr(sub["produccion_piso_ton"], sub[var])
        rows.append({
            "unidad": unidad, "region": region, "piso_ecologico": piso,
            "distrito": distrito, "variable_clima": var,
            "n": len(sub), "r": r, "p_valor": p,
        })

corr_regional = pd.DataFrame(rows)
corr_regional.to_csv(RUTA_OUTPUT / "eda_correlaciones_regional.csv", index=False, encoding="utf-8-sig")

top5 = corr_regional.reindex(corr_regional["r"].abs().sort_values(ascending=False).index).head(5)
print("=== Top 5 |r| por unidad (exploratorio, sin BH) ===")
print(top5[["unidad", "variable_clima", "n", "r", "p_valor"]].to_string(index=False))

# Pooling: mezcla todas las unidades — sesgo por heterogeneidad territorial
sub_all = df.dropna(subset=["produccion_piso_ton"] + CLIMA_EDA)
print("\\n=== Correlación agregada (pooling de todas las unidades) ===")
for var in CLIMA_EDA:
    r, p = stats.pearsonr(sub_all["produccion_piso_ton"], sub_all[var])
    print(f"{var:20s} r={r:+.3f}  p={p:.2e}  n={len(sub_all)}")
''',

    # --- Celda 15: §7 Puno sequía ---
    '''\
# =============================================================================
# CELDA 8 — §7 Caso de estudio: sequía altiplánica en Puno (2021→2022)
# =============================================================================
# Propósito:
#   Documentar cuantitativamente la caída productiva entre 2021 y 2022 en Puno
#   y contrastarla con la evolución de humedad de suelo (proxy de estrés hídrico).
# Sección del análisis: Análisis A — §7 Caso sequía (evidencia para el informe).
# Salidas esperadas:
#   - Consola: tabla de % cambio 2021→2022 por unidad (si hay datos).
#   - Figura dual-eje: OUTPUTS/figures/eda_regional_puno_sequia.png
# =============================================================================

puno = df[df["region"] == "Puno"].copy()

prod_puno = (
    puno.groupby(["unidad", "anio"], observed=True)["produccion_piso_ton"]
    .sum(min_count=1)
    .reset_index()
)
clima_puno = (
    puno.groupby(["unidad", "anio"], observed=True)["humedad_suelo"]
    .mean()
    .reset_index()
)

# Variación porcentual interanual por unidad (solo si hay producción positiva en 2021)
cambios = []
for unidad in prod_puno["unidad"].unique():
    p21 = prod_puno.query("unidad == @unidad and anio == 2021")["produccion_piso_ton"]
    p22 = prod_puno.query("unidad == @unidad and anio == 2022")["produccion_piso_ton"]
    if len(p21) and len(p22) and p21.iloc[0] > 0:
        pct = 100 * (p22.iloc[0] - p21.iloc[0]) / p21.iloc[0]
        cambios.append({"unidad": unidad, "pct_cambio_2021_2022": round(pct, 1)})
if cambios:
    print("=== Cambio producción Puno 2021→2022 ===")
    print(pd.DataFrame(cambios).to_string(index=False))

# Eje izquierdo: producción anual; eje derecho: humedad de suelo media anual
fig, ax1 = plt.subplots(figsize=(9, 4))
for unidad, g in prod_puno.groupby("unidad"):
    ax1.plot(g["anio"], g["produccion_piso_ton"], marker="o", label=f"Prod. {unidad}")
ax1.set_ylabel("Producción (ton)")
ax1.set_title("Puno — producción anual vs humedad de suelo (sequía altiplánica 2022)")
ax1.legend(fontsize=7, loc="upper left")

ax2 = ax1.twinx()
for unidad, g in clima_puno.groupby("unidad"):
    ax2.plot(g["anio"], g["humedad_suelo"], marker="s", linestyle="--", alpha=0.7, label=f"HS {unidad}")
ax2.set_ylabel("Humedad suelo (índice)")
fig.tight_layout()
fig.savefig(RUTA_FIGURES / "eda_regional_puno_sequia.png", dpi=150, bbox_inches="tight")
plt.show()
''',

    # --- Celda 17: §8 El Niño ---
    '''\
# =============================================================================
# CELDA 9 — §8 Caso de estudio: El Niño costero 2023–2024 (Piura, La Libertad, Ica)
# =============================================================================
# Propósito:
#   Comparar clima y producción de la costa norte-centro entre el periodo base
#   2020–2022 y el evento 2023–2024; visualizar series mensuales con sombreado.
# Sección del análisis: Análisis A — §8 Caso Niño costero.
# Salidas esperadas:
#   - Consola: precipitación y temperatura de referencia vs años del evento.
#   - Figura: OUTPUTS/figures/eda_regional_nino_costa.png (precip + producción)
# =============================================================================

costa = df[df["region"].isin(["Piura", "La Libertad", "Ica"])].copy()
ref = costa[costa["anio"].between(2020, 2022)].groupby("region")[["precipitacion", "temp_promedio"]].mean()
evt = costa[costa["anio"].isin([2023, 2024])].groupby(["region", "anio"])[["precipitacion", "temp_promedio"]].mean()

print("=== Referencia 2020–2022 vs evento 2023–2024 (costa norte-centro) ===")
for region in ["Piura", "La Libertad", "Ica"]:
    if region not in ref.index:
        continue
    ref_p = ref.loc[region, "precipitacion"]
    ref_t = ref.loc[region, "temp_promedio"]
    print(f"\\n{region} — ref precip={ref_p:.3f}  temp={ref_t:.2f}")
    if region in evt.index.get_level_values(0):
        print(evt.loc[region].round(3).to_string())

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# Panel izquierdo: precipitación mensual media por región costera
for region, g in costa.groupby("region"):
    m = g.groupby("fecha", observed=True)["precipitacion"].mean()
    axes[0].plot(m.index, m.values, label=region, linewidth=1.2)
axes[0].axvspan(pd.Timestamp("2023-01-01"), pd.Timestamp("2024-12-31"), alpha=0.15, color="coral", label="2023–2024")
axes[0].set_title("Precipitación mensual — costa")
axes[0].set_ylabel("mm/día")
axes[0].legend(fontsize=8)

# Panel derecho: producción mensual agregada en las mismas regiones
for region, g in costa.groupby("region"):
    m = g.groupby("fecha", observed=True)["produccion_piso_ton"].sum(min_count=1)
    axes[1].plot(m.index, m.values, label=region, linewidth=1.2)
axes[1].axvspan(pd.Timestamp("2023-01-01"), pd.Timestamp("2024-12-31"), alpha=0.15, color="coral")
axes[1].set_title("Producción mensual agregada — costa")
axes[1].set_ylabel("Toneladas")
axes[1].legend(fontsize=8)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(RUTA_FIGURES / "eda_regional_nino_costa.png", dpi=150, bbox_inches="tight")
plt.show()
''',

    # --- Celda 19: §9 Auditoría ---
    '''\
# =============================================================================
# CELDA 10 — §9 Auditoría de valores faltantes y resumen ejecutivo del Análisis A
# =============================================================================
# Propósito:
#   Contabilizar NaN en columnas climáticas y de producción; imprimir métricas
#   globales del panel y el número de figuras eda_regional_*.png generadas.
# Sección del análisis: Análisis A — §9 Cierre y trazabilidad de calidad.
# Salidas esperadas:
#   - Consola: conteo de NaN por columna (si los hay) y diccionario resumen.
#   - No genera archivos adicionales.
# =============================================================================

# Todas las columnas de temperatura más el núcleo de variables hidrometeorológicas
clima_cols = [c for c in df.columns if c.startswith("temp_") or c in (
    "precipitacion", "humedad_relativa", "radiacion_solar", "humedad_suelo",
)]
nan_audit = df[clima_cols + ["produccion_piso_ton"]].isna().sum()
print("=== Auditoría NaN ===")
print(nan_audit[nan_audit > 0] if (nan_audit > 0).any() else "Sin NaN en columnas revisadas")

resumen = {
    "filas": len(df),
    "unidades": df["unidad"].nunique(),
    "regiones": df["region"].nunique(),
    "nan_produccion": int(df["produccion_piso_ton"].isna().sum()),
    "figuras_generadas": len(list(RUTA_FIGURES.glob("eda_regional_*.png"))),
}
print("\\n=== Resumen Análisis A ===")
for k, v in resumen.items():
    print(f"{k}: {v}")
''',
]

# ---------------------------------------------------------------------------
# Notebook 05 — EDA por cultivo (Análisis B)
# Tres celdas de código (índices 1, 3, 5)
# ---------------------------------------------------------------------------

CELLS_05 = [
    # --- Celda 1: Setup ---
    '''\
# =============================================================================
# CELDA 1 — Configuración inicial y carga de dataset_integrado.csv
# =============================================================================
# Propósito:
#   Preparar el Análisis B (EDA por cultivo): resolver rutas del repo, cargar
#   el panel cultivo×mes del Pareto-80 (mapping v2) y verificar integridad básica.
# Sección del análisis: Setup / Análisis B — correlaciones por (región, cultivo).
# Salidas esperadas:
#   - Consola: número de filas, combinaciones región–cultivo y NaN en producción.
#   - No genera figuras ni CSV en esta celda.
# Nota: RUTA_MAPPING y DATASET_REGIONAL quedan definidos para trazabilidad
#       con el pipeline y comparación cruzada con el notebook 04.
# =============================================================================

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# Misma lógica de ROOT que en 04: notebooks/, SCRIPTS/ o subcarpeta del repo
ROOT = Path(".").resolve()
if ROOT.name == "notebooks":
    ROOT = ROOT.parent.parent
elif ROOT.name == "SCRIPTS":
    ROOT = ROOT.parent
elif not (ROOT / "OUTPUTS").exists() and (ROOT.parent / "OUTPUTS").exists():
    ROOT = ROOT.parent

RUTA_OUTPUT = ROOT / "OUTPUTS"
RUTA_OUTPUT.mkdir(parents=True, exist_ok=True)
RUTA_FIGURES = RUTA_OUTPUT / "figures"
RUTA_FIGURES.mkdir(parents=True, exist_ok=True)
RUTA_MAPPING = ROOT / "BDS" / "mapping" / "mapping_cultivo_distrito_v2_pipeline.csv"
DATASET_INTEGRADO = RUTA_OUTPUT / "dataset_integrado.csv"
DATASET_REGIONAL = RUTA_OUTPUT / "dataset_regional.csv"

# Panel granular: cada fila = mes × cultivo × distrito (Pareto-80)
df = pd.read_csv(DATASET_INTEGRADO)
print(f"Filas: {len(df):,} | Combos: {df.groupby(['region','cultivo']).ngroups}")
print(f"NaN produccion_ton: {df['produccion_ton'].isna().sum()}")
''',

    # --- Celda 3: Correlaciones ---
    '''\
# =============================================================================
# CELDA 2 — Correlaciones Pearson por par (región, cultivo)
# =============================================================================
# Propósito:
#   Para cada combinación región–cultivo del Pareto, calcular r de Pearson entre
#   produccion_ton y cada variable de CLIMA_EDA (mínimo 12 meses sin NaN).
#   Exploratorio: sin corrección Benjamini–Hochberg ni desestacionalización.
# Sección del análisis: Análisis B — núcleo de correlaciones por cultivo.
# Salidas esperadas:
#   - CSV: OUTPUTS/eda_correlaciones_por_cultivo.csv
#   - Consola: top 5 mayores |r| (hipótesis, no causalidad)
# Limitación: cultivos del mismo piso comparten clima idéntico → las diferencias
#             entre cultivos en una región reflejan sobre todo calendarios de cosecha.
# =============================================================================

CLIMA_EDA = [
    "temp_promedio", "precipitacion", "humedad_relativa",
    "radiacion_solar", "humedad_suelo",
]

rows = []
for (region, cultivo), g in df.groupby(["region", "cultivo"]):
    sub = g.dropna(subset=["produccion_ton"] + CLIMA_EDA)
    if len(sub) < 12:
        continue
    for var in CLIMA_EDA:
        r, p = stats.pearsonr(sub["produccion_ton"], sub[var])
        rows.append({
            "region": region,
            "cultivo": cultivo,
            "variable_clima": var,
            "n": len(sub),
            "r": r,
            "p_valor": p,
        })

corr_df = pd.DataFrame(rows)
top5 = corr_df.reindex(corr_df["r"].abs().sort_values(ascending=False).index).head(5)
print("=== Top 5 |r| (exploratorio, sin corrección BH) ===")
print(top5.to_string(index=False))
corr_df.to_csv(ROOT / "OUTPUTS" / "eda_correlaciones_por_cultivo.csv", index=False, encoding="utf-8-sig")
''',

    # --- Celda 5: Caso Puno ---
    '''\
# =============================================================================
# CELDA 3 — Caso Puno: producción anual desagregada por cultivo
# =============================================================================
# Propósito:
#   Visualizar la evolución interanual de cada cultivo Pareto en Puno para
#   complementar el caso sequía del notebook 04 con granularidad por cultivo
#   (papa, quinua, alfalfa, etc.) — análisis descriptivo sin test formal.
# Sección del análisis: Análisis B — caso de estudio Puno / sequía 2022.
# Salidas esperadas:
#   - Figura: OUTPUTS/figures/eda_puno_produccion_anual.png
# =============================================================================

puno = df[df["region"] == "Puno"].copy()
if not puno.empty:
    idx = puno.groupby(["cultivo", "anio"])["produccion_ton"].sum(min_count=1).reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    for cultivo, g in idx.groupby("cultivo"):
        ax.plot(g["anio"], g["produccion_ton"], marker="o", label=cultivo)
    ax.set_title("Puno — producción anual por cultivo (Pareto)")
    ax.set_ylabel("Toneladas")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(RUTA_FIGURES / "eda_puno_produccion_anual.png", dpi=150, bbox_inches="tight")
    plt.show()
''',
]

NOTEBOOK_MAP: dict[str, list[str]] = {
    "04_eda_regional.ipynb": CELLS_04,
    "05_eda_por_cultivo.ipynb": CELLS_05,
}

TARGETS = [
    REPO_ROOT / "SCRIPTS" / "notebooks" / "04_eda_regional.ipynb",
    REPO_ROOT / "SCRIPTS" / "04_eda_regional.ipynb",
    REPO_ROOT / "SCRIPTS" / "notebooks" / "05_eda_por_cultivo.ipynb",
]


def _source_lines(text: str) -> list[str]:
    """Convierte bloque de código en lista de líneas para el JSON del notebook."""
    if not text.endswith("\n"):
        text += "\n"
    return [line if line.endswith("\n") else line + "\n" for line in text.splitlines(keepends=True)]


def apply_comments(nb_path: Path, commented_cells: list[str]) -> int:
    """Reemplaza cada celda de código en orden con el texto comentado correspondiente."""
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    code_idx = 0
    replaced = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        if code_idx >= len(commented_cells):
            raise IndexError(
                f"{nb_path}: más celdas de código ({code_idx + 1}) que textos comentados "
                f"({len(commented_cells)})"
            )
        cell["source"] = _source_lines(commented_cells[code_idx])
        code_idx += 1
        replaced += 1
    if code_idx != len(commented_cells):
        raise ValueError(
            f"{nb_path}: se esperaban {len(commented_cells)} celdas de código, "
            f"se encontraron {code_idx}"
        )
    nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return replaced


def main() -> None:
    for nb_path in TARGETS:
        if not nb_path.exists():
            print(f"OMITIDO (no existe): {nb_path}")
            continue
        key = nb_path.name
        commented = NOTEBOOK_MAP[key]
        n = apply_comments(nb_path, commented)
        rel = nb_path.relative_to(REPO_ROOT)
        print(f"OK {rel}: {n} celdas de código actualizadas")


if __name__ == "__main__":
    main()
