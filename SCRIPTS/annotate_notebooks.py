# -*- coding: utf-8 -*-
"""Inserta celdas markdown explicativas en notebooks 01-06."""
import json
import uuid
from pathlib import Path

NOTEBOOKS = Path(__file__).resolve().parent / "notebooks"


def md_cell(text: str) -> dict:
    return {
        "id": uuid.uuid4().hex[:8],
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
    }


def has_marker(cell, marker: str) -> bool:
    if cell["cell_type"] != "markdown":
        return False
    return marker in "".join(cell.get("source", []))


def append_md(cell: dict, text: str) -> None:
    src = cell.get("source", [])
    if src and not src[-1].endswith("\n"):
        src[-1] += "\n"
    src.append("\n")
    src.extend(text.splitlines(keepends=True))
    cell["source"] = src


# ---------------------------------------------------------------------------
# Notebook 04 — EDA regional (interpretaciones largas de gráficos)
# ---------------------------------------------------------------------------
NB04_BEFORE = {
    1: (
        "### Qué hace esta celda\n\n"
        "Configura el entorno: resuelve la ruta raíz del repositorio, crea `OUTPUTS/figures/`, "
        "carga `dataset_regional.csv` (1.008 filas = 14 unidades × 72 meses) y define constantes "
        "(`CLIMA_EDA`, orden de meses). Crea la columna `unidad` = región | piso | distrito y "
        "`fecha` para series temporales. Imprime dimensiones y conteo de NaN en producción."
    ),
}

NB04_SECTION_BEFORE = {
    3: (
        "### Qué hace esta celda\n\n"
        "Agrupa con `sum(min_count=1)` la producción de todos los cultivos Pareto-80 por "
        "unidad territorial (14 combinaciones región×piso×distrito) en el periodo 2020–2025. "
        "Calcula el porcentaje sobre el total nacional del subconjunto y genera un gráfico de "
        "barras horizontal guardado en `eda_regional_volumen_unidad.png`."
    ),
    5: (
        "### Qué hace esta celda\n\n"
        "Construye dos paneles: (arriba) producción **anual** por cada una de las 14 unidades; "
        "(abajo) producción **mensual** sumando todos los pisos dentro de cada región. "
        "Guarda `eda_regional_produccion_anual.png`."
    ),
    7: (
        "### Qué hace esta celda\n\n"
        "Para cada una de las 6 regiones, arma una tabla mes×año con la producción agregada "
        "y la visualiza como heatmap (`YlOrRd`). Permite ver en qué meses y años hubo picos o "
        "caídas de cosecha. Guarda `eda_regional_heatmap_estacionalidad.png`."
    ),
    9: (
        "### Qué hace esta celda\n\n"
        "Promedia la producción de cada mes del calendario a través de todos los años "
        "(enero–diciembre) por unidad. Obtiene el **calendario agrícola típico** de cada piso. "
        "Guarda `eda_regional_patron_estacional.png`."
    ),
    11: (
        "### Qué hace esta celda\n\n"
        "Calcula medias 2020–2025 de las 5 variables climáticas core por unidad (panel de barras) "
        "y un boxplot de temperatura mensual por región y piso. Guarda "
        "`eda_regional_perfil_climatico.png` y `eda_regional_boxplot_temp.png`."
    ),
    13: (
        "### Qué hace esta celda\n\n"
        "Calcula correlación de Pearson entre producción mensual y cada variable climática **dentro** "
        "de cada unidad (mínimo 12 meses válidos). Exporta `eda_correlaciones_regional.csv` e "
        "imprime el top-5 de |r| y un pooling agregado (todas las unidades juntas). "
        "**No implica causalidad** ni corrección por comparaciones múltiples."
    ),
    15: (
        "### Qué hace esta celda\n\n"
        "Filtra Puno, agrega producción anual y humedad de suelo media por unidad, calcula el "
        "% de cambio 2021→2022 y grafica en ejes duales producción vs humedad radicular. "
        "Guarda `eda_regional_puno_sequia.png`."
    ),
    17: (
        "### Qué hace esta celda\n\n"
        "Compara precipitación y temperatura en Piura, La Libertad e Ica entre la referencia "
        "2020–2022 y los años 2023–2024 (ventana El Niño costero). Grafica series mensuales de "
        "precipitación y producción con sombreado 2023–2024. Guarda `eda_regional_nino_costa.png`."
    ),
    19: (
        "### Qué hace esta celda\n\n"
        "Audita NaN en columnas climáticas y producción; imprime un resumen cuantitativo del "
        "Análisis A (filas, unidades, figuras generadas). Cierra el notebook con enlace a 05 y 06."
    ),
}

