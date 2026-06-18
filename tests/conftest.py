"""Fixtures pytest para tests de integración."""
import pytest

from paths import OUTPUTS


@pytest.fixture
def dataset_integrado_path():
    path = OUTPUTS / "dataset_integrado.csv"
    if not path.exists():
        pytest.skip(f"Ejecutar pipeline primero: falta {path}")
    return path


@pytest.fixture
def nasa_path():
    path = OUTPUTS / "nasa_2020_2025.csv"
    if not path.exists():
        pytest.skip(f"Ejecutar notebook 02 primero: falta {path}")
    return path
