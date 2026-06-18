# -*- coding: utf-8 -*-
"""Reemplaza celdas de código de 06_clustering_cultivos.ipynb con comentarios extensivos en español."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NB_PATH = ROOT / "SCRIPTS" / "notebooks" / "06_clustering_cultivos.ipynb"

COMMENTED_SOURCES: dict[int, str] = {}


def _cell(idx: int, text: str) -> None:
    COMMENTED_SOURCES[idx] = text.rstrip() + "\n"


# ---------------------------------------------------------------------------
# CELDA 2 — Importaciones
# ---------------------------------------------------------------------------
_cell(2, r"""# ====================================================================
# CELDA: Importaciones sklearn, scipy y utilidades de visualización
# ====================================================================
# Primer bloque ejecutable del notebook 06 (clustering agroclimático).
# Carga librerías para: agrupamiento (KMeans, jerárquico Ward, DBSCAN),
# reducción de dimensionalidad (PCA, NMF), métricas internas de clusters
# y gráficos de validación (dendrograma, heatmaps, scatter PCA).
# No genera archivos; prepara el entorno numérico reutilizado en todo el análisis.

# --- Librerías estándar ---
# warnings: silencia avisos deprecados durante barridos de K y grid DBSCAN.
# pathlib.Path: rutas relativas al repo (OUTPUTS/, figures/) sin hardcodear SO.
import warnings
from pathlib import Path

# --- Visualización ---
# matplotlib + seaborn: gráficos de selección de K, dendrogramas, heatmaps,
#   barras comparativas y scatter PCA anotado por cultivo.
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# --- Clustering (scipy + sklearn) ---
# linkage / dendrogram: árbol jerárquico aglomerativo (método Ward).
# KMeans: partición en K grupos minimizando inercia — método principal del paper.
# AgglomerativeClustering: jerárquico con K fijo para comparar con KMeans.
# DBSCAN: clustering por densidad; etiqueta -1 = ruido/outlier no asignado.
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans

# --- Reducción de dimensionalidad ---
# PCA: componentes ortogonales que capturan varianza climática (análisis mensual).
# NMF: factorización no negativa sobre datos escalados [0,1] (patrones latentes).
from sklearn.decomposition import PCA, NMF

# --- Métricas internas de calidad de clustering (sklearn.metrics) ---
# silhouette_score: cohesión vs separación en [-1, 1]; mayor = clusters más nítidos.
# davies_bouldin_score: ratio dispersión intra/inter; menor = mejor separación.
# calinski_harabasz_score: varianza entre/sobre clusters; mayor = mejor (usado en barrido K).
# silhouette_samples: Silhouette por observación (reservado para diagnóstico fino).
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_samples,
    silhouette_score,
)

# NearestNeighbors: utilidad para explorar distancias k-NN al calibrar eps en DBSCAN.
from sklearn.neighbors import NearestNeighbors

# --- Escalado de features ---
# StandardScaler: z-score (media 0, std 1) para KMeans/jerárquico/DBSCAN en perfiles.
# MinMaxScaler: escala [0, 1] exigida por NMF (solo valores no negativos).
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Configuración global: ignorar warnings, 120 dpi, estilo whitegrid, paleta tab10.
warnings.filterwarnings("ignore")
plt.rcParams["figure.dpi"] = 120
sns.set_style("whitegrid")
PALETTE = sns.color_palette("tab10")
print("Librerías cargadas")
""")

# ---------------------------------------------------------------------------
# CELDA 4 — Carga de datos
# ---------------------------------------------------------------------------
_cell(4, r"""# ====================================================================
# CELDA: Carga de dataset_integrado.csv y rutas de salida
# ====================================================================
# Lee la tabla maestra producida por el notebook 03 (merge MIDAGRI + NASA + mapping).
# Input: OUTPUTS/dataset_integrado.csv (~2.376 filas cultivo×mes, 6 regiones Pareto-80).
# Crea OUTPUTS/figures/ para PNGs del clustering. Imprime dimensiones y vista previa.
# La unidad principal del análisis será la agregación posterior a perfil región×cultivo.

# Resolución de ROOT: compatible si el kernel arranca en notebooks/, Clustering/ o repo raíz.
ROOT = Path.cwd().resolve()
if ROOT.name == "notebooks":
    ROOT = ROOT.parent.parent
elif ROOT.name == "Clustering":
    ROOT = ROOT.parent

# Rutas de insumo (CSV integrado) y salida (CSVs + figuras de clustering).
RUTA_DATA = ROOT / "OUTPUTS" / "dataset_integrado.csv"
RUTA_OUT = ROOT / "OUTPUTS"
RUTA_FIG = RUTA_OUT / "figures"
RUTA_FIG.mkdir(parents=True, exist_ok=True)

# Carga en memoria: cada fila = un mes de un cultivo Pareto en un distrito/piso/región.
df = pd.read_csv(RUTA_DATA)
print(f"Dimensiones: {df.shape[0]:,} filas x {df.shape[1]} columnas")
print(f"Combinaciones (región, cultivo): {df.groupby(['region', 'cultivo']).ngroups}")
print("Columnas:", list(df.columns))
df.head()
""")

# ---------------------------------------------------------------------------
# CELDA 6 — Variables climáticas
# ---------------------------------------------------------------------------
_cell(6, r"""# ====================================================================
# CELDA: Variables climáticas NASA y exploración básica del dataset
# ====================================================================
# Define las 12 variables descargadas de NASA POWER y el subconjunto CLIMA_CORE
# (5 variables interpretables usadas en la agregación de perfiles).
# Imprime regiones, pisos ecológicos, número de cultivos y NaN en producción.
# Contexto: el clima es idéntico para todos los cultivos del mismo distrito/mes.

