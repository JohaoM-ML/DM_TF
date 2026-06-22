# Reglas de asociación (clima → caída de producción) — experimento

Explora si vale la pena agregar un módulo de reglas de asociación (Apriori) al trabajo
final. **No forma parte del pipeline ni del informe** — es una pregunta exploratoria,
no un entregable.

```bash
python EXPERIMENTOS/asociacion_v1/explorar_reglas_asociacion.py
```

No modifica `OUTPUTS/` principal; solo lee `OUTPUTS/dataset_por_cultivo.csv` y escribe en
`EXPERIMENTOS/asociacion_v1/OUTPUTS/`. Implementado a mano con pandas (Apriori simple),
sin agregar dependencias nuevas al proyecto.

Veredicto y metodología: [`RESUMEN.md`](RESUMEN.md).
