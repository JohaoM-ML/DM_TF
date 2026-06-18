#!/usr/bin/env python3
"""
Aplica comentarios extensos en español a los notebooks 01, 02 y 03.
Lee _nb_code_dump.txt como referencia del código ejecutable y reescribe
únicamente las celdas de código (markdown intacto).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUMP_PATH = ROOT / "_nb_code_dump.txt"
NOTEBOOKS = [
    ROOT / "SCRIPTS" / "notebooks" / "01_midagri_pipeline.ipynb",
    ROOT / "SCRIPTS" / "notebooks" / "02_nasa_pipeline.ipynb",
    ROOT / "SCRIPTS" / "notebooks" / "03_build_dataset_integrado.ipynb",
]

# Comentarios superficiales o duplicados que se eliminan
SHALLOW_PATTERNS = [
    re.compile(r"^\s*#\s*Salida informativa en consola\s*$"),
    re.compile(r"^\s*#\s*Bucle por subgrupos\s*$"),
    re.compile(r"^\s*#\s*--- Importaciones ---\s*$"),
    re.compile(r"^\s*#\s*--- Rutas del proyecto ---\s*$"),
    re.compile(r"^\s*#\s*Definición de función:\s*"),
    re.compile(r"^\s*#\s*Constantes del análisis\s*$"),
    re.compile(r"^\s*#\s*Configuración de entorno gráfico\s*$"),
    re.compile(r"^\s*#\s*DataFrame acumulado MIDAGRI\s*$"),
    re.compile(r"^\s*#\s*Transformación del dataframe MIDAGRI\s*$"),
    re.compile(r"^\s*#\s*Ejecutar pipeline de integración\s*$"),
    re.compile(r"^\s*#\s*Validar que el insumo exista antes de continuar\s*$"),
    re.compile(r"^\s*#\s*=== DIAGNÓSTICO.*===\s*$"),
    re.compile(r"^\s*#\s*=== AUDITORÍA.*===\s*$"),
    re.compile(r"^\s*#\s*§0 Setup\s*$"),
    re.compile(r"^\s*#\s*>>>>>>>>>\s*AJUSTAR ESTA RUTA\s*<<<<<<<<<\s*$"),
    re.compile(r"^\s*#\s*Cargar CSV principal en memoria\s*$"),
    re.compile(r"^\s*#\s*Diccionario de archivos requeridos\s*$"),
    re.compile(r"^\s*#\s*--- Funciones de integración.*---\s*$"),
    re.compile(r"^\s*#\s*Reporte de meses faltantes\s*$"),
    re.compile(r"^\s*#\s*Cargar todos los archivos descubiertos\s*$"),
    re.compile(r"^\s*#\s*Lista de todos los cultivos únicos\s*$"),
    re.compile(r"^\s*#\s*Distribución de valores\s*$"),
    re.compile(r"^\s*#\s*Reordenar columnas\s*$"),
    re.compile(r"^\s*#\s*Agregar nombre del mes para legibilidad\s*$"),
    re.compile(r"^\s*#\s*Mostrar la lista lista para pegar\s*$"),
    re.compile(r"^\s*#\s*Mostrar grupos con más de 1 variante\s*$"),
    re.compile(r"^\s*#\s*Agrupar por \"nombre limpio\".*\s*$"),
    re.compile(r"^\s*#\s*Calcular diff por \(region, anio\).*\s*$"),
    re.compile(r"^\s*#\s*Tratamiento de negativos.*\s*$"),
    re.compile(r"^\s*#\s*Validacion: monotonia.*\s*$"),
    re.compile(r"^\s*#\s*Verificacion: filas con TODO NaN.*\s*$"),
    re.compile(r"^\s*#\s*Umbral Pareto-80 por región\s*$"),
    re.compile(r"^\s*#\s*Rutas relativas al repo.*\s*$"),
    re.compile(r"^\s*#\s*Años a procesar\s*$"),
    re.compile(r"^\s*#\s*Regiones objetivo.*\s*$"),
    re.compile(r"^\s*#\s*Mapeo de meses.*\s*$"),
    re.compile(r"^\s*#\s*Mapeo de variantes de cultivos.*\s*$"),
    re.compile(r"^\s*#\s*Endpoint NASA POWER.*\s*$"),
    re.compile(r"^\s*#\s*Rango temporal\s*$"),
    re.compile(r"^\s*#\s*Variables climaticas crudas.*\s*$"),
    re.compile(r"^\s*#\s*14 distritos seleccionados.*\s*$"),
    re.compile(r"^\s*#\s*Lowercase nombres de variables.*\s*$"),
    re.compile(r"^\s*#\s*Cuáles cultivos tienen mayor.*\s*$"),
    re.compile(r"^\s*#\s*Por región: cuántos cultivos.*\s*$"),
    re.compile(r"^\s*#\s*Cargar UN archivo de muestra.*\s*$"),
    re.compile(r"^\s*#\s*Usaremos la misma lógica.*\s*$"),
    re.compile(r"^\s*#\s*Cargar TODOS los archivos sin mapeo.*\s*$"),
    re.compile(r"^\s*#\s*=== DIAGNÓSTICO: detectar variantes.*\s*$"),
]

OLD_HEADER = re.compile(
    r"^\s*#\s*=+\s*\n\s*#\s*CELDA:.*\n\s*#\s*=+\s*$", re.MULTILINE
)


def parse_dump(path: Path) -> dict[str, dict[int, str]]:
    """Extrae celdas del volcado: {notebook_name: {cell_index: source}}."""
    text = path.read_text(encoding="utf-8")
    sections: dict[str, dict[int, str]] = {}
    current_nb: str | None = None
    current_cell: int | None = None
    buf: list[str] = []

    def flush():
        nonlocal buf, current_nb, current_cell
        if current_nb and current_cell is not None and buf:
            sections.setdefault(current_nb, {})[current_cell] = "\n".join(buf).rstrip()
        buf = []

    for line in text.splitlines():
        if line.startswith("# SCRIPTS/notebooks/") and line.endswith(".ipynb"):
            flush()
            current_nb = Path(line.split()[-1]).name
            current_cell = None
            continue
        m = re.match(r"^--- CELL (\d+) ---$", line.strip())
        if m:
            flush()
            current_cell = int(m.group(1))
            continue
        if line.startswith("################################################################################"):
            continue
        if current_cell is not None:
            buf.append(line)
    flush()
    return sections


def is_shallow_comment(line: str) -> bool:
    return any(p.match(line) for p in SHALLOW_PATTERNS)


def strip_old_header_and_shallow(source: str) -> list[str]:
    """Devuelve líneas ejecutables conservando docstrings y comentarios útiles inline."""
    lines = source.splitlines()
    out: list[str] = []
    skip_header = True
    for line in lines:
        if skip_header:
            if re.match(r"^\s*#\s*=+", line):
                continue
            if re.match(r"^\s*#\s*CELDA:", line):
                continue
            skip_header = False
        if is_shallow_comment(line):
            continue
        out.append(line)
    # Quitar líneas vacías iniciales
    while out and not out[0].strip():
        out.pop(0)
    return out


def make_header(n: int, title: str, intro: list[str]) -> list[str]:
    lines = [
        "# " + "=" * 68,
        f"# CELDA {n}: {title}",
        "# " + "=" * 68,
    ]
    for ln in intro:
        lines.append(f"# {ln}")
    lines.append("")
    return lines


# Metadatos por notebook: lista ordenada de celdas de código
CELL_META: dict[str, list[dict]] = {
    "01_midagri_pipeline.ipynb": [
        {
            "idx": 1,
            "title": "Importaciones y configuración de pandas",
            "intro": [
                "Primer bloque ejecutable del pipeline MIDAGRI (notebook 01).",
                "Carga librerías para leer Excel, normalizar texto y manejar rutas.",
                "No produce archivos; prepara el entorno para las celdas siguientes.",
                "Salida implícita: módulos importados y opciones de visualización activas.",
            ],
        },
        {
            "idx": 3,
            "title": "Rutas BDS/OUTPUTS, años y regiones objetivo",
            "intro": [
                "Define dónde están los Excel MIDAGRI (BDS/) y dónde escribir CSV (OUTPUTS/).",
                "Detecta la raíz del repo aunque el kernel se lance desde SCRIPTS/ o notebooks/.",
                "Fija el universo temporal (2020-2025) y las 6 regiones del estudio.",
                "Incluye diccionarios de meses y mapeo de nombres de cultivos rotos en Excel.",
            ],
        },
        {
            "idx": 5,
            "title": "Funciones de normalización de nombres",
            "intro": [
                "Utilidades reutilizadas en todo el notebook para homogeneizar etiquetas.",
                "MIDAGRI usa tildes, mayúsculas y guiones irregulares en columnas y regiones.",
                "Estas funciones convierten texto a snake_case ASCII y unifican variantes.",
                "No modifican datos aún; solo definen la lógica de limpieza nominal.",
            ],
        },
        {
            "idx": 7,
            "title": "Descubrimiento de archivos Excel c-18",
            "intro": [
                "Escanea BDS/YYYY/*.xlsx y construye un índice (año, mes) → ruta.",
                "El mes se infiere del nombre del archivo (p. ej. 'MARZO 2021.xlsx').",
                "Genera un reporte de cobertura: meses presentes vs. faltantes por año.",
                "Salida: dict `archivos` usado por todas las cargas posteriores.",
            ],
        },
        {
            "idx": 9,
            "title": "Carga y limpieza de cada archivo MIDAGRI",
            "intro": [
                "Lee la hoja c-18 de cada Excel: producción acumulada por región y cultivo.",
                "Detecta la fila de encabezado, elimina totales nacionales y columnas espejo.",
                "Normaliza nombres, filtra regiones objetivo y concatena todos los meses.",
                "Salida: `df_acumulado` en formato ancho (una columna por cultivo).",
            ],
        },
        {
            "idx": 11,
            "title": "Recuperación de diciembre 2020 desde dic-2021",
            "intro": [
                "MIDAGRI no publicó dic-2020; el Excel de dic-2021 incluye filas comparativas 2020.",
                "Extrae esas filas como proxy del acumulado de diciembre 2020.",
                "Evita duplicar filas si ya existían registros para (2020, 12).",
                "Salida: `df_acumulado` actualizado con diciembre 2020 recuperado.",
            ],
        },
        {
            "idx": 13,
            "title": "Grid completo región×año×mes con NaN explícitos",
            "intro": [
                "Construye el producto cartesiano región × año × mes (1-12).",
                "Hace left merge con datos reales: meses sin archivo quedan como NaN.",
                "Documenta explícitamente los huecos temporales (no se imputan valores).",
                "Salida: grilla completa ordenada, base para calcular producción mensual.",
            ],
        },
        {
            "idx": 15,
            "title": "Producción mensual real vía diff() del acumulado",
            "intro": [
                "MIDAGRI reporta producción acumulada; la mensual = diff mes a mes por región/año.",
                "Enero conserva el valor original (no hay mes anterior en la serie anual).",
                "Negativos del diff (revisiones retroactivas) se convierten a NaN.",
                "Salida: `df_mensual` con producción mensual estimada por cultivo.",
            ],
        },
        {
            "idx": 17,
            "title": "Diagnóstico de variantes de nombres de cultivos",
            "intro": [
                "Celda exploratoria: detecta columnas que representan el mismo cultivo.",
                "Carga archivos SIN mapeo canónico para ver nombres crudos del Excel.",
                "Agrupa variantes (p. ej. acei_tuna vs aceituna) y sugiere MAPEO_CANONICO.",
                "No altera el pipeline principal; sirve para auditar la limpieza nominal.",
            ],
        },
        {
            "idx": 19,
            "title": "Conversión a formato largo (melt)",
            "intro": [
                "Pasa de formato ancho (columnas=cultivos) a largo (filas=observaciones).",
                "Cada fila queda: región, año, mes, cultivo, produccion_mensual.",
                "Añade mes_nombre legible y ordena para inspección y exportación.",
                "Salida: `df_largo`, formato estándar para merge con clima en notebook 03.",
            ],
        },
        {
            "idx": 21,
            "title": "Diagnóstico post-melt de cultivos",
            "intro": [
                "Segunda pasada de diagnóstico sobre cultivos ya en formato largo.",
                "Verifica que el mapeo canónico no dejó duplicados semánticos.",
                "Cuenta filas con dato por variante para priorizar fusiones.",
                "Imprime sugerencias listas para pegar en MAPEO_CANONICO si hiciera falta.",
            ],
        },
        {
            "idx": 23,
            "title": "Exportar midagri_largo.csv",
            "intro": [
                "Persiste el dataset limpio en OUTPUTS/midagri_largo.csv.",
                "Encoding utf-8-sig para compatibilidad con Excel en Windows.",
                "Este CSV es insumo obligatorio del notebook 03 (integración).",
                "Salida en disco: ~432 filas × 54 cultivos × 6 regiones (con NaN explícitos).",
            ],
        },
        {
            "idx": 25,
            "title": "Auditoría final del dataset MIDAGRI",
            "intro": [
                "Resumen descriptivo del CSV exportado antes de pasar al pipeline NASA.",
                "Cuenta NaN, ceros y valores positivos en produccion_mensual.",
                "Identifica cultivos con muchos ceros (no se siembran en ciertas regiones).",
                "Cierra el notebook 01 con métricas de calidad y cobertura regional.",
            ],
        },
    ],
    "02_nasa_pipeline.ipynb": [
        {
            "idx": 1,
            "title": "Importaciones para API NASA POWER",
            "intro": [
                "Notebook 02: descarga variables climáticas mensuales vía NASA POWER.",
                "Importa pandas, requests y utilidades para llamadas HTTP con reintentos.",
                "Entrada: ninguna. Prepara el cliente HTTP y opciones de display.",
                "Salida del pipeline completo: OUTPUTS/nasa_2020_2025.csv.",
            ],
        },
        {
            "idx": 3,
            "title": "Coordenadas de los 14 distritos y parámetros climáticos",
            "intro": [
                "Define los 14 distritos representativos (lat/lon) alineados al mapping v2.",
                "Lista 12 parámetros AG de NASA POWER (temperatura, lluvia, radiación, etc.).",
                "Rango 2020-2025 coherente con MIDAGRI del notebook 01.",
                "Calcula filas esperadas: 14 distritos × 72 meses = 1 008 registros.",
            ],
        },
        {
            "idx": 5,
            "title": "Función de descarga con reintentos",
            "intro": [
                "Encapsula la llamada GET a la API temporal/monthly/point de NASA POWER.",
                "Reintenta hasta 3 veces con backoff exponencial ante errores de red o HTTP.",
                "Parsea JSON y devuelve DataFrame indexado por YYYYMM.",
                "Función pura reutilizada en el bucle de descarga por distrito.",
            ],
        },
        {
            "idx": 7,
            "title": "Descarga secuencial por distrito",
            "intro": [
                "Itera los 14 distritos y acumula respuestas en una lista de DataFrames.",
                "Añade metadatos territoriales (región, piso, lat, lon) a cada bloque.",
                "Concatena todo en `df_nasa` con índice continuo.",
                "Salida: datos crudos de API listos para limpieza en la celda siguiente.",
            ],
        },
        {
            "idx": 9,
            "title": "Limpieza: mes 13, -999→NaN, renombrar columnas",
            "intro": [
                "Elimina filas MM=13 (resumen anual que NASA incluye al final).",
                "Reemplaza -999 (missing flag de NASA) por NaN en variables climáticas.",
                "Deriva columnas anio y mes_num desde fecha_yyyymm.",
                "Normaliza nombres a minúsculas para merge consistente con notebook 03.",
            ],
        },
        {
            "idx": 11,
            "title": "Validación de filas y rangos por distrito",
            "intro": [
                "Sanity check: 72 filas por distrito y cobertura 2020-2025.",
                "Reporta porcentaje de NaN por variable climática.",
                "Muestra min/mean/max para detectar unidades o outliers groseros.",
                "No modifica datos; solo audita antes de interpolar.",
            ],
        },
        {
            "idx": 14,
            "title": "Ejemplo visual de interpolación lineal",
            "intro": [
                "Demostración pedagógica con radiación solar en Ilave (Puno).",
                "Compara serie original vs. interpolada alrededor del primer NaN.",
                "Explica si el hueco está al inicio, medio o final de la serie.",
                "No altera df_nasa; prepara la justificación del método de imputación.",
            ],
        },
        {
            "idx": 16,
            "title": "Interpolación de NaN climáticos restantes",
            "intro": [
                "Aplica interpolación lineal por distrito, con ffill/bfill en bordes.",
                "Solo se ejecuta si quedan NaN tras la limpieza de -999.",
                "Preserva series temporales continuas para correlaciones posteriores.",
                "Salida: `df_nasa` sin NaN (salvo casos donde la variable no aplica).",
            ],
        },
        {
            "idx": 18,
            "title": "Exportar nasa_2020_2025.csv",
            "intro": [
                "Escribe OUTPUTS/nasa_2020_2025.csv con encoding utf-8-sig.",
                "Incluye metadatos territoriales + 12 variables climáticas mensuales.",
                "Segundo insumo obligatorio del notebook 03 (integración MIDAGRI+clima).",
                "Muestra primeras filas y confirma conteo total antes de cerrar.",
            ],
        },
    ],
    "03_build_dataset_integrado.ipynb": [
        {
            "idx": 1,
            "title": "Setup — rutas e imports",
            "intro": [
                "Notebook 03: integra producción MIDAGRI, clima NASA y mapping cultivo→distrito.",
                "Resuelve rutas relativas al repo y crea carpetas OUTPUTS/ y figures/.",
                "Apunta al mapping v2_pipeline y a los CSV de salida finales.",
                "Entrada: repos ejecutados 01 y 02. Salida: dataset_integrado.csv y derivados.",
            ],
        },
        {
            "idx": 3,
            "title": "Verificar insumos (01, 02, mapping)",
            "intro": [
                "Comprueba existencia de midagri_largo.csv, nasa_2020_2025.csv y mapping.",
                "Falla rápido con FileNotFoundError si falta algún archivo previo.",
                "Evita merges parciales o errores crípticos más adelante.",
                "Salida: mensaje 'Insumos listos' y dict `insumos` con rutas absolutas.",
            ],
        },
        {
            "idx": 5,
            "title": "Vista previa MIDAGRI, NASA y mapping",
            "intro": [
                "Carga los tres CSV en memoria para inspección rápida de dimensiones.",
                "Muestra regiones presentes en MIDAGRI (deben coincidir con mapping).",
                "No transforma datos; confirma que los esquemas son mergeables.",
                "Salida: df_midagri, df_nasa, df_mapping en el namespace del notebook.",
            ],
        },
        {
            "idx": 7,
            "title": "Merge, Pareto-80, agregados y exportación",
            "intro": [
                "Núcleo del pipeline: une MIDAGRI + mapping + NASA por distrito/mes.",
                "Genera dataset_por_cultivo (B), dataset_regional (A) y dataset_integrado (Pareto).",
                "Filtra cultivos hasta cubrir ≥80% de producción regional acumulada.",
                "Valida coherencia A vs B, exporta CSVs renombrados al español.",
            ],
        },
        {
            "idx": 10,
            "title": "Resumen del dataset_integrado.csv exportado",
            "intro": [
                "Recarga desde disco el CSV integrado recién exportado.",
                "Resume filas, columnas, combinaciones región-cultivo y NaN en producción.",
                "Lista todos los dataset*.csv en OUTPUTS con conteo de filas.",
                "Cierra el notebook 03 con describe() numérico del producto final.",
            ],
        },
    ],
}


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _prefix_comment(comment: str, indent: int) -> str:
    pad = " " * indent
    return f"{pad}# {comment}"


def annotate_lines(clean_lines: list[str], meta: dict, cell_num: int) -> str:
    """Inserta comentarios extensos antes de bloques lógicos sin alterar código."""
    header = make_header(cell_num, meta["title"], meta["intro"])
    result: list[str] = list(header)
    i = 0
    n = len(clean_lines)

    def add_block(comments: list[str], indent: int = 0):
        for c in comments:
            result.append(_prefix_comment(c, indent))

    while i < n:
        line = clean_lines[i]
        stripped = line.strip()
        indent = _indent_of(line)

        # Saltar líneas vacías (se preservan después)
        if not stripped:
            result.append(line)
            i += 1
            continue

        # --- Comentarios antes de imports ---
        if re.match(r"^(import |from )", stripped):
            if i == 0 or not re.match(r"^(import |from )", clean_lines[i - 1].strip()):
                add_block([
                    "Importación de módulos necesarios para esta celda.",
                    "Se agrupan al inicio según convención PEP 8.",
                ], indent)

        # --- Constantes UPPER_CASE ---
        elif re.match(r"^[A-Z][A-Z0-9_]*\s*=", stripped) and "def " not in stripped:
            name = stripped.split("=")[0].strip()
            ctx = {
                "ROOT": "Raíz del repositorio; se ajusta si cwd es notebooks/ o SCRIPTS/.",
                "RUTA_BASE": "Carpeta BDS/ con Excel MIDAGRI organizados por año.",
                "RUTA_OUTPUT": "Carpeta OUTPUTS/ donde se escriben CSV e figuras.",
                "ANIOS": "Ventana temporal principal del estudio agroclimático.",
                "REGIONES_OBJETIVO": "Seis regiones con mayor peso agrícola en el proyecto.",
                "MES_NUM": "Traduce nombre de mes en MAYÚSCULAS (Excel) a entero 1-12.",
                "NUM_MES": "Traduce entero de mes a nombre legible en español.",
                "MAPEO_CANONICO": "Fusiona variantes rotas de nombres de cultivos en MIDAGRI.",
                "URL_NASA": "Endpoint REST NASA POWER para series mensuales por punto.",
                "ANIO_INICIO": "Primer año incluido en la descarga climática.",
                "ANIO_FIN": "Último año incluido (inclusive) en la descarga climática.",
                "PARAMETROS": "Variables crudas solicitadas a NASA POWER (comunidad AG).",
                "DISTRITOS": "14 puntos geográficos representativos con lat/lon y piso ecológico.",
                "COLS_CLIMA_NASA": "Subconjunto de columnas climáticas en minúsculas post-merge.",
                "RENAME_CLIMA": "Diccionario de renombre a etiquetas en español para exportación.",
                "RENAME_COLUMNAS": "Renombres adicionales de metadatos y producción al exportar.",
                "COLS_META_B": "Columnas de identificación del dataset por cultivo (nivel B).",
                "UMBRAL_PARETO": "Fracción de producción regional acumulada que define cultivos top.",
                "RUTA_MAPPING": "CSV que asigna cada (región, cultivo) a un distrito representativo.",
                "DATASET_INTEGRADO": "Ruta del CSV final filtrado por Pareto-80.",
                "DATASET_REGIONAL": "Ruta del CSV agregado por piso/distrito (nivel A).",
                "RUTA_FIGURES": "Subcarpeta para gráficos generados en notebooks posteriores.",
            }.get(name.split("[")[0], f"Constante de configuración: `{name}`.")
            add_block([ctx, "Valor fijado aquí para reutilizarse en celdas posteriores."], indent)

        # --- Definiciones de función ---
        elif stripped.startswith("def "):
            fname = re.match(r"def\s+(\w+)", stripped)
            fname = fname.group(1) if fname else "función"
            descs = {
                "normalizar_nombre": "Convierte texto a snake_case ASCII sin tildes ni símbolos.",
                "aplicar_canonico": "Busca alias en MAPEO_CANONICO; si no existe, deja el nombre.",
                "normalizar_region": "Quita tildes de nombres de departamento para comparar con MIDAGRI.",
                "extraer_mes_de_filename": "Infiere mes 1-12 desde el stem del archivo Excel.",
                "descubrir_archivos": "Indexa todos los .xlsx por (año, mes) bajo BDS/YYYY/.",
                "cargar_archivo": "Pipeline completo de lectura y limpieza de un Excel c-18.",
                "recuperar_dic_2020": "Imputa dic-2020 usando filas 2020 del Excel dic-2021.",
                "construir_grid_completo": "Outer grid región×año×mes; huecos quedan como NaN.",
                "cargar_archivo_crudo": "Igual que cargar_archivo pero SIN mapeo canónico (diagnóstico).",
                "descargar_nasa": "GET a NASA POWER con reintentos y parseo JSON→DataFrame.",
                "renombrar_columnas": "Aplica RENAME_COLUMNAS solo sobre columnas presentes.",
                "filtrar_pareto": "Por región, conserva cultivos hasta alcanzar umbral acumulado.",
                "construir_datasets": "Orquesta merges y produce dict con 3 datasets analíticos.",
                "validar": "Compara suma de B vs total en A; cuenta NaN de clima y producción.",
                "exportar": "Escribe CSVs renombrados y duplica integrado como filtrado.",
            }
            add_block([
                f"Definición de `{fname}()`.",
                descs.get(fname, "Función auxiliar del pipeline; ver docstring para detalle."),
            ], indent)

        # --- Bucles for ---
        elif re.match(r"for ", stripped):
            if ".groupby" in stripped or "grupo" in stripped:
                add_block([
                    "Iteración por subgrupos del DataFrame (groupby).",
                    "Cada iteración procesa un bloque homogéneo (región, cultivo, distrito, etc.).",
                ], indent)
            elif "archivos.items()" in stripped:
                add_block([
                    "Recorre cronológicamente todos los Excel descubiertos.",
                    "Cada par (año, mes) se carga y apendiza a la lista dfs.",
                ], indent)
            elif "DISTRITOS" in stripped:
                add_block([
                    "Descarga secuencial: una llamada HTTP por distrito (14 en total).",
                    "Evita saturar la API; el progreso se imprime en consola.",
                ], indent)
            elif "cols_cultivos" in stripped or "cols_clima" in stripped:
                add_block([
                    "Bucle columna a columna sobre variables de cultivo o clima.",
                    "Permite aplicar la misma transformación a cada variable homogéneamente.",
                ], indent)
            elif "insumos.items()" in stripped:
                add_block([
                    "Verifica cada archivo requerido antes de continuar el merge.",
                ], indent)
            elif "reporte_pareto" in stripped:
                add_block([
                    "Imprime el desglose Pareto-80 región por región.",
                ], indent)
            elif "stats.items()" in stripped:
                add_block([
                    "Muestra métricas de validación post-merge (NaN, shapes, diff A-B).",
                ], indent)
            elif "variantes" in stripped or "cultivos_unicos" in stripped or "cultivos_crudos" in stripped:
                add_block([
                    "Agrupa nombres de cultivos que difieren solo por guiones o typos.",
                ], indent)
            elif "MESES" in stripped or "anio" in stripped:
                add_block([
                    "Iteración temporal para reportes de cobertura o auditoría.",
                ], indent)
            else:
                add_block(["Bucle de iteración sobre elementos de una colección."], indent)

        # --- Merge ---
        elif ".merge(" in stripped:
            add_block([
                "Operación merge (join) entre DataFrames.",
                "Une claves compartidas; how='left' preserva filas del lado izquierdo.",
            ], indent)

        # --- Concat ---
        elif ".concat(" in stripped or "pd.concat(" in stripped:
            add_block([
                "Concatena verticalmente DataFrames con la misstructura de columnas.",
            ], indent)

        # --- Melt ---
        elif ".melt(" in stripped:
            add_block([
                "Transforma de formato ancho (columnas=cultivos) a largo (filas=observaciones).",
                "id_vars conservan región, año y mes; value_vars son todos los cultivos.",
            ], indent)

        # --- Export CSV ---
        elif ".to_csv(" in stripped:
            add_block([
                "Exportación a CSV en OUTPUTS/ con encoding utf-8-sig (Excel-friendly).",
                "index=False evita escribir el índice numérico de pandas.",
            ], indent)

        # --- Groupby agg ---
        elif ".groupby(" in stripped and i + 1 < n and ".agg(" in clean_lines[i + 1]:
            add_block([
                "Agregación con groupby: resume producción o clima por claves territoriales.",
            ], indent)

        # --- read_csv / read_excel ---
        elif ".read_csv(" in stripped or ".read_excel(" in stripped:
            add_block([
                "Lectura de archivo tabular desde disco hacia un DataFrame pandas.",
            ], indent)

        # --- Asignaciones clave de DataFrame ---
        elif stripped.startswith("df_") and "=" in stripped and ".(" not in stripped:
            if "df_acumulado" in stripped:
                add_block(["DataFrame acumulado MIDAGRI (producción YTD por mes)."], indent)
            elif "df_mensual" in stripped:
                add_block(["DataFrame con producción mensual (diff del acumulado)."], indent)
            elif "df_largo" in stripped:
                add_block(["Dataset en formato largo listo para exportar o mergear."], indent)
            elif "df_nasa" in stripped:
                add_block(["DataFrame maestro de clima NASA por distrito y mes."], indent)
            elif "df_integrado" in stripped:
                add_block(["Dataset integrado post-Pareto (cultivos top por región)."], indent)

        # --- if/else notables ---
        elif stripped.startswith("if ") and "faltantes" in stripped:
            add_block([
                "Control de calidad: aborta si faltan insumos de notebooks anteriores.",
            ], indent)
        elif stripped.startswith("if ") and "n_nan_antes" in stripped:
            add_block([
                "Solo interpola si quedaron NaN tras limpiar flags -999 de NASA.",
            ], indent)
        elif stripped.startswith("if ") and "mask_vacio" in stripped:
            add_block([
                "Lista meses donde ningún cultivo tiene dato (archivo faltante).",
            ], indent)

        # --- requests.get ---
        elif "requests.get(" in stripped:
            add_block([
                "Petición HTTP GET a la API NASA POWER con parámetros de consulta.",
            ], indent)

        # --- print inicial de celda ---
        elif stripped.startswith("print(") and i > 0:
            prev = clean_lines[i - 1].strip()
            if not prev.startswith("print(") and not prev.endswith(","):
                add_block([
                    "Salida de consola para trazabilidad y verificación intermedia.",
                ], indent)

        result.append(line)
        i += 1

    return "\n".join(result) + "\n"


def code_cell_indices(nb: dict) -> list[int]:
    return [i for i, c in enumerate(nb["cells"]) if c["cell_type"] == "code"]


def apply_to_notebook(nb_path: Path, dump_cells: dict[int, str], meta_list: list[dict]) -> dict:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    code_idxs = code_cell_indices(nb)
    if len(code_idxs) != len(meta_list):
        raise ValueError(
            f"{nb_path.name}: {len(code_idxs)} celdas código vs {len(meta_list)} metadatos"
        )
    changed = 0
    for seq, (cell_idx, meta) in enumerate(zip(code_idxs, meta_list), start=1):
        dump_idx = meta["idx"]
        if dump_idx not in dump_cells:
            raise KeyError(f"{nb_path.name}: falta CELL {dump_idx} en dump")
        clean = strip_old_header_and_shallow(dump_cells[dump_idx])
        annotated = annotate_lines(clean, meta, seq)
        old_src = "".join(nb["cells"][cell_idx]["source"])
        if old_src != annotated:
            nb["cells"][cell_idx]["source"] = annotated.splitlines(keepends=True)
            changed += 1
    nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"path": str(nb_path), "code_cells": len(code_idxs), "changed": changed}


def main():
    dump = parse_dump(DUMP_PATH)
    summary = []
    for nb_path in NOTEBOOKS:
        nb_name = nb_path.name
        if nb_name not in CELL_META:
            print(f"[SKIP] Sin metadatos: {nb_name}")
            continue
        if nb_name not in dump:
            print(f"[ERROR] Sin celdas en dump: {nb_name}")
            continue
        info = apply_to_notebook(nb_path, dump[nb_name], CELL_META[nb_name])
        summary.append(info)
        print(f"[OK] {nb_name}: {info['changed']}/{info['code_cells']} celdas actualizadas")

    print("\n" + "=" * 60)
    print("RESUMEN apply_comments_01_03.py")
    print("=" * 60)
    total_cells = sum(s["code_cells"] for s in summary)
    total_changed = sum(s["changed"] for s in summary)
    print(f"Notebooks procesados : {len(summary)}")
    print(f"Celdas de código     : {total_cells}")
    print(f"Celdas modificadas   : {total_changed}")
    for s in summary:
        print(f"  - {Path(s['path']).name}: {s['changed']} cambios")


if __name__ == "__main__":
    main()