# Lista completa de variables climáticas (12 columnas NASA en dataset_integrado).
CLIMA_VARS = [
    "temp_promedio", "temp_maxima", "temp_minima", "precipitacion",
    "humedad_relativa", "radiacion_solar", "velocidad_viento",
    "presion_atmosferica", "humedad_suelo", "temp_superficie",
    "punto_rocio", "humedad_especifica",
]

# Subconjunto reducido para perfiles: temperatura, lluvia, humedad, radiación, suelo.
CLIMA_CORE = [
    "temp_promedio", "precipitacion", "humedad_relativa",
    "radiacion_solar", "humedad_suelo",
]

# Auditoría exploratoria antes de agregar perfiles.
print("Regiones :", sorted(df["region"].unique()))
print("Pisos    :", sorted(df["piso_ecologico"].unique()))
print("Cultivos :", df["cultivo"].nunique())
print("NaN produccion_ton:", df["produccion_ton"].isna().sum())
""")

# ---------------------------------------------------------------------------
# CELDA 8 — Funciones auxiliares
# ---------------------------------------------------------------------------
_cell(8, r"""# ====================================================================
# CELDA: Funciones auxiliares — métricas, barrido K, DBSCAN y gráficos
# ====================================================================
# Define utilidades reutilizadas en todo el notebook:
#   - Métricas adaptadas a DBSCAN (Silhouette sin ruido, % puntos -1).
#   - eval_kmeans_range: barrido K=2..8 con Silhouette, Calinski, Davies-Bouldin.
#   - elegir_k: consenso entre mejor Silhouette y mejor Davies-Bouldin.
#   - grid_dbscan: búsqueda en rejilla (eps × min_samples).
#   - plot_k_selection: panel codo + Silhouette + Davies-Bouldin.
# Estas funciones encapsulan la lógica de validación interna de clusters.

# Rango por defecto de K a evaluar en KMeans (particiones de 2 a 8 clusters).
K_RANGE = range(2, 9)


# Silhouette excluyendo etiquetas -1 (ruido DBSCAN): evita sesgar la métrica
# con puntos no asignados que no pertenecen a ningún cluster denso.
def silhouette_no_noise(X, labels):
    mask = labels >= 0
    labs = labels[mask]
    if len(set(labs)) < 2 or mask.sum() < 3:
        return np.nan
    return float(silhouette_score(X[mask], labs))


# Porcentaje de observaciones marcadas como ruido (etiqueta -1) por DBSCAN.
def pct_ruido(labels):
    return 100.0 * (labels < 0).mean()


# Barrido sistemático de K en KMeans: para cada K guarda inercia, Silhouette,
# Calinski-Harabasz, Davies-Bouldin, etiquetas y el modelo ajustado.
def eval_kmeans_range(X, k_range=K_RANGE, random_state=42):
    rows = []
    for k in k_range:
        # n_init=10: múltiples inicializaciones aleatorias para evitar mínimos locales.
        km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        lbl = km.fit_predict(X)
        rows.append({
            "k": k,
            "inertia": km.inertia_,
            "silhouette": silhouette_score(X, lbl),
            "calinski": calinski_harabasz_score(X, lbl),
            "davies_bouldin": davies_bouldin_score(X, lbl),
            "labels": lbl,
            "model": km,
        })
    return pd.DataFrame(rows)


# Selección de K óptimo: si Silhouette y Davies-Bouldin coinciden, usar ese K;
# si no, promediar rankings de ambas métricas (compromiso interpretabilidad/calidad).
def elegir_k(df_km):
    best_sil = int(df_km.loc[df_km["silhouette"].idxmax(), "k"])
    best_db = int(df_km.loc[df_km["davies_bouldin"].idxmin(), "k"])
    if best_sil == best_db:
        return best_sil, "coincidencia Silhouette y Davies-Bouldin"
    rank_sil = df_km.set_index("k")["silhouette"].rank(ascending=False)
    rank_db = df_km.set_index("k")["davies_bouldin"].rank(ascending=True)
    k_opt = int((rank_sil + rank_db).idxmin())
    return k_opt, f"ranking promedio (Sil={best_sil}, DB={best_db})"


# Rejilla DBSCAN: prueba combinaciones (eps, min_samples), descarta configs con <2 clusters,
# ordena por Silhouette (sin ruido). eps = radio de vecindad; min_samples = densidad mínima.
def grid_dbscan(X, eps_list, ms_list):
    rows = []
    for eps in eps_list:
        for ms in ms_list:
            # fit_predict asigna -1 a puntos en regiones de baja densidad.
            lbl = DBSCAN(eps=eps, min_samples=ms).fit_predict(X)
            n_cl = len(set(lbl)) - (1 if -1 in lbl else 0)
            if n_cl < 2:
                continue
            rows.append({
                "eps": eps,
                "min_samples": ms,
                "n_clusters": n_cl,
                "pct_ruido": pct_ruido(lbl),
                "silhouette": silhouette_no_noise(X, lbl),
                "davies_bouldin": davies_bouldin_score(X[lbl >= 0], lbl[lbl >= 0]),
                "labels": lbl,
            })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values("silhouette", ascending=False)


