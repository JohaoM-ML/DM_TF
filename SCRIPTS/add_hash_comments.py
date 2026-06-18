# -*- coding: utf-8 -*-
"""Inserta comentarios # en celdas de código de notebooks 01-06."""
import json
import re
import uuid
from pathlib import Path

NOTEBOOKS = Path(__file__).resolve().parent / "notebooks"

# Título de cabecera por (notebook, índice de celda)
TITLES: dict[tuple[str, int], str] = {
    # --- 01 MIDAGRI ---
    ("01_midagri_pipeline.ipynb", 1): "Importaciones y configuración de pandas",
    ("01_midagri_pipeline.ipynb", 3): "Rutas BDS/OUTPUTS, años y regiones objetivo",
    ("01_midagri_pipeline.ipynb", 5): "Funciones de normalización de nombres",
    ("01_midagri_pipeline.ipynb", 7): "Descubrimiento de archivos Excel c-18",
    ("01_midagri_pipeline.ipynb", 9): "Carga y limpieza de cada archivo MIDAGRI",
    ("01_midagri_pipeline.ipynb", 11): "Recuperación de diciembre 2020 desde dic-2021",
    ("01_midagri_pipeline.ipynb", 13): "Grid completo región×año×mes con NaN explícitos",
    ("01_midagri_pipeline.ipynb", 15): "Producción mensual real vía diff() del acumulado",
    ("01_midagri_pipeline.ipynb", 17): "Diagnóstico de variantes de nombres de cultivos",
    ("01_midagri_pipeline.ipynb", 19): "Conversión a formato largo (melt)",
    ("01_midagri_pipeline.ipynb", 21): "Diagnóstico post-melt de cultivos",
    ("01_midagri_pipeline.ipynb", 23): "Exportar midagri_largo.csv",
    ("01_midagri_pipeline.ipynb", 25): "Auditoría final del dataset MIDAGRI",
    # --- 02 NASA ---
    ("02_nasa_pipeline.ipynb", 1): "Importaciones para API NASA POWER",
    ("02_nasa_pipeline.ipynb", 3): "Coordenadas de los 14 distritos y parámetros",
    ("02_nasa_pipeline.ipynb", 5): "Función de descarga con reintentos",
    ("02_nasa_pipeline.ipynb", 7): "Descarga secuencial por distrito",
    ("02_nasa_pipeline.ipynb", 9): "Limpieza: mes 13, -999→NaN, renombrar columnas",
    ("02_nasa_pipeline.ipynb", 11): "Validación de filas y rangos por distrito",
    ("02_nasa_pipeline.ipynb", 14): "Ejemplo visual de interpolación lineal",
    ("02_nasa_pipeline.ipynb", 16): "Interpolación de NaN climáticos restantes",
    ("02_nasa_pipeline.ipynb", 18): "Exportar nasa_2020_2025.csv",
    # --- 03 Integración ---
    ("03_build_dataset_integrado.ipynb", 1): "Setup — rutas e imports",
    ("03_build_dataset_integrado.ipynb", 3): "Verificar insumos (01, 02, mapping)",
    ("03_build_dataset_integrado.ipynb", 5): "Vista previa MIDAGRI, NASA y mapping",
    ("03_build_dataset_integrado.ipynb", 7): "Merge, Pareto-80, agregados y exportación",
    ("03_build_dataset_integrado.ipynb", 10): "Resumen del dataset_integrado.csv exportado",
    # --- 04 EDA regional ---
    ("04_eda_regional.ipynb", 1): "Setup — cargar dataset_regional.csv",
    ("04_eda_regional.ipynb", 3): "§1 Volumen productivo por unidad territorial",
    ("04_eda_regional.ipynb", 5): "§2 Series temporales anual y mensual",
    ("04_eda_regional.ipynb", 7): "§3 Heatmaps estacionalidad mes×año",
    ("04_eda_regional.ipynb", 9): "§4 Patrón estacional promedio",
    ("04_eda_regional.ipynb", 11): "§5 Perfil climático por piso",
    ("04_eda_regional.ipynb", 13): "§6 Correlaciones Pearson por unidad",
    ("04_eda_regional.ipynb", 15): "§7 Caso sequía Puno 2021→2022",
    ("04_eda_regional.ipynb", 17): "§8 Caso El Niño costero 2023–2024",
    ("04_eda_regional.ipynb", 19): "§9 Auditoría NaN y resumen",
    # --- 05 EDA cultivo ---
    ("05_eda_por_cultivo.ipynb", 1): "Setup — cargar dataset_integrado.csv",
    ("05_eda_por_cultivo.ipynb", 3): "Correlaciones Pearson por (región, cultivo)",
    ("05_eda_por_cultivo.ipynb", 5): "Caso Puno — producción anual por cultivo",
    # --- 06 Clustering ---
    ("06_clustering_cultivos.ipynb", 2): "Importaciones sklearn y utilidades",
    ("06_clustering_cultivos.ipynb", 4): "Carga dataset_integrado.csv",
    ("06_clustering_cultivos.ipynb", 6): "Variables climáticas y exploración básica",
    ("06_clustering_cultivos.ipynb", 8): "Funciones auxiliares de clustering",
    ("06_clustering_cultivos.ipynb", 10): "Agregación de perfiles región×cultivo",
    ("06_clustering_cultivos.ipynb", 12): "KMeans sobre perfiles — selección de K",
    ("06_clustering_cultivos.ipynb", 14): "Clustering jerárquico y dendrograma",
    ("06_clustering_cultivos.ipynb", 16): "DBSCAN sobre perfiles",
    ("06_clustering_cultivos.ipynb", 18): "Tabla, heatmap e interpretación de clusters",
    ("06_clustering_cultivos.ipynb", 20): "Perfil narrativo por cluster KMeans",
    ("06_clustering_cultivos.ipynb", 22): "Matriz mensual solo clima (complementario)",
    ("06_clustering_cultivos.ipynb", 24): "KMeans y DBSCAN mensual",
    ("06_clustering_cultivos.ipynb", 26): "PCA sobre filas mensuales",
    ("06_clustering_cultivos.ipynb", 28): "NMF sobre filas mensuales",
    ("06_clustering_cultivos.ipynb", 30): "Tabla comparativa de métricas",
    ("06_clustering_cultivos.ipynb", 32): "Gráfico comparativa_clustering.png",
    ("06_clustering_cultivos.ipynb", 34): "Exportar CSVs de clustering",
    ("06_clustering_cultivos.ipynb", 37): "Conclusiones impresas",
}

