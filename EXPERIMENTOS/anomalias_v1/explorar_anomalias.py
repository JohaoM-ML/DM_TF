"""
Experimento: deteccion de anomalias (Isolation Forest) sobre clima+produccion mensual,
para ver si un metodo no supervisado detecta por si solo la sequia 2022 (Puno) y
El Nino 2023-2024 (costa), que hoy el informe describe solo narrativamente.

No modifica el pipeline principal ni el informe. Solo lee OUTPUTS/dataset_regional.csv
y escribe sus propias salidas en EXPERIMENTOS/anomalias_v1/OUTPUTS/.

Usa sklearn.IsolationForest (ya es dependencia fija del proyecto, no agrega nada nuevo).

Uso: python EXPERIMENTOS/anomalias_v1/explorar_anomalias.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = Path(__file__).resolve().parent / "OUTPUTS"
OUT.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "produccion_piso_ton", "temp_promedio", "temp_maxima", "precipitacion",
    "humedad_relativa", "radiacion_solar", "humedad_suelo",
]
RANDOM_STATE = 42
CONTAMINATION = 0.05  # ~5% de meses esperados como anomalos


def cargar_datos() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "OUTPUTS" / "dataset_regional.csv", encoding="utf-8")
    return df.dropna(subset=FEATURES).copy()


def normalizar_por_unidad(df: pd.DataFrame) -> pd.DataFrame:
    """Z-score de cada variable dentro de su propia unidad (region, piso, distrito):
    asi 'anomalo' significa anomalo PARA ESE lugar, no solo 'es Puno' (que ya es atipico
    de por si frente a la costa)."""
    out = df.copy()
    grupo = out.groupby(["region", "piso_ecologico", "distrito"])
    for col in FEATURES:
        media = grupo[col].transform("mean")
        std = grupo[col].transform("std").replace(0, np.nan)
        out[f"{col}_z"] = (out[col] - media) / std
    return out.dropna(subset=[f"{c}_z" for c in FEATURES])


def detectar_anomalias(df: pd.DataFrame) -> pd.DataFrame:
    cols_z = [f"{c}_z" for c in FEATURES]
    modelo = IsolationForest(contamination=CONTAMINATION, random_state=RANDOM_STATE, n_estimators=200)
    out = df.copy()
    out["anomalia"] = modelo.fit_predict(out[cols_z]) == -1
    out["score_anomalia"] = -modelo.score_samples(out[cols_z])  # mayor = mas anomalo
    return out


def marcar_eventos_conocidos(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    sequia_puno = (
        (out["region"] == "Puno")
        & (out["piso_ecologico"].isin(["altiplano_lacustre", "puna_alta"]))
        & (out["anio"] == 2022)
    )
    nino_costa = (
        out["region"].isin(["Ica", "La Libertad", "Piura", "San Martin"])
        & (out["anio"].isin([2023, 2024]))
    )
    out["evento_conocido"] = "ninguno"
    out.loc[sequia_puno, "evento_conocido"] = "sequia_puno_2022"
    out.loc[nino_costa, "evento_conocido"] = "nino_costero_2023_2024"
    return out


def main() -> None:
    df = cargar_datos()
    df = normalizar_por_unidad(df)
    df = detectar_anomalias(df)
    df = marcar_eventos_conocidos(df)

    n = len(df)
    n_anom = df["anomalia"].sum()
    print(f"Filas analizadas: {n:,} | marcadas como anomalia: {n_anom:,} ({n_anom / n:.1%})")

    tasa_base = (df["evento_conocido"] != "ninguno").mean()
    tasa_en_anomalas = (df.loc[df["anomalia"], "evento_conocido"] != "ninguno").mean()
    print(f"\n% de filas que son evento conocido (sequia/Nino) en TODO el dataset: {tasa_base:.1%}")
    print(f"% de filas que son evento conocido DENTRO de las marcadas anomalas:    {tasa_en_anomalas:.1%}")

    for evento in ["sequia_puno_2022", "nino_costero_2023_2024"]:
        sub = df[df["evento_conocido"] == evento]
        detectadas = sub["anomalia"].mean()
        print(f"  - {evento}: {len(sub)} filas, {detectadas:.1%} detectadas como anomalia")

    top = df.sort_values("score_anomalia", ascending=False).head(20)
    cols_mostrar = ["region", "piso_ecologico", "distrito", "anio", "numero_mes", "evento_conocido", "score_anomalia"]
    print("\n=== Top 20 anomalias (mayor score) ===")
    print(top[cols_mostrar].to_string(index=False))

    df.sort_values("score_anomalia", ascending=False).to_csv(
        OUT / "anomalias_detectadas.csv", index=False, encoding="utf-8-sig"
    )


if __name__ == "__main__":
    main()