# Panel de diagnóstico visual para elegir K: inercia (método del codo), Silhouette y Davies-Bouldin.
def plot_k_selection(df_km, titulo):
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))
    # Panel 1: curva de inercia — buscar "codo" donde añadir clusters aporta poco.
    axes[0].plot(df_km["k"], df_km["inertia"], "o-", color="steelblue")
    axes[0].set_title("Codo (inercia)")
    axes[0].set_xlabel("K")
    # Panel 2: Silhouette por K — línea roja en el K con mayor cohesión/separación.
    best_sil = int(df_km.loc[df_km["silhouette"].idxmax(), "k"])
    axes[1].plot(df_km["k"], df_km["silhouette"], "o-", color="green")
    axes[1].axvline(best_sil, color="red", ls="--", label=f"K={best_sil}")
    axes[1].set_title("Silhouette")
    axes[1].legend()
    # Panel 3: Davies-Bouldin por K — línea en el K con menor dispersión relativa.
    best_db = int(df_km.loc[df_km["davies_bouldin"].idxmin(), "k"])
    axes[2].plot(df_km["k"], df_km["davies_bouldin"], "o-", color="crimson")
    axes[2].axvline(best_db, color="navy", ls="--", label=f"K={best_db}")
    axes[2].set_title("Davies-Bouldin")
    axes[2].legend()
    plt.suptitle(titulo, fontweight="bold")
    plt.tight_layout()
    plt.show()
""")

# ---------------------------------------------------------------------------
# CELDA 10 — Agregación de perfiles
# ---------------------------------------------------------------------------
_cell(10, r"""# ====================================================================
# CELDA: Agregación de perfiles región×cultivo (unidad principal del análisis)
# ====================================================================
# Colapsa las ~72 filas mensuales de cada par (región, cultivo, piso, distrito)
# en UN perfil agroclimático-productivo con features interpretables:
#   - Producción: total, media en meses de cosecha, coeficiente de variación.
#   - Clima CLIMA_CORE: media y desviación estándar temporal por variable.
# Estandariza con StandardScaler → matriz X_perfil para KMeans/jerárquico/DBSCAN.
# Output: df_perfil (~33 filas) y X_perfil (numpy array z-score).

# Coeficiente de variación (std/mean) solo en meses con producción estrictamente > 0.
def coef_var_positivos(s):
    v = s.dropna()
    v = v[v > 0]
    if len(v) < 2 or v.mean() == 0:
        return np.nan
    return v.std() / v.mean()


# Diccionario de agregaciones pandas: tuplas (columna_origen, función).
agg_dict = {
    "produccion_total": ("produccion_ton", lambda s: s.dropna().sum()),
    "produccion_media_cosecha": (
        "produccion_ton",
        lambda s: s[s > 0].mean() if (s > 0).any() else np.nan,
    ),
    "coef_var_produccion": ("produccion_ton", coef_var_positivos),
    "n_meses_con_dato": ("produccion_ton", lambda s: s.notna().sum()),
    "n_meses_cosecha": ("produccion_ton", lambda s: (s > 0).sum()),
}

# Por cada variable CLIMA_CORE añadir media y std temporal al perfil.
for v in CLIMA_CORE:
    agg_dict[f"{v}_mean"] = (v, "mean")
    agg_dict[f"{v}_std"] = (v, "std")

# groupby: una fila por combinación región×cultivo×piso×distrito (33 perfiles Pareto-80).
df_perfil = df.groupby(
    ["region", "cultivo", "piso_ecologico", "distrito"], as_index=False
).agg(**agg_dict)

# Etiqueta legible para dendrograma y anotaciones: "Región | cultivo".
df_perfil["etiqueta"] = df_perfil["region"] + " | " + df_perfil["cultivo"]

# Lista de columnas numéricas que alimentan el clustering (clima mean/std + producción).
FEATURES_PERFIL = [c for c in df_perfil.columns if c.endswith("_mean") or c.endswith("_std")]
FEATURES_PERFIL += [
    "produccion_total", "produccion_media_cosecha", "coef_var_produccion",
]

# Matriz cruda y estandarizada: KMeans asume features en escala comparable.
X_perfil_raw = df_perfil[FEATURES_PERFIL].copy()
scaler_perfil = StandardScaler()
X_perfil = scaler_perfil.fit_transform(X_perfil_raw)

print(f"Perfiles: {df_perfil.shape[0]} filas x {len(FEATURES_PERFIL)} features")
df_perfil[["region", "cultivo", "produccion_total", "n_meses_cosecha"]].head(10)
""")

# ---------------------------------------------------------------------------
# CELDA 12 — KMeans perfiles
# ---------------------------------------------------------------------------
_cell(12, r"""# ====================================================================
# CELDA: KMeans sobre perfiles — selección de K y ajuste final
# ====================================================================
# Análisis PRINCIPAL del notebook: clustering de los ~33 perfiles estandarizados.
# 1) Barrido K=2..7 con eval_kmeans_range y panel plot_k_selection.
# 2) elegir_k determina K_PERFIL (típicamente K=6 en la versión actual).
# 3) KMeans final: asigna cluster_kmeans, calcula Silhouette y Davies-Bouldin.
# Figura esperada: seleccion_k_perfiles.png (generada por plot_k_selection si se guarda).

# Barrido de K sobre X_perfil (espacio z-score de features agroclimáticas).
km_perfil_df = eval_kmeans_range(X_perfil, k_range=range(2, 8))
K_PERFIL, motivo_k = elegir_k(km_perfil_df)
plot_k_selection(km_perfil_df, f"Selección de K — perfiles (K={K_PERFIL})")
print(f"K óptimo perfiles: {K_PERFIL} ({motivo_k})")

# Modelo definitivo KMeans con K_PERFIL clusters sobre perfiles.
km_perfil = KMeans(n_clusters=K_PERFIL, random_state=42, n_init=10)
labels_perfil_km = km_perfil.fit_predict(X_perfil)
df_perfil["cluster_kmeans"] = labels_perfil_km