NB04_AFTER = {
    3: (
        "### Interpretación — volumen por unidad (`eda_regional_volumen_unidad.png`)\n\n"
        "Este gráfico responde: **¿dónde se concentra el volumen productivo del subconjunto Pareto-80?**\n\n"
        "- Cada barra es una **unidad territorial** (región + piso ecológico + distrito NASA), no una región administrativa completa.\n"
        "- Las unidades con barras más largas (típicamente **costa de La Libertad — Virú**, **Ica — Chincha**, **selva de San Martín o Junín**) "
        "dominan el volumen porque albergan cultivos de alto tonelaje (caña, arroz, palta, espárrago, etc.).\n"
        "- Los pisos de **altiplano (Puno)** suelen aparecer con barras menores en toneladas absolutas, pero no son menos relevantes agronómicamente: "
        "reflejan escala de cultivos andinos y filtro Pareto, no \"menor importancia\".\n"
        "- El `% del total` en la tabla impresa cuantifica la concentración: pocas unidades explican gran parte del volumen del análisis.\n\n"
        "**Lectura honesta:** estamos sumando **toneladas**, no rendimiento (t/ha). Una barra grande puede deberse a extensión sembrada "
        "o a cultivos industrializados, no necesariamente a mayor productividad por hectárea."
    ),
    5: (
        "### Interpretación — series temporales (`eda_regional_produccion_anual.png`)\n\n"
        "**Panel superior (anual por unidad):**\n"
        "- Cada línea = una de las 14 unidades. Permite ver tendencias interanuales y comparar pisos dentro de la misma región "
        "(ej. Junín tiene selva alta, selva baja y sierra con trayectorias distintas).\n"
        "- Caídas marcadas en **Puno 2022** son compatibles con la sequía altiplánica documentada en el paper; "
        "subidas en años favorables reflejan recuperación o años hidrológicamente mejores.\n"
        "- Picos aislados pueden deberse a meses MIDAGRI imputados como NaN en el agregado (`min_count=1` evita falsos ceros).\n\n"
        "**Panel inferior (mensual por región):**\n"
        "- Suma todos los pisos de cada región → visión macro de estacionalidad y shocks.\n"
        "- La **estacionalidad** se ve como oscilaciones repetidas cada año; desviaciones sostenidas en 2022–2023 en sur andino "
        "o anomalías en costa 2023–2024 enlazan con los casos de estudio posteriores.\n\n"
        "**No interpretar como:** efecto causal del clima mes a mes; es co-movimiento temporal producción agregada."
    ),
    7: (
        "### Interpretación — heatmaps estacionalidad (`eda_regional_heatmap_estacionalidad.png`)\n\n"
        "Cada subpanel es una **región**; filas = meses, columnas = años; color = toneladas producidas ese mes.\n\n"
        "- **Celdas más intensas (rojo):** meses de mayor cosecha agregada en esa región (calendario productivo principal).\n"
        "- **Costa norte (Piura, La Libertad, Ica):** a menudo patrones más continuos o concentrados en campañas de riego/verano según cultivo dominante.\n"
        "- **Sierra y altiplano (Puno, pisos de Junín/La Libertad):** estacionalidad más marcada; celdas pálidas en invierno seco andino.\n"
        "- **Selva (San Martín, Junín baja):** puede mostrar producción más distribuida o picos ligados a ciclos de cultivos perennes/transitorios del Pareto.\n"
        "- **Celdas vacías o muy claras:** mes sin producción reportada (NaN en origen) o mes fuera de ventana de cosecha.\n"
        "- Comparar **2022 vs años vecinos** en Puno/Junín sierra ayuda a visualizar el evento de sequía sin calcular elasticidades.\n\n"
        "Este gráfico sustenta en el paper la \"caracterización de patrones de estacionalidad\" a nivel regional agregado."
    ),
    9: (
        "### Interpretación — patrón estacional promedio (`eda_regional_patron_estacional.png`)\n\n"
        "Promedia todos los años → curva **típica** mes a mes por unidad (suaviza shocks como 2022).\n\n"
        "- **Picos de curva:** meses de cosecha habitual (ej. verano costero, post-lluvias en sierra).\n"
        "- **Valles:** meses sin cosecha o con producción marginal.\n"
        "- Unidades de la misma región pero distinto piso (ej. La Libertad: costa vs sierra vs yunga) deben mostrar curvas **desfasadas o de distinta amplitud**, "
        "validando el enfoque multi-distrito del proyecto frente a un solo punto climático por departamento.\n"
        "- Si dos unidades tienen curvas casi idénticas en producción pero climas distintos, recuerda que aquí la producción está **sumada por cultivo Pareto** "
        "y el clima no entra aún en este gráfico.\n\n"
        "Útil para la defensa: explica \"cuándo se cosecha\" antes de hablar de correlaciones clima–producción."
    ),
    11: (
        "### Interpretación — perfil climático (`eda_regional_perfil_climatico.png`, `eda_regional_boxplot_temp.png`)\n\n"
        "**Panel de barras (5 variables):**\n"
        "- Resume el **clima promedio 2020–2025** del punto NASA de cada distrito.\n"
        "- `temp_promedio`: gradiente costa cálida → altiplano frío (Puno/Ayaviri, Ilave más bajos).\n"
        "- `precipitacion`: contraste costa árida (Ica, Virú) vs sierra/selva húmeda (Canchaque, Moyobamba, Perené).\n"
        "- `humedad_suelo` / `humedad_relativa`: indicadores de estrés hídrico; valores bajos sostenidos en costa y puna.\n"
        "- `radiacion_solar`: alta en costa despejada; modulada en selva nublada.\n\n"
        "**Boxplot de temperatura:**\n"
        "- Muestra **variabilidad mensual** (no solo la media): amplitud térmica intra-anual por piso.\n"
        "- Pisos de sierra y altiplano suelen tener cajas más bajas y a veces mayor dispersión estacional.\n\n"
        "**Limitación:** un solo punto por distrito; no captura microclima dentro del valle o la cuenca."
    ),
    13: (
        "### Interpretación — correlaciones Pearson (tablas y CSV)\n\n"
        "Cada fila del CSV = una unidad × una variable climática; `r` mide asociación lineal mensual.\n\n"
        "- **|r| alto** (ej. > 0,6): meses con más producción tienden a coincidir con meses con valores altos/bajos de esa variable "
        "en esa unidad — **no** demuestra que el clima \"cause\" la cosecha (confusión por estacionalidad compartida).\n"
        "- **Signo de r:** positivo = ambas suben juntas; negativo = una sube cuando la otra baja.\n"
        "- El **pooling agregado** (todas las unidades mezcladas) mezcla climas muy distintos; un r global (ej. temperatura) "
        "puede ser débil o engañoso. Prioriza siempre el análisis **por unidad** o el notebook 05 por cultivo.\n"
        "- Sin corrección Benjamini–Hochberg: con 14×5 = 70 contrastes, algunos p_valor < 0,05 pueden ser falsos positivos.\n\n"
        "En el paper se menciona temperatura como variable influyente a nivel agregado; verifica que la cifra citada "
        "corresponda al mismo nivel de agregación y periodo que esta tabla."
    ),
    15: (
        "### Interpretación — sequía Puno (`eda_regional_puno_sequia.png`)\n\n"
        "- **Líneas sólidas (eje izquierdo):** producción anual agregada en Ilave y Ayaviri (altiplano).\n"
        "- **Líneas punteadas (eje derecho):** humedad de zona radicular (`humedad_suelo`, índice 0–1 de NASA POWER).\n"
        "- Una **caída fuerte 2021→2022** en producción junto a humedad de suelo baja o estancada es **evidencia descriptiva** "
        "coherente con sequía altiplánica; no sustituye un estudio causal con rendimiento (t/ha) ni control de área sembrada.\n"
        "- La tabla impresa de `% cambio` cuantifica la magnitud para cada unidad (cultivos andinos agregados en Pareto).\n"
        "- Si una unidad recupera en 2023–2024, puede reflejar año hidrológico menos severo, no necesariamente política o tecnología.\n\n"
        "Para el detalle por cultivo (quinua, papa, etc.) ver `05_eda_por_cultivo.ipynb`."
    ),
    17: (
        "### Interpretación — El Niño costero (`eda_regional_nino_costa.png`)\n\n"
        "- **Panel izquierdo:** precipitación mensual media en Piura, La Libertad e Ica; zona sombreada = 2023–2024.\n"
        "- Durante episodios El Niño costero suele observarse **precipitación anómala** (aumento en norte, posible estrés en cultivos sensibles a exceso hídrico o calor).\n"
        "- **Panel derecho:** producción mensual agregada en las mismas regiones; busca desfases (el impacto productivo puede aparecer meses después del pico pluvial).\n"
        "- La tabla impresa compara medias 2020–2022 vs 2023–2024 por región y año.\n\n"
        "**Cautela:** El Niño afecta de forma heterogénea por cultivo (arroz vs uva vs caña); este gráfico es regional agregado. "
        "No atribuir al clima sin desagregar."
    ),
    19: (
        "### Cierre del Análisis A\n\n"
        "Con estos nueve bloques se cubren los objetivos regionales del paper: volumen, estacionalidad, clima, asociaciones exploratorias "
        "y dos eventos extremos. El siguiente paso lógico es **desagregar por cultivo** (`05`) y luego **tipologías** (`06`)."
    ),
}

