import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "SCRIPTS"
sys.path.insert(0, str(SCRIPTS))

from pipeline_integrado import COLS_CLIMA, construir_datasets, filtrar_pareto, renombrar_columnas, validar
from paths import DATASET_INTEGRADO, MAPPING_ACTIVO, OUTPUTS


@pytest.fixture
def dfs():
    df_midagri = pd.read_csv(OUTPUTS / "midagri_largo.csv")
    df_nasa = pd.read_csv(OUTPUTS / "nasa_2020_2025.csv")
    df_mapping = pd.read_csv(MAPPING_ACTIVO)
    return construir_datasets(df_midagri, df_nasa, df_mapping)


def test_pareto_80_includes_until_threshold(dfs):
    df_b = dfs["dataset_por_cultivo"]
    df_p, combos, _ = filtrar_pareto(df_b, umbral=0.80)
    assert len(combos) == 33
    assert len(df_p) == 2376


def test_pareto_70_less_than_80(dfs):
    df_b = dfs["dataset_por_cultivo"]
    _, combos_70, _ = filtrar_pareto(df_b, umbral=0.70)
    _, combos_80, _ = filtrar_pareto(df_b, umbral=0.80)
    assert len(combos_70) <= len(combos_80)


def test_pareto_90_more_than_80(dfs):
    df_b = dfs["dataset_por_cultivo"]
    _, combos_80, _ = filtrar_pareto(df_b, umbral=0.80)
    _, combos_90, _ = filtrar_pareto(df_b, umbral=0.90)
    assert len(combos_90) >= len(combos_80)


def test_integrado_schema():
    df = pd.read_csv(DATASET_INTEGRADO)
    expected_meta = {
        "region", "piso_ecologico", "distrito", "cultivo",
        "anio", "numero_mes", "mes", "produccion_ton",
    }
    assert expected_meta.issubset(set(df.columns))
    assert set(COLS_CLIMA).issubset(set(df.columns))
    assert df.shape[1] == 20


def test_validar_coherencia(dfs):
    stats = validar(dfs)
    assert stats["max_diff_a_b"] < 1e-6


def test_renombrar_columnas():
    df = pd.DataFrame({"produccion_mensual": [1.0], "t2m": [20.0]})
    out = renombrar_columnas(df)
    assert "produccion_ton" in out.columns
    assert "temp_promedio" in out.columns