# Métricas de calidad del particionado final (referencia para tabla comparativa).
sil_perfil_km = silhouette_score(X_perfil, labels_perfil_km)
db_perfil_km = davies_bouldin_score(X_perfil, labels_perfil_km)
print(f"Silhouette={sil_perfil_km:.4f}  Davies-Bouldin={db_perfil_km:.4f}")
""")

# ---------------------------------------------------------------------------
# CELDA 14 — Jerárquico
# ---------------------------------------------------------------------------
_cell(14, r"""# ====================================================================
# CELDA: Clustering jerárquico aglomerativo (Ward) y dendrograma
# ====================================================================
# Complementa KMeans con enfoque bottom-up: fusiones Ward minimizan varianza intra-grupo.
# 1) linkage() construye matriz de fusiones sobre X_perfil estandarizado.
# 2) dendrogram() visualiza el árbol con etiquetas región|cultivo.
# 3) AgglomerativeClustering con mismo K_PERFIL para comparar asignaciones.
# Output PNG: OUTPUTS/figures/dendrograma_perfiles.png

# Matriz de enlace jerárquico (método Ward = distancia euclídea en espacio estandarizado).
Z = linkage(X_perfil, method="ward")

# Dendrograma: altura de fusión indica disimilitud; hojas = perfiles individuales.
fig, ax = plt.subplots(figsize=(14, 6))
dendrogram(
    Z,
    labels=df_perfil["etiqueta"].tolist(),
    leaf_rotation=90,
    leaf_font_size=8,
    color_threshold=None,
    ax=ax,
)
ax.set_title("Dendrograma — perfiles (región | cultivo)", fontweight="bold")
plt.tight_layout()
plt.savefig(RUTA_FIG / "dendrograma_perfiles.png", dpi=150, bbox_inches="tight")
plt.show()

# Clustering jerárquico con K fijo = K_PERFIL (misma cardinalidad que KMeans).
hc = AgglomerativeClustering(n_clusters=K_PERFIL, linkage="ward")
labels_perfil_hc = hc.fit_predict(X_perfil)
df_perfil["cluster_jerarquico"] = labels_perfil_hc
sil_perfil_hc = silhouette_score(X_perfil, labels_perfil_hc)
print(f"Jerárquico K={K_PERFIL} | Silhouette={sil_perfil_hc:.4f}")
""")

# ---------------------------------------------------------------------------
# CELDA 16 — DBSCAN perfiles
# ---------------------------------------------------------------------------
_cell(16, r"""# ====================================================================
# CELDA: DBSCAN sobre perfiles — grid de hiperparámetros
# ====================================================================
# DBSCAN no requiere K a priori pero es sensible a eps y min_samples en espacio z-score.
# Se prueba una rejilla reducida; se elige la config con mayor Silhouette (sin ruido).
# En perfiles suele haber alto % de ruido → método complementario, no principal.
# Guarda cluster_dbscan, sil_perfil_db y pct_noise_p para la tabla comparativa.

# Rejilla DBSCAN sobre X_perfil: eps en unidades de desviación estándar.
res_db_perfil = grid_dbscan(
    X_perfil,
    eps_list=[0.8, 1.0, 1.2, 1.5, 2.0, 2.5],
    ms_list=[2, 3, 4],
)

if len(res_db_perfil):
    # Mejor fila = mayor Silhouette tras excluir puntos -1.
    best_db_p = res_db_perfil.iloc[0]
    labels_perfil_db = best_db_p["labels"].astype(int)
    df_perfil["cluster_dbscan"] = labels_perfil_db
    sil_perfil_db = best_db_p["silhouette"]
    pct_noise_p = best_db_p["pct_ruido"]
    print("Top DBSCAN perfiles:")
    print(res_db_perfil[["eps", "min_samples", "n_clusters", "pct_ruido", "silhouette"]].head(5).to_string(index=False))
else:
    # Sin configuración válida: todos los perfiles marcados como ruido (-1).
    labels_perfil_db = np.full(len(df_perfil), -1)
    df_perfil["cluster_dbscan"] = labels_perfil_db
    sil_perfil_db = np.nan
    pct_noise_p = 100.0
    print("DBSCAN perfiles: sin configuración válida")
""")

# ---------------------------------------------------------------------------
# CELDA 18 — Tabla, heatmap, PCA 2D
# ---------------------------------------------------------------------------
_cell(18, r"""# ====================================================================
# CELDA: Tabla de asignaciones, heatmap de centroides y PCA 2D de perfiles
# ====================================================================
# Consolida resultados del bloque principal (perfiles):
#   - tabla_perfil: asignaciones KMeans, jerárquico y DBSCAN por cultivo.
#   - crosstab: composición de cada cluster KMeans por región.
#   - heatmap: centroides normalizados min-max por variable → heatmap_perfiles_kmeans.png.
#   - scatter PCA 2D coloreado por cluster KMeans con anotación de cultivos.

# Tabla ordenada: región, cultivo, piso, distrito, tres métodos y producción total.
tabla_perfil = df_perfil[
    ["region", "cultivo", "piso_ecologico", "distrito",
     "cluster_kmeans", "cluster_jerarquico", "cluster_dbscan", "produccion_total"]
].sort_values(["cluster_kmeans", "region", "cultivo"])
print(tabla_perfil.to_string(index=False))

# Crosstab: cuántos cultivos de cada región caen en cada cluster KMeans.
comp_region = pd.crosstab(df_perfil["cluster_kmeans"], df_perfil["region"])
print("\nComposición KMeans por región:")
print(comp_region)

# Centroides KMeans: media de cada feature por cluster; normalización 0-1 para heatmap.
cent = df_perfil.groupby("cluster_kmeans")[FEATURES_PERFIL].mean()
cent_norm = (cent - cent.min()) / (cent.max() - cent.min() + 1e-9)

