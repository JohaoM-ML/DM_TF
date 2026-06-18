import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "SCRIPTS"
sys.path.insert(0, str(SCRIPTS))

from paths import DATASET_INTEGRADO, MAPPING_ACTIVO, NASA_CLIMA


def test_mapping_distritos_in_nasa():
    mapping = pd.read_csv(MAPPING_ACTIVO)
    nasa = pd.read_csv(NASA_CLIMA)
    distritos_nasa = set(nasa["distrito"].unique())
    integrado = pd.read_csv(DATASET_INTEGRADO)
    distritos_usados = set(integrado["distrito"].unique())
    assert distritos_usados.issubset(distritos_nasa)


def test_pareto_combos_have_clima():
    df = pd.read_csv(DATASET_INTEGRADO)
    assert df["temp_promedio"].notna().all()
