"""
Fase A (diagnostico) — compara el distrito proxy climatico que usa hoy el
pipeline canonico (mapping v2, notebook 00) contra el distrito real donde
SISAGRI (BDS/sisagri/Sisagri_2016_2025.xlsx) registra la mayor produccion
de cada uno de los 33 combos Pareto-80 (region, cultivo) de 2020-2025.

No modifica OUTPUTS/ ni BDS/mapping/ canonicos. Escribe solo en
EXPERIMENTOS/sisagri_v3/OUTPUTS/.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RUTA_SISAGRI = ROOT / "BDS" / "sisagri" / "Sisagri_2016_2025.xlsx"
RUTA_INTEGRADO = ROOT / "OUTPUTS" / "dataset_integrado.csv"
RUTA_OUT_DIR = Path(__file__).resolve().parent / "OUTPUTS"
RUTA_OUT_DIR.mkdir(parents=True, exist_ok=True)

DPTO_MAP = {
    "ICA": "Ica",
    "JUNIN": "Junin",
    "LA LIBERTAD": "La Libertad",
    "PIURA": "Piura",
    "PUNO": "Puno",
    "SAN MARTIN": "San Martin",
}

# Distritos NASA ya descargados hoy (notebook 02) — si el distrito real de
# SISAGRI coincide con uno de estos, no hace falta pedir un punto nuevo.
DISTRITOS_NASA_ACTUALES = {
    "Chincha Alta", "Viru", "Huamachuco", "Cascas", "Tambogrande", "Sullana",
    "Canchaque", "Moyobamba", "Tocache", "Perene", "Rio Tambo", "El Tambo",
    "Ilave", "Ayaviri",
}

# Equivalencia EXACTA cultivo del proyecto -> nombre dsc_Cultivo en SISAGRI.
# Verificada a mano contra los nombres reales de cada region (no fuzzy/substring
# — un intento anterior con substring confundio "papa" con "papaya").
# None = SISAGRI no registra el cultivo en absoluto para esa region.
CULTIVO_SISAGRI: dict[str, str | None] = {
    "alfalfa": "ALFALFA",
    "esparrago": "ESPARRAGO",
    "maiz_amarillo_duro": "MAIZ AMARILLO DURO",
    "mandarina": "MANDARINA",
    "palta": "PALTA",
    "papa": "PAPA",
    "tomate": "TOMATE",
    "uva": "VID",
    "avena_forrajera": "AVENA FORRAJERA",
    "cafe_pergamino": "CAFE",
    "maiz_choclo": "MAIZ CHOCLO",
    "naranja": "NARANJA",
    "pina": "PIÑA",
    "platano": "PLATANO",
    "yuca": "YUCA",
    "arroz_cascara": "ARROZ",
    "mango": "MANGO",
    "cana_para_azucar": "CAÑA DE AZUCAR (ALCOHOL)",  # parcial: ver NOTAS_ESPECIALES
    "palma_aceitera": None,  # SISAGRI no registra palma aceitera en ningun departamento
}

# Casos donde la cobertura SISAGRI es nula, parcial o de baja confianza y
# requiere una nota explicita en el reporte (decidido junto al usuario).
NOTAS_ESPECIALES: dict[tuple[str, str], dict] = {
    ("La Libertad", "cana_para_azucar"): {
        "fuente_evidencia": "gemini_hipotesis_no_verificada",
        "nivel_confianza": "baja",
        "distrito_candidato": "Casa Grande (Ascope) o Laredo (Trujillo)",
        "nota": (
            "SISAGRI no registra ningun tipo de cana de azucar en La Libertad "
            "(ni siquiera la variante alcohol). Candidato propuesto por Gemini "
            "(LLM, sin cifras verificadas) — Casa Grande y Laredo son zonas "
            "caneras historicas conocidas, pero no hay evidencia medida."
        ),
    },
    ("Piura", "cana_para_azucar"): {
        "fuente_evidencia": "sisagri_excel_medido_parcial",
        "nivel_confianza": "media",
        "nota": (
            "SISAGRI solo registra la variante 'CANA DE AZUCAR (ALCOHOL)', "
            "un producto secundario distinto de la industria azucarera "
            "dominante (azucar de exportacion). El distrito real calculado "
            "abajo puede no representar la zona cazucarera principal de Piura."
        ),
    },
    ("San Martin", "palma_aceitera"): {
        "fuente_evidencia": "sin_evidencia_mantener_proxy",
        "nivel_confianza": "alta",
        "nota": (
            "SISAGRI no registra palma aceitera en ningun departamento del "
            "Peru (cultivo agroindustrial de gran escala, fuera del alcance "
            "de este sistema de reporte municipal). El distrito actual "
            "(Tocache) coincide con la hipotesis independiente de Gemini, "
            "asi que se mantiene sin cambios con confianza alta."
        ),
    },
}


def cargar_sisagri() -> pd.DataFrame:
    hojas = pd.read_excel(RUTA_SISAGRI, sheet_name=["2016_2020", "2021_2025"])
    sis = pd.concat(hojas.values(), ignore_index=True)
    sis = sis[sis["Dpto"].isin(DPTO_MAP)].copy()
    sis["region"] = sis["Dpto"].map(DPTO_MAP)
    return sis[sis["anho"].between(2020, 2025)]


def distrito_dominante(sis: pd.DataFrame, region: str, cultivo_sisagri: str) -> pd.DataFrame:
    """Top distritos por produccion (t) para un cultivo exacto en una region."""
    sub = sis[(sis["region"] == region) & (sis["dsc_Cultivo"] == cultivo_sisagri)]
    if sub.empty:
        return pd.DataFrame()
    agg = (
        sub.groupby("Dist")[["PRODUCCION(t)", "COSECHA (ha)"]]
        .sum()
        .sort_values("PRODUCCION(t)", ascending=False)
    )
    agg["rendimiento_ton_ha"] = agg["PRODUCCION(t)"] / agg["COSECHA (ha)"].replace(0, pd.NA)
    return agg


def _normalizar(s: str) -> str:
    """Compara nombres de distrito ignorando espacios/mayusculas (SISAGRI
    escribe 'TAMBO GRANDE', el pipeline actual usa 'Tambogrande' — mismo lugar)."""
    return str(s).strip().lower().replace(" ", "")


def clasificar_estado(distrito_actual: str, distrito_real: str | None) -> str:
    if distrito_real is None:
        return "SIN_EVIDENCIA"
    if _normalizar(distrito_real) == _normalizar(distrito_actual):
        return "COINCIDE"
    if any(_normalizar(distrito_real) == _normalizar(d) for d in DISTRITOS_NASA_ACTUALES):
        return "DIFIERE_PUNTO_EXISTENTE"
    return "DIFIERE_PUNTO_NUEVO"


def main() -> None:
    sis = cargar_sisagri()
    combos = (
        pd.read_csv(RUTA_INTEGRADO)[["region", "cultivo", "piso_ecologico", "distrito"]]
        .drop_duplicates()
        .sort_values(["region", "cultivo"])
        .reset_index(drop=True)
    )

    filas = []
    for _, row in combos.iterrows():
        region, cultivo, distrito_actual = row["region"], row["cultivo"], row["distrito"]
        especial = NOTAS_ESPECIALES.get((region, cultivo))
        cultivo_sisagri = CULTIVO_SISAGRI.get(cultivo)

        fila = {
            "region": region,
            "cultivo": cultivo,
            "distrito_actual": distrito_actual,
            "cultivo_sisagri": cultivo_sisagri,
            "distrito_real_1": None,
            "produccion_ton_1": None,
            "cosecha_ha_1": None,
            "rendimiento_ton_ha_1": None,
            "distrito_real_2": None,
            "produccion_ton_2": None,
            "estado": None,
            "fuente_evidencia": "sisagri_excel_medido",
            "nivel_confianza": "alta",
            "nota": "",
        }

        if especial:
            fila["fuente_evidencia"] = especial["fuente_evidencia"]
            fila["nivel_confianza"] = especial["nivel_confianza"]
            fila["nota"] = especial["nota"]
            if "distrito_candidato" in especial:
                fila["distrito_real_1"] = especial["distrito_candidato"]

        if cultivo_sisagri is None:
            fila["estado"] = "SIN_EVIDENCIA"
            filas.append(fila)
            continue

        top = distrito_dominante(sis, region, cultivo_sisagri)
        if top.empty:
            fila["estado"] = "SIN_EVIDENCIA"
            filas.append(fila)
            continue

        d1 = top.index[0]
        fila["distrito_real_1"] = d1
        fila["produccion_ton_1"] = round(float(top.iloc[0]["PRODUCCION(t)"]), 1)
        fila["cosecha_ha_1"] = round(float(top.iloc[0]["COSECHA (ha)"]), 1)
        fila["rendimiento_ton_ha_1"] = (
            round(float(top.iloc[0]["rendimiento_ton_ha"]), 2)
            if pd.notna(top.iloc[0]["rendimiento_ton_ha"])
            else None
        )
        if len(top) > 1:
            fila["distrito_real_2"] = top.index[1]
            fila["produccion_ton_2"] = round(float(top.iloc[1]["PRODUCCION(t)"]), 1)
        fila["estado"] = clasificar_estado(distrito_actual, d1)
        filas.append(fila)

    out = pd.DataFrame(filas)
    ruta_csv = RUTA_OUT_DIR / "comparacion_distrito_v2_vs_sisagri.csv"
    out.to_csv(ruta_csv, index=False, encoding="utf-8-sig")

    # --- Resumen markdown ---
    conteo = out["estado"].value_counts()
    nuevos = out[out["estado"] == "DIFIERE_PUNTO_NUEVO"].sort_values(
        "produccion_ton_1", ascending=False
    )

    lineas = [
        "# Comparacion distrito v2 (actual) vs SISAGRI (medido) — Fase A",
        "",
        f"Total combos Pareto-80: {len(out)}",
        "",
        "## Conteo por estado",
        "",
        "| Estado | Cantidad |",
        "|---|---|",
    ]
    for estado, n in conteo.items():
        lineas.append(f"| {estado} | {n} |")

    lineas += [
        "",
        "## Distritos nuevos candidatos (ordenados por produccion, requieren punto NASA nuevo)",
        "",
        "| Region | Cultivo | Distrito actual | Distrito real (SISAGRI) | Produccion (t) | Fuente |",
        "|---|---|---|---|---|---|",
    ]
    for _, r in nuevos.iterrows():
        lineas.append(
            f"| {r['region']} | {r['cultivo']} | {r['distrito_actual']} | "
            f"{r['distrito_real_1']} | {r['produccion_ton_1']:,.0f} | {r['fuente_evidencia']} |"
        )

    lineas += ["", "## Casos sin evidencia o con nota especial", ""]
    especiales_out = out[out["nota"] != ""]
    for _, r in especiales_out.iterrows():
        lineas.append(f"- **{r['region']} / {r['cultivo']}** ({r['nivel_confianza']}): {r['nota']}")

    ruta_md = RUTA_OUT_DIR / "resumen_comparacion.md"
    ruta_md.write_text("\n".join(lineas), encoding="utf-8")

    print(f"Filas: {len(out)}")
    print(conteo.to_string())
    print(f"\nEscrito: {ruta_csv}")
    print(f"Escrito: {ruta_md}")


if __name__ == "__main__":
    main()