fig, ax = plt.subplots(figsize=(12, 4))
sns.heatmap(cent_norm.T, annot=False, cmap="YlOrRd", ax=ax)
ax.set_title("Perfil normalizado por cluster KMeans", fontweight="bold")
ax.set_xticklabels([f"C{i}" for i in cent.index])
plt.tight_layout()
plt.savefig(RUTA_FIG / "heatmap_perfiles_kmeans.png", dpi=150, bbox_inches="tight")
plt.show()

# PCA con 2 componentes sobre perfiles: proyección visual del espacio de clustering.
pca_p = PCA(n_components=2, random_state=42)
xy_p = pca_p.fit_transform(X_perfil)

fig, ax = plt.subplots(figsize=(9, 7))
for c in sorted(df_perfil["cluster_kmeans"].unique()):
    m = df_perfil["cluster_kmeans"] == c
    ax.scatter(xy_p[m, 0], xy_p[m, 1], label=f"Cluster {c}", s=80, alpha=0.85)
for idx, (_, row) in enumerate(df_perfil.iterrows()):
    ax.annotate(row["cultivo"][:12], (xy_p[idx, 0], xy_p[idx, 1]), fontsize=6, alpha=0.7)
ax.set_title("PCA perfiles — KMeans", fontweight="bold")
ax.legend()
plt.tight_layout()
plt.show()
""")

# ---------------------------------------------------------------------------
# CELDA 20 — Perfil narrativo
# ---------------------------------------------------------------------------
_cell(20, r"""# ====================================================================
# CELDA: Perfil narrativo por cluster KMeans (interpretación agronómica)
# ====================================================================
# Imprime en consola un resumen textual de cada cluster KMeans:
#   - Cultivos miembros (región-cultivo), pisos ecológicos presentes.
#   - Medias de variables climáticas clave y producción total / meses de cosecha.
# Sirve para nombrar clusters (costa industrial, selva húmeda, altiplano, etc.)
# sin generar archivos adicionales — complementa el heatmap y la tabla.

print("=" * 70)
print("PERFIL CLIMÁTICO Y PRODUCTIVO POR CLUSTER")
print("=" * 70)

# Variables seleccionadas por interpretabilidad agronómica (no todas las features).
vars_interpretar = [
    'temp_promedio_mean', 'precipitacion_mean',
    'humedad_suelo_mean', 'radiacion_solar_mean',
    'produccion_total', 'n_meses_cosecha'
]

for c in sorted(df_perfil['cluster_kmeans'].unique()):
    sub = df_perfil[df_perfil['cluster_kmeans'] == c]
    print(f"\nCluster {c} ({len(sub)} cultivos)")
    print(f"  Cultivos : {', '.join(sub['region'] + '-' + sub['cultivo'])}")
    print(f"  Pisos    : {', '.join(sorted(sub['piso_ecologico'].unique()))}")
    print(f"  ---")
    for v in vars_interpretar:
        if v in df_perfil.columns:
            val = sub[v].mean()
            print(f"  {v:<30}: {val:.2f}")
    print()
""")

# ---------------------------------------------------------------------------
# CELDA 22 — Matriz mensual clima
# ---------------------------------------------------------------------------
_cell(22, r"""# ====================================================================
# CELDA: Matriz mensual solo clima (análisis complementario)
# ====================================================================
# Prepara un segundo nivel de análisis sobre filas mensuales (no perfiles):
# ~2.376 observaciones con las 12 variables climáticas completas.
# Limitación metodológica: el mismo vector climático se repite para cada cultivo
# del mismo distrito/mes → infla artificialmente Silhouette en clustering mensual.
# X_clima = z-score; X_clima_mm = MinMax [0,1] para NMF posterior.

# Filas con las 12 variables climáticas sin NaN (descarta meses incompletos NASA).
df_clima = df.dropna(subset=CLIMA_VARS, how="any").copy()
X_clima_raw = df_clima[CLIMA_VARS].values

# Escalado estándar para KMeans/PCA/DBSCAN mensual.
scaler_clima = StandardScaler()
X_clima = scaler_clima.fit_transform(X_clima_raw)

# Escalado MinMax para NMF (requiere entradas no negativas en [0, 1]).
scaler_mm = MinMaxScaler()
X_clima_mm = scaler_mm.fit_transform(X_clima_raw)

print(f"Filas mensuales con clima completo: {len(df_clima):,}")
""")

# ---------------------------------------------------------------------------
# CELDA 24 — KMeans y DBSCAN mensual
# ---------------------------------------------------------------------------
_cell(24, r"""# ====================================================================
# CELDA: KMeans y DBSCAN sobre filas mensuales (solo clima)
# ====================================================================
# Análisis COMPLEMENTARIO: clustering directo de observaciones mes×distrito
# sin agregar por cultivo. K barrido 2..10 (más filas que perfiles).
# DBSCAN con rejilla más amplia (eps y min_samples mayores por n≈2376).
# Métricas guardadas en variables sil_mensual_*, pct_noise_m para tabla final.
# Advertencia: interpretabilidad Baja — no usar como resultado principal del paper.

# Barrido KMeans mensual sobre X_clima (12 vars estandarizadas).
km_mensual_df = eval_kmeans_range(X_clima, k_range=range(2, 11))
K_MENSUAL, _ = elegir_k(km_mensual_df)
plot_k_selection(km_mensual_df, f"KMeans mensual — solo clima (K={K_MENSUAL})")

# Ajuste final KMeans mensual.
km_mensual = KMeans(n_clusters=K_MENSUAL, random_state=42, n_init=10)
labels_mensual_km = km_mensual.fit_predict(X_clima)
sil_mensual_km = silhouette_score(X_clima, labels_mensual_km)
db_mensual_km = davies_bouldin_score(X_clima, labels_mensual_km)
print(f"KMeans mensual K={K_MENSUAL} | Sil={sil_mensual_km:.4f}")

