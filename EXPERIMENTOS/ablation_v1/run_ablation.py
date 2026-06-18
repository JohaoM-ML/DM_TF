"""
Ablación mapping v1 vs v2 canónico.

Uso:
  python EXPERIMENTOS/ablation_v1/run_ablation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
ABLATION = Path(__file__).resolve().parent
OUT_ABLATION = ABLATION / "OUTPUTS" / "v1"
OUT_CANON = ROOT / "OUTPUTS"
SCRIPTS = ROOT / "SCRIPTS"

sys.path.insert(0, str(SCRIPTS))
from clustering import clustering_perfiles  # noqa: E402
from pipeline_integrado import ejecutar_desde_csvs  # noqa: E402
from paths import MAPPING_V1_LEGACY  # noqa: E402


def comparar_con_canonico(stats_v1: dict, clust_v1: dict) -> str:
    lines = [
        "# Ablación mapping v1 vs v2 (canónico)",
        "",
        "El pipeline principal (`OUTPUTS/`) usa **mapping v2**.",
        "Esta carpeta reproduce el merge con **mapping v1 legacy** para comparación.",
        "",
        "## Datasets",
        "",
        "| Archivo | v1 (ablación) | v2 (canónico OUTPUTS/) |",
        "|---------|---------------:|-------------------------:|",
    ]
    for f in ["dataset_integrado.csv", "dataset_por_cultivo.csv", "dataset_regional.csv"]:
        s1 = s2 = "—"
        p1, p2 = OUT_ABLATION / f, OUT_CANON / f
        if p1.exists():
            s1 = str(pd.read_csv(p1).shape)
        if p2.exists():
            s2 = str(pd.read_csv(p2).shape)
        lines.append(f"| `{f}` | {s1} | {s2} |")

    int_v1 = pd.read_csv(OUT_ABLATION / "dataset_integrado.csv")
    int_v2 = pd.read_csv(OUT_CANON / "dataset_integrado.csv")
    lines.extend([
        "",
        f"| Combos Pareto | {int_v1.groupby(['region','cultivo']).ngroups} | {int_v2.groupby(['region','cultivo']).ngroups} |",
        "",
        "## Clustering v1 (ablación)",
        f"- K={clust_v1['k']}, Silhouette={clust_v1['silhouette']:.4f}",
        "",
        "### Pareto v1",
    ])
    for line in stats_v1.get("pareto_reporte", []):
        lines.append(f"- {line}")

    if (OUT_CANON / "robustez" / "ari_v1_v2.csv").exists():
        ari = pd.read_csv(OUT_CANON / "robustez" / "ari_v1_v2.csv")
        row = ari.iloc[0]
        lines.extend([
            "",
            "## ARI KMeans (perfiles comunes)",
            "",
            f"- ARI: {row['ari_kmeans']}",
            f"- Perfiles comunes: {int(row['n_comun'])}",
        ])

    return "\n".join(lines)


def main() -> None:
    print("=" * 60)
    print("ABLACIÓN v1 — EXPERIMENTOS/ablation_v1/")
    print("=" * 60)

    OUT_ABLATION.mkdir(parents=True, exist_ok=True)
    result = ejecutar_desde_csvs(OUT_ABLATION, MAPPING_V1_LEGACY, ruta_input=OUT_CANON)
    df_int = pd.read_csv(OUT_ABLATION / "dataset_integrado.csv")
    clust = clustering_perfiles(
        df_int,
        OUT_ABLATION,
        OUT_ABLATION / "figures",
        titulo_suffix="v1 ablación",
    )

    reporte = comparar_con_canonico(result, clust)
    reporte_path = ABLATION / "REPORTE_ablacion_v1.md"
    reporte_path.write_text(reporte, encoding="utf-8")
    print(reporte)
    print(f"\nReporte: {reporte_path}")


if __name__ == "__main__":
    main()