# ---------------------------------------------------------------------------
# Notebook 05
# ---------------------------------------------------------------------------
NB05_BEFORE = {
    1: (
        "### Qué hace esta celda\n\n"
        "Setup: carga `dataset_integrado.csv` (granularidad cultivo×mes), define rutas y variables climáticas "
        "para el Análisis B (correlaciones por par región–cultivo)."
    ),
    2: (
        "### Qué hace esta celda\n\n"
        "Bucle sobre cada par `(región, cultivo)` del Pareto-80: calcula Pearson entre `produccion_ton` "
        "y cada variable en `CLIMA_EDA` (≥12 meses válidos). Exporta `eda_correlaciones_por_cultivo.csv` "
        "e imprime el top-5 de |r|."
    ),
    3: (
        "### Qué hace esta celda\n\n"
        "Caso Puno: serie anual de producción por cultivo Pareto; gráfico de líneas guardado en "
        "`eda_puno_produccion_anual.png`."
    ),
}

NB05_AFTER = {
    2: (
        "### Interpretación — correlaciones por cultivo\n\n"
        "Cada fila = un cultivo en una región × variable climática.\n\n"
        "- Cultivos del **mismo piso comparten clima idéntico** → correlaciones distintas entre cultivos en la misma región "
        "reflejan sobre todo **patrones de cosecha diferentes**, no sensibilidades climáticas independientes.\n"
        "- Top |r| elevados (ej. radiación en cítricos de Ica) deben leerse como **hipótesis exploratorias** para validación agronómica.\n"
        "- Comparar con `eda_correlaciones_regional.csv` del notebook 04: allí la unidad es el piso agregado; aquí el cultivo."
    ),
    3: (
        "### Interpretación — Puno por cultivo (`eda_puno_produccion_anual.png`)\n\n"
        "- Una línea por cultivo Pareto en Puno (papa, quinua, alfalfa, etc.).\n"
        "- Caídas pronunciadas en **2022** en cultivos andinos son el sustento cuantitativo del caso sequía del paper "
        "(ej. quinua, oca, papa según cifras del informe).\n"
        "- Cultivos forrajeros o de menor sensibilidad hídrica pueden mostrar caídas menores → heterogeneidad intra-regional.\n"
        "- Sin área cosechada no distinguimos si la caída es por menor rendimiento o menor superficie."
    ),
}