# Reglas: (regex sobre línea stripped, comentario a insertar ANTES si no hay ya un # similar)
INLINE_RULES = [
    (r"^import |^from ", "# --- Importaciones ---"),
    (r"^ROOT = |^RUTA_", "# --- Rutas del proyecto ---"),
    (r"^df = pd\.read_csv", "# Cargar CSV principal en memoria"),
    (r"^if not .+\.exists\(\)", "# Validar que el insumo exista antes de continuar"),
    (r"^CLIMA_|^MESES_|^COLS_|^PARAMETROS|^ANIOS|^REGIONES", "# Constantes del análisis"),
    (r"^def ", None),  # manejado aparte
    (r"^vol_unidad|^prod_anual|^patron|^clima_mean", "# Agregación con groupby (sum/min_count=1 o mean)"),
    (r"^rows = \[\]", "# Acumulador para resultados fila a fila"),
    (r"^for .+ in df\.groupby", "# Bucle por grupos del dataframe"),
    (r"^for .+ in .+\.groupby", "# Bucle por subgrupos"),
    (r"^corr_", "# DataFrame de correlaciones"),
    (r"^fig, ax", "# Crear figura matplotlib"),
    (r"^fig, axes", "# Crear figura con subplots"),
    (r"^sns\.(barplot|heatmap|boxplot)", "# Gráfico seaborn"),
    (r"^ax\.set_title|^axes\[", "# Etiquetas del gráfico"),
    (r"fig\.savefig", "# Guardar PNG en OUTPUTS/figures/"),
    (r"^plt\.show", "# Mostrar gráfico en el notebook"),
    (r"\.to_csv\(", "# Exportar resultado a CSV"),
    (r"^print\(", "# Salida informativa en consola"),
    (r"^puno = |^costa = ", "# Filtrar subconjunto regional para caso de estudio"),
    (r"^km_|^hc = |^Z = linkage", "# Modelo de clustering"),
    (r"^dfs = |^exportar\(|^stats = ", "# Ejecutar pipeline de integración"),
    (r"^UMBRAL_PARETO", "# Umbral Pareto-80 por región"),
    (r"^insumos = ", "# Diccionario de archivos requeridos"),
    (r"^df_largo = |^df_mensual", "# Transformación del dataframe MIDAGRI"),
    (r"^df_acumulado", "# DataFrame acumulado MIDAGRI"),
    (r"^metricas = ", "# Tabla resumen de métodos de clustering"),
    (r"^warnings\.|^plt\.rcParams|^sns\.set", "# Configuración de entorno gráfico"),
]