# Grid DBSCAN mensual: más puntos → eps más pequeños y min_samples más altos.
res_db_mensual = grid_dbscan(
    X_clima,
    eps_list=[0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0],
    ms_list=[3, 5, 10, 15],
)
if len(res_db_mensual):
    best_db_m = res_db_mensual.iloc[0]
    labels_mensual_db = best_db_m["labels"].astype(int)
    sil_mensual_db = best_db_m["silhouette"]
    pct_noise_m = best_db_m["pct_ruido"]
    print(f"DBSCAN mensual eps={best_db_m['eps']} ms={int(best_db_m['min_samples'])} | Sil={sil_mensual_db:.4f} | ruido={pct_noise_m:.1f}%")
else:
    labels_mensual_db = np.full(len(df_clima), -1)
    sil_mensual_db = np.nan
    pct_noise_m = 100.0
""")

# ---------------------------------------------------------------------------
# CELDA 26 — PCA mensual
# ---------------------------------------------------------------------------
_cell(26, r"""# ====================================================================
# CELDA: PCA sobre filas mensuales — varianza, loadings y clustering
# ====================================================================
# Reducción lineal de 12 variables climáticas:
#   1) PCA completo → varianza acumulada y loadings PC1–PC2 (heatmap).
#   2) Selección de n_pc_90 componentes que explican ≥90% varianza (máx 8).
#   3) KMeans + DBSCAN en el espacio PCA reducido (menos dimensionalidad).
# Interpretabilidad Media: los clusters están en espacio de componentes, no en clima directo.

# Ajuste PCA sin truncar: examinar cuántas componentes capturan 90% de varianza.
pca_full = PCA(random_state=42)
pca_full.fit(X_clima)
var_ac = np.cumsum(pca_full.explained_variance_ratio_)
n_pc_90 = int(np.searchsorted(var_ac, 0.90) + 1)
n_pc_90 = max(2, min(n_pc_90, 8))

# Panel izquierdo: curva de varianza acumulada; derecho: loadings PC1 y PC2 por variable.
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(range(1, len(var_ac) + 1), var_ac, "o-")
axes[0].axhline(0.9, ls="--", color="gray")
axes[0].set_title("Varianza acumulada PCA")
load = pd.DataFrame(pca_full.components_[:2].T, index=CLIMA_VARS, columns=["PC1", "PC2"])
sns.heatmap(load, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=axes[1])
axes[1].set_title("Loadings PC1–PC2")
plt.tight_layout()
plt.show()

# PCA truncado a n_pc_90 componentes → matriz X_pca para clustering en espacio reducido.
pca = PCA(n_components=n_pc_90, random_state=42)
X_pca = pca.fit_transform(X_clima)

km_pca_df = eval_kmeans_range(X_pca, k_range=range(2, 11))
K_PCA, _ = elegir_k(km_pca_df)
labels_pca_km = KMeans(n_clusters=K_PCA, random_state=42, n_init=10).fit_predict(X_pca)
sil_pca_km = silhouette_score(X_pca, labels_pca_km)

# DBSCAN en espacio PCA (distancias en componentes principales, no en clima original).
res_pca_db = grid_dbscan(X_pca, eps_list=[0.8, 1.2, 1.5, 2.0, 2.5], ms_list=[5, 10, 15, 20])
if len(res_pca_db):
    best_pca_db = res_pca_db.iloc[0]
    labels_pca_db = best_pca_db["labels"].astype(int)
    sil_pca_db = best_pca_db["silhouette"]
    pct_noise_pca = best_pca_db["pct_ruido"]
else:
    labels_pca_db = np.full(len(X_pca), -1)
    sil_pca_db = np.nan
    pct_noise_pca = 100.0
print(f"PCA ({n_pc_90} PCs) + KMeans K={K_PCA} | Sil={sil_pca_km:.4f}")
""")

# ---------------------------------------------------------------------------
# CELDA 29 — NMF
# ---------------------------------------------------------------------------
_cell(29, r"""# ====================================================================
# CELDA: NMF sobre filas mensuales — selección de componentes y clustering
# ====================================================================
# Factorización no negativa (NMF) sobre X_clima_mm (MinMax [0,1]):
#   - Barrido N=2..9: error de reconstrucción → codo para elegir N_NMF.
#   - fit_transform → espacio latente no negativo (patrones climáticos interpretables).
#   - KMeans + DBSCAN en X_nmf (análogo al bloque PCA).
# NMF asume datos ≥0; por eso se usa MinMax y no StandardScaler.

# Lista de errores de reconstrucción por número de componentes N.
nmf_errors = []
for n in range(2, 10):
    nmf_tmp = NMF(n_components=n, random_state=42, max_iter=500).fit(X_clima_mm)
    nmf_errors.append(nmf_tmp.reconstruction_err_)

# Criterio de codo simple: N donde la caída relativa del error es mínima (mayor curvatura).
drops = np.diff(nmf_errors)
N_NMF = int(np.argmin(drops) + 2) if len(drops) else 3
N_NMF = max(2, min(N_NMF, 8))

# Gráfico del error de reconstrucción vs N (línea vertical en N_NMF elegido).
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(range(2, 10), nmf_errors, "o-", color="purple")
ax.axvline(N_NMF, ls="--", color="red", label=f"N={N_NMF}")
ax.set_title("Error reconstrucción NMF")
ax.legend()
plt.tight_layout()
plt.show()

# NMF definitivo con N_NMF componentes → matriz X_nmf (filas × componentes latentes).
nmf = NMF(n_components=N_NMF, random_state=42, max_iter=500)
X_nmf = nmf.fit_transform(X_clima_mm)

