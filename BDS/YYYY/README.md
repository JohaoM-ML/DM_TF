# Datos MIDAGRI (insumo local)

Coloca aquí los Excel del **cuadro C-18** (Agro en Cifras, MIDAGRI Perú), uno por año:

```
BDS/YYYY/
  2020.xlsx
  2021.xlsx
  ...
  2025.xlsx
```

Los `.xlsx` **no se versionan** (`.gitignore`). Sin ellos, el notebook `01_midagri_pipeline.ipynb` no puede generar `OUTPUTS/midagri_largo.csv`.

## Dónde obtenerlos

1. [MIDAGRI — Agro en Cifras](https://www.gob.pe/midagri)
2. Descargar cuadro **C-18** (producción agrícola por departamento/cultivo)
3. Renombrar o copiar a `BDS/YYYY/AAAA.xlsx` según el año

## Alternativa (solo EDA/clustering)

Si ya tienes `OUTPUTS/midagri_largo.csv` generado en otra máquina, puedes copiarlo localmente y continuar desde el notebook **02** (NASA requiere red) o **03** si también tienes clima.