DEF_COMMENT = {
    "normalizar_nombre": "# Normaliza texto: minúsculas, sin tildes, guiones bajos",
    "cargar_archivo": "# Lee Excel c-18: detecta header, limpia bloques, filtra año",
    "descubrir_archivos": "# Escanea carpetas BDS/YYYY/*.xlsx y mapea (año, mes)→ruta",
    "recuperar_dic_2020": "# Extrae total anual 2020 del Excel de diciembre 2021",
    "construir_grid_completo": "# Inserta filas NaN para meses sin boletín MIDAGRI",
    "descargar_nasa": "# Llama API NASA POWER con reintentos y pausa",
    "filtrar_pareto": "# Selecciona cultivos hasta ≥80% producción regional acumulada",
    "construir_datasets": "# Merge MIDAGRI+mapping+NASA; genera 3 datasets",
    "validar": "# Comprueba coherencia agregado A vs suma B",
    "exportar": "# Escribe CSVs en OUTPUTS/",
    "renombrar_columnas": "# Renombra columnas NASA/MIDAGRI a español",
    "coef_var_positivos": "# Coeficiente de variación solo en meses con producción >0",
    "eval_kmeans_range": "# Evalúa Silhouette y Davies-Bouldin para rango de K",
    "elegir_k": "# Elige K óptimo según métricas",
    "silhouette_no_noise": "# Silhouette excluyendo puntos ruido DBSCAN",
    "pct_ruido": "# Porcentaje de puntos marcados como ruido (-1)",
}


def already_commented(source: str) -> bool:
    return "# === CELDA" in source[:200]


def header_block(title: str) -> str:
    bar = "# " + "=" * 68
    return f"{bar}\n# CELDA: {title}\n{bar}\n\n"


def comment_for_def(line: str) -> str:
    m = re.match(r"def (\w+)", line.strip())
    if m and m.group(1) in DEF_COMMENT:
        return DEF_COMMENT[m.group(1)]
    if m:
        return f"# Definición de función: {m.group(1)}()"
    return "# Definición de función"


def insert_inline_comments(source: str) -> str:
    lines = source.splitlines()
    out: list[str] = []
    seen_blocks: set[str] = set()
    prev_blank = True

    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append(line)
            prev_blank = True
            continue

        if stripped.startswith("#"):
            out.append(line)
            prev_blank = False
            continue

        inserted = False
        if stripped.startswith("def "):
            c = comment_for_def(stripped)
            if out and out[-1].strip() != c:
                out.append(c)
            inserted = True
        else:
            for pattern, comment in INLINE_RULES:
                if comment and pattern and re.match(pattern, stripped):
                    key = comment
                    if key not in seen_blocks or prev_blank:
                        if not (out and out[-1].strip() == comment):
                            out.append(comment)
                        seen_blocks.add(key)
                    inserted = True
                    break

        out.append(line)
        prev_blank = False

    return "\n".join(out) + ("\n" if source.endswith("\n") else "")


def process_notebook(nb_path: Path) -> int:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    n = 0
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell.get("source", []))
        if already_commented(src):
            continue
        title = TITLES.get((nb_path.name, i), f"Código — celda {i}")
        new_src = header_block(title) + insert_inline_comments(src)
        cell["source"] = new_src.splitlines(keepends=True)
        n += 1
    nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return n


def main():
    total = 0
    for nb_path in sorted(NOTEBOOKS.glob("*.ipynb")):
        c = process_notebook(nb_path)
        print(f"OK {nb_path.name}: {c} celdas comentadas")
        total += c
    # Sincronizar copia legacy de 04
    src = NOTEBOOKS / "04_eda_regional.ipynb"
    legacy = NOTEBOOKS.parent / "04_eda_regional.ipynb"
    if src.exists():
        legacy.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Total: {total} celdas")


if __name__ == "__main__":
    main()