# KMeans en espacio NMF.
km_nmf_df = eval_kmeans_range(X_nmf, k_range=range(2, 11))
K_NMF, _ = elegir_k(km_nmf_df)
labels_nmf_km = KMeans(n_clusters=K_NMF, random_state=42, n_init=10).fit_predict(X_nmf)
sil_nmf_km = silhouette_score(X_nmf, labels_nmf_km)

# DBSCAN en espacio NMF.
res_nmf_db = grid_dbscan(X_nmf, eps_list=[0.5, 1.0, 1.5, 2.0], ms_list=[5, 10, 15])
if len(res_nmf_db):
    best_nmf_db = res_nmf_db.iloc[0]
    labels_nmf_db = best_nmf_db["labels"].astype(int)
    sil_nmf_db = best_nmf_db["silhouette"]
    pct_noise_nmf = best_nmf_db["pct_ruido"]
else:
    labels_nmf_db = np.full(len(X_nmf), -1)
    sil_nmf_db = np.nan
    pct_noise_nmf = 100.0
print(f"NMF ({N_NMF}) + KMeans K={K_NMF} | Sil={sil_nmf_km:.4f}")
""")

# ---------------------------------------------------------------------------
# CELDA 31 — Tabla comparativa
# ---------------------------------------------------------------------------
_cell(31, r"""# ====================================================================
# CELDA: Tabla comparativa de métricas — todos los métodos y configuraciones
# ====================================================================
# Consolida Silhouette, Davies-Bouldin, % ruido DBSCAN e interpretabilidad
# para 9 configuraciones: 3 métodos × perfiles + 3 mensuales + 3 con reducción.
# Columnas: configuracion, unidad (perfil/mensual), metodo, reduccion (PCA/NMF/Ninguna).
# Output consola: tabla impresa + recomendado (mejor Silhouette en perfiles Alta).
# Este DataFrame se exporta luego como clustering_metricas.csv.

metricas = pd.DataFrame([
    {"configuracion": f"Perfil KMeans K={K_PERFIL}", "unidad": "perfil", "metodo": "KMeans",
     "reduccion": "Ninguna", "silhouette": sil_perfil_km, "davies_bouldin": db_perfil_km,
     "pct_ruido": 0.0, "interpretabilidad": "Alta"},
    {"configuracion": f"Perfil Jerárquico K={K_PERFIL}", "unidad": "perfil", "metodo": "Jerárquico",
     "reduccion": "Ninguna", "silhouette": sil_perfil_hc, "davies_bouldin": davies_bouldin_score(X_perfil, labels_perfil_hc),
     "pct_ruido": 0.0, "interpretabilidad": "Alta"},
    {"configuracion": "Perfil DBSCAN", "unidad": "perfil", "metodo": "DBSCAN",
     "reduccion": "Ninguna", "silhouette": sil_perfil_db, "davies_bouldin": np.nan,
     "pct_ruido": pct_noise_p if len(res_db_perfil) else 100.0, "interpretabilidad": "Alta"},
    {"configuracion": f"Mensual KMeans K={K_MENSUAL}", "unidad": "mensual", "metodo": "KMeans",
     "reduccion": "Ninguna", "silhouette": sil_mensual_km, "davies_bouldin": db_mensual_km,
     "pct_ruido": 0.0, "interpretabilidad": "Baja"},
    {"configuracion": "Mensual DBSCAN", "unidad": "mensual", "metodo": "DBSCAN",
     "reduccion": "Ninguna", "silhouette": sil_mensual_db, "davies_bouldin": np.nan,
     "pct_ruido": pct_noise_m, "interpretabilidad": "Baja"},
    {"configuracion": f"PCA+KMeans K={K_PCA}", "unidad": "mensual", "metodo": "KMeans",
     "reduccion": "PCA", "silhouette": sil_pca_km, "davies_bouldin": np.nan,
     "pct_ruido": 0.0, "interpretabilidad": "Media"},
    {"configuracion": "PCA+DBSCAN", "unidad": "mensual", "metodo": "DBSCAN",
     "reduccion": "PCA", "silhouette": sil_pca_db, "davies_bouldin": np.nan,
     "pct_ruido": pct_noise_pca, "interpretabilidad": "Media"},
    {"configuracion": f"NMF+KMeans K={K_NMF}", "unidad": "mensual", "metodo": "KMeans",
     "reduccion": "NMF", "silhouette": sil_nmf_km, "davies_bouldin": np.nan,
     "pct_ruido": 0.0, "interpretabilidad": "Media"},
    {"configuracion": "NMF+DBSCAN", "unidad": "mensual", "metodo": "DBSCAN",
     "reduccion": "NMF", "silhouette": sil_nmf_db, "davies_bouldin": np.nan,
     "pct_ruido": pct_noise_nmf, "interpretabilidad": "Media"},
])

# Redondeo de métricas numéricas para legibilidad en consola y CSV.
metricas[["silhouette", "davies_bouldin", "pct_ruido"]] = metricas[
    ["silhouette", "davies_bouldin", "pct_ruido"]
].round(4)
print(metricas.to_string(index=False))

# Recomendación para el informe: mejor Silhouette entre métodos de unidad=perfil (Alta interpretabilidad).
cand = metricas[(metricas["unidad"] == "perfil") & metricas["silhouette"].notna()]
recomendado = cand.loc[cand["silhouette"].idxmax(), "configuracion"]
print(f"\nRecomendado para el paper: {recomendado}")
""")

# ---------------------------------------------------------------------------
# CELDA 33 — Gráfico comparativo
# ---------------------------------------------------------------------------
_cell(33, r"""# ====================================================================
# CELDA: Gráfico comparativo comparativa_clustering.png
# ====================================================================
# Visualiza lado a lado Silhouette y % ruido DBSCAN para las 9 configuraciones.
# Azul (#2196F3) = métodos sobre perfiles (unidad principal); gris = mensuales.
# Output: OUTPUTS/figures/comparativa_clustering.png
# Permite defender en el paper por qué KMeans perfiles supera DBSCAN mensual.

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Etiquetas abreviadas en eje X (salto de línea tras la primera palabra).
short = metricas["configuracion"].str.replace(" ", "\n", n=1)
colors = ["#2196F3" if u == "perfil" else "#9E9E9E" for u in metricas["unidad"]]

