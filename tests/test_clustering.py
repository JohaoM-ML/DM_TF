import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "SCRIPTS"
sys.path.insert(0, str(SCRIPTS))

from clustering import clustering_perfiles, construir_perfiles
from paths import DATASET_INTEGRADO, OUTPUTS


def test_construir_perfiles_count():
    df = pd.read_csv(DATASET_INTEGRADO)
    df_perfil, features = construir_perfiles(df)
    n_combos = df.groupby(["region", "cultivo"]).ngroups
    assert len(df_perfil) == n_combos == 33
    assert len(features) >= 10


def test_clustering_runs():
    df = pd.read_csv(DATASET_INTEGRADO)
    result = clustering_perfiles(df, OUTPUTS / "_test_cluster", OUTPUTS / "_test_cluster" / "figures")
    assert 2 <= result["k"] <= 7
    assert result["n_perfiles"] == 33
    assert (OUTPUTS / "_test_cluster" / "clustering_perfiles.csv").exists()
