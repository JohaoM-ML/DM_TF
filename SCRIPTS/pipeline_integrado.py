"""
Pipeline de integración MIDAGRI + NASA + mapping.
Genera dataset_integrado.csv (maestro Pareto-80) y datasets auxiliares.

Correcciones respecto a 03_merge_y_filtrado.ipynb:
  - Pareto-80: incluye cultivos hasta alcanzar >= 80% (no solo <= 80%)
  - Agregado regional: sum(min_count=1) para no convertir meses 100% NaN en 0
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# Nombres originales NASA POWER (insumo nasa_2020_2025.csv)
COLS_CLIMA_NASA = [
    "t2m", "t2m_max", "t2m_min", "prectotcorr", "rh2m",
    "allsky_sfc_sw_dwn", "ws2m", "ps", "gwetroot", "ts", "t2mdew", "qv2m",
]

# Nombres exportados en los datasets finales (español, snake_case)
RENAME_CLIMA = {
    "t2m": "temp_promedio",
    "t2m_max": "temp_maxima",
    "t2m_min": "temp_minima",
    "prectotcorr": "precipitacion",
    "rh2m": "humedad_relativa",
    "allsky_sfc_sw_dwn": "radiacion_solar",
    "ws2m": "velocidad_viento",
    "ps": "presion_atmosferica",
    "gwetroot": "humedad_suelo",
    "ts": "temp_superficie",
    "t2mdew": "punto_rocio",
    "qv2m": "humedad_especifica",
}

RENAME_COLUMNAS = {
    **RENAME_CLIMA,
    "piso_asignado": "piso_ecologico",
    "piso": "piso_ecologico",
    "mes_num": "numero_mes",
    "mes_nombre": "mes",
    "produccion_mensual": "produccion_ton",
    "produccion_total_piso": "produccion_piso_ton",
    "n_cultivos": "num_cultivos",
}

COLS_CLIMA = list(RENAME_CLIMA.values())

COLS_META_B = [
    "region", "piso_asignado", "distrito", "cultivo",
    "anio", "mes_num", "mes_nombre", "produccion_mensual",
]


def renombrar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica nombres coherentes en metadatos y variables climáticas."""
    cols = {k: v for k, v in RENAME_COLUMNAS.items() if k in df.columns}
    return df.rename(columns=cols)


def filtrar_pareto(df_b: pd.DataFrame, umbral: float = 0.80) -> tuple[pd.DataFrame, list[tuple[str, str]]]:
    """Conserva cultivos hasta alcanzar al menos `umbral` de producción regional."""
    cultivos_a_conservar: list[tuple[str, str]] = []
    reporte: list[str] = []

    for region in sorted(df_b["region"].unique()):
        prod = (
            df_b.loc[df_b["region"] == region]
            .groupby("cultivo")["produccion_mensual"]
            .sum()
            .sort_values(ascending=False)
        )
        prod = prod[prod > 0]
        if prod.empty:
            continue

        acum = prod.cumsum() / prod.sum()
        if (acum >= umbral).any():
            idx = (acum >= umbral).idxmax()
        else:
            idx = acum.index[-1]
        cultivos_top = acum.loc[:idx].index.tolist()

        for c in cultivos_top:
            cultivos_a_conservar.append((region, c))

        pct = 100 * acum.loc[idx]
        reporte.append(f"{region:<13}: {len(cultivos_top)} cultivos ({pct:.1f}% acumulado)")

    cultivos_set = set(cultivos_a_conservar)
    mask = df_b.apply(lambda r: (r["region"], r["cultivo"]) in cultivos_set, axis=1)
    return df_b.loc[mask].copy(), cultivos_a_conservar, reporte