# Panel izquierdo: Silhouette — mayor barra = mejor cohesión/separación.
axes[0].bar(range(len(metricas)), metricas["silhouette"], color=colors)
axes[0].set_xticks(range(len(metricas)))
axes[0].set_xticklabels(short, fontsize=7, rotation=45, ha="right")
axes[0].set_title("Silhouette (mayor = mejor)")

# Panel derecho: % ruido DBSCAN — barras altas indican método poco usable (muchos -1).
axes[1].bar(range(len(metricas)), metricas["pct_ruido"], color=colors)
axes[1].set_xticks(range(len(metricas)))
axes[1].set_xticklabels(short, fontsize=7, rotation=45, ha="right")
axes[1].set_title("% ruido DBSCAN")

plt.suptitle("Comparativa perfiles vs mensual", fontweight="bold")
plt.tight_layout()
plt.savefig(RUTA_FIG / "comparativa_clustering.png", dpi=150, bbox_inches="tight")
plt.show()
""")

# ---------------------------------------------------------------------------
# CELDA 35 — Exportación CSV
# ---------------------------------------------------------------------------
_cell(35, r"""# ====================================================================
# CELDA: Exportación de resultados a CSV en OUTPUTS/
# ====================================================================
# Persiste dos artefactos reutilizables fuera del notebook:
#   - clustering_perfiles.csv: tabla_perfil (asignaciones por región×cultivo).
#   - clustering_metricas.csv: DataFrame metricas (comparativa de 9 métodos).
# encoding utf-8-sig para compatibilidad con Excel en Windows.

export_perfil = tabla_perfil.copy()
export_perfil.to_csv(RUTA_OUT / "clustering_perfiles.csv", index=False, encoding="utf-8-sig")
metricas.to_csv(RUTA_OUT / "clustering_metricas.csv", index=False, encoding="utf-8-sig")

print("Exportado:")
print(f"  {RUTA_OUT / 'clustering_perfiles.csv'}")
print(f"  {RUTA_OUT / 'clustering_metricas.csv'}")
""")

# ---------------------------------------------------------------------------
# CELDA 37 — Conclusiones
# ---------------------------------------------------------------------------
_cell(37, r"""# ====================================================================
# CELDA: Conclusiones impresas — síntesis para defensa e informe
# ====================================================================
# Resume en consola el método recomendado, composición de clusters KMeans,
# y hallazgos/limitaciones metodológicas del notebook 06.
# No genera archivos; cierra el pipeline de tipologías agroclimáticas.

print("=" * 60)
print("CONCLUSIONES")
print("=" * 60)
print(f"Método recomendado: {recomendado}")
print(f"Perfiles analizados: {len(df_perfil)} combinaciones (región, cultivo)")
print()

# Listado de cultivos y pisos por cluster KMeans (truncado si la lista es muy larga).
for c in sorted(df_perfil["cluster_kmeans"].unique()):
    sub = df_perfil[df_perfil["cluster_kmeans"] == c]
    cultivos = ", ".join(sub["region"] + "-" + sub["cultivo"])
    pisos = ", ".join(sorted(sub["piso_ecologico"].unique()))
    print(f"Cluster KMeans {c} ({len(sub)} cultivos):")
    print(f"  Cultivos: {cultivos[:200]}{'...' if len(cultivos)>200 else ''}")
    print(f"  Pisos: {pisos}")
    print()

print("Hallazgos:")
print("- El clustering por PERFIL agrupa cultivos con condiciones agroclimáticas similares.")
print("- El análisis MENSUAL infla Silhouette por 72 réplicas por cultivo; usar solo como complemento.")
print("- No se imputaron NaN de producción; coeficientes usan solo meses con dato real.")
print("- Limitación: 30 unidades — correlación no implica causalidad clima→producción.")
""")


def strip_comments(source: str) -> str:
    """Elimina líneas que son solo comentarios para verificar código ejecutable."""
    code_lines = []
    for line in source.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        code_lines.append(line)
    return "\n".join(code_lines)


def apply() -> None:
    if not NB_PATH.exists():
        raise FileNotFoundError(f"No se encontró el notebook: {NB_PATH}")

    nb = json.loads(NB_PATH.read_text(encoding="utf-8"))
    code_indices = [i for i, c in enumerate(nb["cells"]) if c["cell_type"] == "code"]

    if set(COMMENTED_SOURCES.keys()) != set(code_indices):
        missing = set(code_indices) - set(COMMENTED_SOURCES.keys())
        extra = set(COMMENTED_SOURCES.keys()) - set(code_indices)
        raise ValueError(
            f"Desajuste de celdas. Faltan: {sorted(missing)}. Sobran: {sorted(extra)}. "
            f"Esperadas: {sorted(code_indices)}"
        )

    updated = 0
    for idx in code_indices:
        nb["cells"][idx]["source"] = COMMENTED_SOURCES[idx].splitlines(keepends=True)
        updated += 1

    NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK {NB_PATH.name}: {updated} celdas de código actualizadas con comentarios extensivos")
    print(f"   Ruta: {NB_PATH}")


if __name__ == "__main__":
    apply()