# ---------------------------------------------------------------------------
# Notebook 01 — textos por índice de celda código
# ---------------------------------------------------------------------------
NB01_BEFORE = {
    1: "Importa librerías (`pandas`, `numpy`, `pathlib`) y configura opciones de visualización.",
    3: "Define `ROOT`, rutas a `BDS/` y `OUTPUTS/`, años 2020–2025 y las 6 regiones objetivo.",
    5: "Define funciones de normalización de nombres de cultivos y regiones (quita tildes, unifica variantes).",
    7: "Implementa `descubrir_archivos`: escanea carpetas anuales y reporta meses presentes/faltantes en Excel c-18.",
    9: "Implementa `cargar_archivo`: lee hoja c-18, detecta header, limpia bloques duplicados y filtra por año del archivo.",
    11: "Implementa `recuperar_dic_2020`: extrae diciembre 2020 desde el Excel de diciembre 2021 (fila de total anual 2020).",
    13: "Construye grid completo región×año×mes e inserta NaN donde MIDAGRI no publicó boletín (evita diff inflado).",
    15: "Aplica `diff()` por región y año para obtener producción mensual real; enero conserva acumulado; negativos → NaN.",
    17: "Diagnóstico de variantes de nombres de cultivos en archivos crudos (antes del mapeo canónico).",
    19: "Convierte de formato ancho (columnas=cultivos) a largo (`region`, `cultivo`, `mes`, `produccion_mensual`).",
    20: "Segundo diagnóstico de variantes post-melt para detectar cultivos no mapeados.",
    22: "Exporta `OUTPUTS/midagri_largo.csv` — insumo principal del notebook 03.",
    23: "Auditoría final: filas, regiones, cultivos únicos y conteo de NaN.",
}

