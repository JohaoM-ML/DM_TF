# Detección de anomalías (Isolation Forest) — experimento

Explora si un método no supervisado de detección de anomalías detecta por sí solo la
sequía 2022 (Puno) y El Niño 2023–2024, que hoy el informe describe solo narrativamente.
**No forma parte del pipeline ni del informe** — es una pregunta exploratoria.

```bash
python EXPERIMENTOS/anomalias_v1/explorar_anomalias.py
```

No modifica `OUTPUTS/` principal; solo lee `OUTPUTS/dataset_regional.csv` y escribe en
`EXPERIMENTOS/anomalias_v1/OUTPUTS/`. Usa `sklearn.IsolationForest`, ya dependencia fija
del proyecto — no agrega nada nuevo.

Veredicto y metodología: [`RESUMEN.md`](RESUMEN.md).
