"""Rutas y constantes compartidas para tests."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "SCRIPTS" / "notebooks"
PIPELINE_NOTEBOOK = NOTEBOOKS / "00_pipeline_integrado.ipynb"
OUTPUTS = ROOT / "OUTPUTS"
FIGURES = OUTPUTS / "figures"
MAPPING = ROOT / "BDS" / "mapping" / "mapping_cultivo_distrito_v2_pipeline.csv"

CLIMA_COLS = {
    "temp_promedio",
    "temp_maxima",
    "temp_minima",
    "precipitacion",
    "humedad_relativa",
    "radiacion_solar",
    "velocidad_viento",
    "presion_atmosferica",
    "humedad_suelo",
    "temp_superficie",
    "punto_rocio",
    "humedad_especifica",
}

META_COLS = {
    "region",
    "piso_ecologico",
    "distrito",
    "cultivo",
    "anio",
    "numero_mes",
    "mes",
    "produccion_ton",
}

EXPECTED_NOTEBOOKS = [
    "00_pipeline_integrado.ipynb",
    "04_eda.ipynb",
    "06_clustering_final.ipynb",
    "07_analisis_clusters.ipynb",
]