# ---------------------------------------------------------------------------
# Notebook 02
# ---------------------------------------------------------------------------
NB02_BEFORE = {
    1: "Importa librerías y define parámetros NASA POWER (12 variables) y coordenadas de los 14 distritos.",
    3: "Tabla de coordenadas finales por región/distrito/piso (acordadas en el paper).",
    5: "Función `descargar_nasa` con reintentos y pausa entre llamadas a la API.",
    7: "Bucle de descarga para los 14 distritos (o lectura de cache si el CSV ya existe).",
    9: "Limpieza: elimina fila resumen anual (mes 13), convierte -999 a NaN, renombra columnas.",
    11: "Validación: 72 filas por distrito (6 años × 12 meses), rangos plausibles de variables.",
    14: "Ejemplo visual de interpolación lineal en radiación solar para un distrito.",
    15: "Interpola NaN restantes en variables climáticas (política del pipeline NASA).",
    17: "Exporta `OUTPUTS/nasa_2020_2025.csv`.",
}

# ---------------------------------------------------------------------------
# Notebook 03
# ---------------------------------------------------------------------------
NB03_BEFORE = {
    1: "Setup: rutas, imports y constantes del merge MIDAGRI + NASA + mapping v2.",
    3: "Verifica que existan `midagri_largo.csv`, `nasa_2020_2025.csv` y el mapping v2 antes de integrar.",
    5: "Vista previa de dimensiones y columnas de los tres insumos.",
    7: "Funciones de integración inline: Pareto-80 por región, merge por distrito, agregados regional y por cultivo, exportación.",
    9: "Lee `dataset_integrado.csv` generado y resume filas, combos Pareto y NaN intencionales.",
}

NB03_AFTER = {
    7: (
        "### Qué produce esta celda\n\n"
        "Genera tres CSV en `OUTPUTS/`:\n"
        "- `dataset_integrado.csv` — tabla maestra (cultivo×mes)\n"
        "- `dataset_regional.csv` — Análisis A (piso×mes)\n"
        "- `dataset_por_cultivo.csv` — series por cultivo Pareto\n\n"
        "Aplica `sum(min_count=1)` en agregados para no convertir meses 100% NaN en cero."
    ),
}

# ---------------------------------------------------------------------------
# Notebook 06 — índices de celdas código (del dump)
# ---------------------------------------------------------------------------
NB06_BEFORE = {
    2: "Importa sklearn, scipy, matplotlib y utilidades para clustering, PCA, NMF y métricas.",
    4: "Carga `dataset_integrado.csv`, crea carpetas de salida y muestra dimensiones.",
    5: "Lista regiones, pisos, cultivos y define `CLIMA_VARS` / `CLIMA_CORE`.",
    7: "Define funciones: `eval_kmeans_range`, `elegir_k`, `grid_dbscan`, `plot_k_selection`, etc.",
    9: "Agrega perfiles (región×cultivo): medias/std climáticas, producción total, CV; estandariza features.",
    10: "Sweep K=2–7 con KMeans sobre perfiles; elige K por Silhouette/Davies–Bouldin; gráfico `seleccion_k_perfiles.png`.",
    11: "Dendrograma Ward + clustering jerárquico con el mismo K; guarda `dendrograma_perfiles.png`.",
    12: "Grid DBSCAN sobre perfiles; reporta % ruido (suele ser alto → método complementario).",
    14: "Tabla de asignaciones, crosstab por región y heatmap de centroides → `heatmap_perfiles_kmeans.png`.",
    15: "Impresión narrativa de composición climática-productiva por cluster KMeans.",
    17: "Prepara matriz mensual solo clima (análisis complementario, 2.376 filas).",
    19: "KMeans y DBSCAN sobre filas mensuales (limitación: clima repetido por cultivo).",
    21: "PCA: varianza explicada, loadings PC1–PC2, clustering en espacio reducido.",
    23: "NMF: selección de componentes por codo, clustering en espacio NMF.",
    25: "Tabla comparativa de métricas (Silhouette, DB, % ruido) para todos los métodos.",
    26: "Gráfico comparativo `comparativa_clustering.png`.",
    27: "Exporta `clustering_perfiles.csv` y `clustering_metricas.csv`.",
    29: "Imprime conclusiones y método recomendado (KMeans K=6 sobre perfiles).",
}