def construir_datasets(
    df_midagri: pd.DataFrame,
    df_nasa: pd.DataFrame,
    df_mapping: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Merge completo: Análisis B, Análisis A y filtrado Pareto."""
    mapping = df_mapping[["region", "cultivo", "piso_asignado", "distrito"]].copy()

    df_b = df_midagri.merge(mapping, on=["region", "cultivo"], how="left")
    df_b = df_b.dropna(subset=["distrito"]).copy()

    df_nasa_m = df_nasa.rename(columns={"region": "region_nasa"})
    df_b = df_b.merge(df_nasa_m, on=["distrito", "anio", "mes_num"], how="left")

    cols_drop = [c for c in ["region_nasa", "lat", "lon", "piso"] if c in df_b.columns]
    df_b = df_b.drop(columns=cols_drop)
    cols_clima = [c for c in df_b.columns if c not in COLS_META_B]
    df_b = df_b[COLS_META_B + cols_clima]

    # Análisis A — producción agregada con min_count=1
    df_a_prod = (
        df_b.groupby(["region", "piso_asignado", "distrito", "anio", "mes_num", "mes_nombre"])
        .agg(
            produccion_total_piso=("produccion_mensual", lambda x: x.sum(min_count=1)),
            n_cultivos=("cultivo", "nunique"),
        )
        .reset_index()
    )

    df_clima = df_b[["distrito", "anio", "mes_num"] + cols_clima].drop_duplicates(
        ["distrito", "anio", "mes_num"]
    )
    df_a = df_a_prod.merge(df_clima, on=["distrito", "anio", "mes_num"], how="left")
    df_a = df_a.rename(columns={"piso_asignado": "piso"})
    cols_meta_a = [
        "region", "piso", "distrito", "anio", "mes_num", "mes_nombre",
        "n_cultivos", "produccion_total_piso",
    ]
    df_a = df_a[cols_meta_a + cols_clima]

    df_integrado, _, _ = filtrar_pareto(df_b, umbral=0.80)

    return {
        "dataset_por_cultivo": df_b,
        "dataset_regional": df_a,
        "dataset_integrado": df_integrado,
    }


def validar(dfs: dict[str, pd.DataFrame]) -> dict[str, object]:
    """Validaciones de coherencia y cobertura."""
    df_b = dfs["dataset_por_cultivo"]
    df_a = dfs["dataset_regional"]

    suma_b = (
        df_b.groupby(["region", "piso_asignado", "anio", "mes_num"])["produccion_mensual"]
        .sum(min_count=1)
        .reset_index()
        .rename(columns={"piso_asignado": "piso", "produccion_mensual": "suma_desde_B"})
    )
    check = df_a[["region", "piso", "anio", "mes_num", "produccion_total_piso"]].merge(
        suma_b, on=["region", "piso", "anio", "mes_num"], how="outer"
    )
    check["diferencia"] = (check["produccion_total_piso"] - check["suma_desde_B"]).abs()
    max_diff = check["diferencia"].max()

    cols_clima_nasa = [c for c in COLS_CLIMA_NASA if c in df_b.columns]
    nan_clima = df_b[cols_clima_nasa].isna().sum().sum()
    nan_prod_b = df_b["produccion_mensual"].isna().sum()
    nan_prod_a = df_a["produccion_total_piso"].isna().sum()

    return {
        "max_diff_a_b": float(max_diff) if pd.notna(max_diff) else 0.0,
        "nan_clima": int(nan_clima),
        "nan_prod_b": int(nan_prod_b),
        "nan_prod_a": int(nan_prod_a),
        "shapes": {k: v.shape for k, v in dfs.items()},
    }


def exportar(dfs: dict[str, pd.DataFrame], ruta_output: Path) -> None:
    """Exporta CSVs con redondeo en producción."""
    ruta_output.mkdir(parents=True, exist_ok=True)

    for name, df in dfs.items():
        out = renombrar_columnas(df.copy())
        if "produccion_ton" in out.columns:
            out["produccion_ton"] = out["produccion_ton"].round(4)
        if "produccion_piso_ton" in out.columns:
            out["produccion_piso_ton"] = out["produccion_piso_ton"].round(4)
        out.to_csv(ruta_output / f"{name}.csv", index=False, encoding="utf-8-sig")

    # Compatibilidad con notebooks/clustering existentes
    legacy = ruta_output / "dataset_por_cultivo_filtrado.csv"
    renombrar_columnas(dfs["dataset_integrado"]).to_csv(legacy, index=False, encoding="utf-8-sig")


def ejecutar_desde_csvs(
    ruta_output: Path,
    ruta_mapping: Path,
) -> dict[str, object]:
    """Ejecuta merge usando midagri_largo.csv y nasa_2020_2025.csv existentes."""
    df_midagri = pd.read_csv(ruta_output / "midagri_largo.csv")
    df_nasa = pd.read_csv(ruta_output / "nasa_2020_2025.csv")
    df_mapping = pd.read_csv(ruta_mapping)

    dfs = construir_datasets(df_midagri, df_nasa, df_mapping)
    stats = validar(dfs)
    _, _, reporte = filtrar_pareto(dfs["dataset_por_cultivo"])
    exportar(dfs, ruta_output)

    return {
        "dfs": {k: renombrar_columnas(v) for k, v in dfs.items()},
        "stats": stats,
        "pareto_reporte": reporte,
    }


if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parent.parent
    OUT = ROOT / "OUTPUTS"
    MAP = ROOT / "BDS" / "mapping_cultivo_distrito.csv"

    result = ejecutar_desde_csvs(OUT, MAP)
    print("=== Pareto-80 (corregido) ===")
    for line in result["pareto_reporte"]:
        print(line)
    print("\n=== Validación ===")
    for k, v in result["stats"].items():
        print(f"  {k}: {v}")
    print("\n=== Exportado ===")
    for f in sorted(OUT.glob("dataset*.csv")):
        print(f"  {f.name}")
