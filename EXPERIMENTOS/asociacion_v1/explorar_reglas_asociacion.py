"""
Experimento: ¿aporta valor un modulo de reglas de asociacion (clima -> caida de produccion)?

No modifica el pipeline principal ni el informe. Solo lee OUTPUTS/dataset_por_cultivo.csv
(ya generado por el pipeline) y escribe sus propias salidas en EXPERIMENTOS/asociacion_v1/OUTPUTS/.

Idea: discretizar variables climaticas en terciles (bajo/medio/alto) por piso ecologico,
marcar meses con caida fuerte de produccion vs. la mediana historica del propio cultivo,
y minar reglas X (condiciones climaticas) -> caida_fuerte con Apriori implementado a mano
(sin agregar dependencias nuevas al proyecto).

Uso: python EXPERIMENTOS/asociacion_v1/explorar_reglas_asociacion.py
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = Path(__file__).resolve().parent / "OUTPUTS"
OUT.mkdir(parents=True, exist_ok=True)

CLIMA_VARS = [
    "temp_promedio", "temp_maxima", "precipitacion",
    "humedad_relativa", "radiacion_solar", "humedad_suelo",
]
CAIDA_UMBRAL = -0.25  # caida >= 25% vs mediana historica del propio (region, cultivo)
MIN_SUPPORT = 0.02
MIN_CONFIDENCE = 0.30


def cargar_datos() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "OUTPUTS" / "dataset_por_cultivo.csv", encoding="utf-8")
    df = df.dropna(subset=["produccion_ton"] + CLIMA_VARS).copy()
    return df


def discretizar_clima(df: pd.DataFrame) -> pd.DataFrame:
    """Terciles por rango percentil dentro de cada piso ecologico (bajo/medio/alto);
    evita comparar costa con sierra y no falla con valores climaticos repetidos."""
    out = df.copy()
    for var in CLIMA_VARS:
        rank_pct = out.groupby("piso_ecologico")[var].rank(pct=True, method="average")
        out[f"{var}_bin"] = pd.cut(
            rank_pct, bins=[0, 1 / 3, 2 / 3, 1.0], labels=["bajo", "medio", "alto"], include_lowest=True
        )
    return out


def marcar_caidas(df: pd.DataFrame) -> pd.DataFrame:
    """Caida fuerte = produccion del mes < (1 + CAIDA_UMBRAL) * mediana historica del cultivo."""
    out = df.copy()
    mediana = out.groupby(["region", "cultivo"])["produccion_ton"].transform("median")
    var_pct = (out["produccion_ton"] - mediana) / mediana.replace(0, np.nan)
    out["caida_fuerte"] = var_pct <= CAIDA_UMBRAL
    return out


def construir_transacciones(df: pd.DataFrame) -> list[frozenset]:
    bin_cols = [f"{v}_bin" for v in CLIMA_VARS]
    items_por_fila = df[bin_cols].astype(str).apply(
        lambda row: [f"{col.replace('_bin', '')}={val}" for col, val in row.items()], axis=1
    )
    evento = df["caida_fuerte"].map({True: "evento=caida_fuerte", False: "evento=normal"})
    transacciones = [frozenset(items + [ev]) for items, ev in zip(items_por_fila, evento)]
    return transacciones


def apriori_simple(transacciones: list[frozenset], min_support: float) -> dict[frozenset, float]:
    n = len(transacciones)
    items = sorted({item for t in transacciones for item in t})
    frecuentes: dict[frozenset, float] = {}
    nivel = [frozenset([i]) for i in items]
    k = 1
    while nivel:
        conteo: dict[frozenset, int] = {}
        for combo in nivel:
            cnt = sum(1 for t in transacciones if combo <= t)
            if cnt / n >= min_support:
                conteo[combo] = cnt
        if not conteo:
            break
        for combo, cnt in conteo.items():
            frecuentes[combo] = cnt / n
        k += 1
        candidatos_base = sorted({i for combo in conteo for i in combo})
        nivel = [
            frozenset(c) for c in combinations(candidatos_base, k)
            if all(frozenset(sub) in conteo for sub in combinations(c, k - 1))
        ]
        if k > 4:  # limitar profundidad, son pocas variables
            break
    return frecuentes


def generar_reglas(frecuentes: dict[frozenset, float], min_confidence: float) -> pd.DataFrame:
    filas = []
    soporte_evento = frecuentes.get(frozenset(["evento=caida_fuerte"]), 0.0)
    for itemset, sup_xy in frecuentes.items():
        if "evento=caida_fuerte" not in itemset or len(itemset) < 2:
            continue
        antecedente = itemset - {"evento=caida_fuerte"}
        sup_x = frecuentes.get(antecedente)
        if not sup_x:
            continue
        confianza = sup_xy / sup_x
        if confianza < min_confidence:
            continue
        lift = confianza / soporte_evento if soporte_evento else np.nan
        filas.append({
            "regla": " & ".join(sorted(antecedente)) + " -> caida_fuerte",
            "soporte": round(sup_xy, 4),
            "confianza": round(confianza, 4),
            "lift": round(lift, 4),
        })
    return pd.DataFrame(filas).sort_values("lift", ascending=False)


def main() -> None:
    df = cargar_datos()
    df = discretizar_clima(df)
    df = marcar_caidas(df)

    print(f"Filas usables: {len(df):,}")
    print(f"Meses con caida fuerte (>= {abs(CAIDA_UMBRAL):.0%} vs mediana del cultivo): "
          f"{df['caida_fuerte'].sum():,} ({df['caida_fuerte'].mean():.1%})")

    transacciones = construir_transacciones(df)
    frecuentes = apriori_simple(transacciones, MIN_SUPPORT)
    reglas = generar_reglas(frecuentes, MIN_CONFIDENCE)

    reglas.to_csv(OUT / "reglas_asociacion.csv", index=False, encoding="utf-8-sig")
    print(f"\nReglas encontradas (soporte>={MIN_SUPPORT}, confianza>={MIN_CONFIDENCE}): {len(reglas)}")
    if not reglas.empty:
        print(reglas.head(15).to_string(index=False))


if __name__ == "__main__":
    main()
