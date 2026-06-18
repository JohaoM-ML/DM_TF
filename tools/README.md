# Herramientas de mantenimiento

Scripts **opcionales** para inyectar comentarios en notebooks. No forman parte del pipeline de datos.

| Script | Notebooks |
|--------|-----------|
| `apply_comments_01_03.py` | 01, 02, 03 |
| `apply_comments_04_05.py` | 04, 05 |
| `apply_comments_06.py` | 06 |

Uso (desde la raíz del repo):

```bash
python tools/apply_comments_06.py
```

Los scripts en `SCRIPTS/annotate_notebooks.py` y `SCRIPTS/add_hash_comments.py` cumplen la misma función de documentación inline.
