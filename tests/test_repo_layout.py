"""Validación de estructura del repositorio (no requiere OUTPUTS)."""
from paths import EXPECTED_NOTEBOOKS, MAPPING, NOTEBOOKS, ROOT


def test_canonical_notebooks_exist():
    for name in EXPECTED_NOTEBOOKS:
        assert (NOTEBOOKS / name).exists(), f"Falta notebook canónico: {name}"


def test_no_duplicate_eda_at_scripts_root():
    assert not (ROOT / "SCRIPTS" / "04_eda.ipynb").exists()


def test_mapping_v2_pipeline_exists():
    assert MAPPING.exists()


def test_no_orphan_root_notebooks():
    forbidden = {"build_dataset_integrado.ipynb", "leer_midagri.ipynb"}
    for name in forbidden:
        assert not (ROOT / name).exists(), f"Notebook huérfano en raíz: {name}"