NB06_AFTER = {
    10: (
        "### Interpretación — selección de K (`seleccion_k_perfiles.png`)\n\n"
        "Muestra Silhouette y Davies–Bouldin para K=2…7 sobre **33 perfiles**. "
        "El K elegido balancea separación de clusters e interpretabilidad agronómica (K=6 en la versión actual). "
        "Un K muy alto fragmenta cultivos similares; uno muy bajo mezcla costa y selva."
    ),
    11: (
        "### Interpretación — dendrograma (`dendrograma_perfiles.png`)\n\n"
        "Árbol jerárquico Ward: cultivos que se fusionan a baja altura son perfiles similares en el espacio "
        "clima+producción estandarizado. Útil para validar si KMeans respeta estructura natural (costa, selva, altiplano)."
    ),
    14: (
        "### Interpretación — heatmap perfiles (`heatmap_perfiles_kmeans.png`)\n\n"
        "Filas = clusters KMeans; columnas = variables (medias climáticas y producción). "
        "Permite nombrar clusters: ej. alto volumen costero, selva húmeda, altiplano frío, outlier caña La Libertad."
    ),
    21: (
        "### Interpretación — PCA mensual\n\n"
        "Muestra cuánta varianza climática capturan PC1–PC2 y qué variables cargan en cada componente. "
        "Análisis **complementario** con repetición temporal; no es el resultado principal del informe."
    ),
    26: (
        "### Interpretación — comparativa (`comparativa_clustering.png`)\n\n"
        "Compara Silhouette y % ruido entre métodos. DBSCAN puede tener Silhouette alto pero >60% ruido → "
        "descartado como método principal. KMeans/Jerárquico sobre perfiles es la recomendación defendible."
    ),
}


def wrap_before(text: str) -> str:
    if text.startswith("###"):
        return text
    return f"### Qué hace esta celda\n\n{text}"


def annotate(nb_path: Path, before_map: dict, after_map: dict | None = None) -> int:
    after_map = after_map or {}
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    new_cells = []
    n_added = 0

    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "code":
            # Texto "before": anexar al markdown previo o insertar celda nueva
            if i in before_map and not (
                new_cells and has_marker(new_cells[-1], "### Qué hace esta celda")
            ):
                text = wrap_before(before_map[i])
                if new_cells and new_cells[-1]["cell_type"] == "markdown":
                    if not has_marker(new_cells[-1], "### Qué hace esta celda"):
                        append_md(new_cells[-1], text)
                        n_added += 1
                else:
                    new_cells.append(md_cell(text))
                    n_added += 1

        new_cells.append(cell)

        if cell["cell_type"] == "code" and i in after_map:
            if not (new_cells and has_marker(new_cells[-1], "### Interpretación")):
                new_cells.append(md_cell(after_map[i]))
                n_added += 1

    nb["cells"] = new_cells
    nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return n_added


def main():
    jobs = [
        (NOTEBOOKS / "04_eda_regional.ipynb", {**NB04_BEFORE, **NB04_SECTION_BEFORE}, NB04_AFTER),
        (NOTEBOOKS / "05_eda_por_cultivo.ipynb", NB05_BEFORE, NB05_AFTER),
        (NOTEBOOKS / "01_midagri_pipeline.ipynb", {k: wrap_before(v) for k, v in NB01_BEFORE.items()}, None),
        (NOTEBOOKS / "02_nasa_pipeline.ipynb", {k: wrap_before(v) for k, v in NB02_BEFORE.items()}, None),
        (NOTEBOOKS / "03_build_dataset_integrado.ipynb", {k: wrap_before(v) for k, v in NB03_BEFORE.items()}, NB03_AFTER),
        (NOTEBOOKS / "06_clustering_cultivos.ipynb", {k: wrap_before(v) for k, v in NB06_BEFORE.items()}, NB06_AFTER),
    ]
    for path, before, after in jobs:
        if not path.exists():
            print("SKIP (no existe):", path.name)
            continue
        n = annotate(path, before, after)
        print(f"OK {path.name}: +{n} bloques markdown")


if __name__ == "__main__":
    main()
