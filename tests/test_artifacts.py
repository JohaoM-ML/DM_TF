"""Validación de artefactos generados por el pipeline (skip si no existen)."""
import pytest
import pandas as pd

from paths import CLIMA_COLS, FIGURES, MAPPING, META_COLS, OUTPUTS


@pytest.mark.integration
def test_dataset_integrado_schema(dataset_integrado_path):
    df = pd.read_csv(dataset_integrado_path)
    assert META_COLS.issubset(set(df.columns))
    assert CLIMA_COLS.issubset(set(df.columns))
    assert df.shape[1] == 20
    assert len(df) == 2376


@pytest.mark.integration
def test_clustering_outputs_exist():
    for name in ("06a_zonas_clusters.csv", "06b_perfiles_productivos_clusters.csv"):
        assert (OUTPUTS / name).exists(), f"Ejecutar notebook 06_clustering_final: falta {name}"


@pytest.mark.integration
def test_folium_map_exported():
    path = FIGURES / "06a_mapa_zonas.html"
    if not path.exists():
        pytest.skip("Ejecutar celda Folium en notebook 06_clustering_final")
    html = path.read_text(encoding="utf-8")
    assert "leaflet" in html.lower()


@pytest.mark.integration
def test_mapping_distritos_subset_of_nasa(nasa_path, dataset_integrado_path):
    mapping = pd.read_csv(MAPPING)
    nasa = pd.read_csv(nasa_path)
    integrado = pd.read_csv(dataset_integrado_path)
    distritos_nasa = set(nasa["distrito"].unique())
    distritos_usados = set(integrado["distrito"].unique())
    assert distritos_usados.issubset(distritos_nasa)
    assert mapping["distrito"].isin(distritos_nasa).all()
