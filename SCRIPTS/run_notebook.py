"""Ejecuta un notebook in-place evitando el bug de encoding de `jupyter execute`
en Windows (nbclient.cli abre el archivo sin encoding="utf-8", lo que en locales
no-UTF8 como cp1252 corrompe todo el texto no-ASCII al guardar). Lee y escribe
siempre con encoding explicito.

Uso: python SCRIPTS/run_notebook.py <ruta_notebook>
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

path = Path(sys.argv[1])
nb = nbformat.read(path, as_version=4)
client = NotebookClient(nb, resources={"metadata": {"path": str(path.parent)}})
client.execute()
nbformat.write(nb, path)
print(f"OK: {path}")
