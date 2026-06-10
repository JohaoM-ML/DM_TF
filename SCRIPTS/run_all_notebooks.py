"""Ejecuta todos los notebooks del proyecto y reporta errores."""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NOTEBOOKS = [
    ("SCRIPTS/01_midagri_pipeline.ipynb", ROOT, 600),
    ("SCRIPTS/02_nasa_pipeline.ipynb", ROOT, 900),
    ("SCRIPTS/03_merge_y_filtrado.ipynb", ROOT, 300),
    ("build_dataset_integrado.ipynb", ROOT, 300),
    ("SCRIPTS/04_eda_regional.ipynb", ROOT, 600),
    ("SCRIPTS/05_eda_por_cultivo.ipynb", ROOT, 600),
    ("Clustering/Clustering_Cultivos.ipynb", ROOT, 1200),
]


def run_one(rel: str, cwd: Path, timeout: int) -> dict:
    src = ROOT / rel
    out = ROOT / "OUTPUTS" / "_executed" / rel.replace("/", "_").replace("\\", "_")
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        str(src),
        "--output", str(out.name),
        "--output-dir", str(out.parent),
        "--ExecutePreprocessor.timeout", str(timeout),
    ]
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout + 120
        )
        ok = proc.returncode == 0
        err = proc.stderr.strip() or proc.stdout.strip()
    except subprocess.TimeoutExpired as e:
        ok = False
        err = f"Timeout ({timeout}s): {e}"
    except Exception as e:
        ok = False
        err = str(e)

    return {
        "notebook": rel,
        "ok": ok,
        "seconds": round(time.time() - t0, 1),
        "error": err[-3000:] if err else "",
    }


def main():
    results = []
    print("=" * 60)
    print("Ejecutando notebooks DM_TF")
    print("=" * 60)
    for rel, cwd, timeout in NOTEBOOKS:
        print(f"\n>> {rel} ...", flush=True)
        r = run_one(rel, cwd, timeout)
        status = "OK" if r["ok"] else "FAIL"
        print(f"   [{status}] {r['seconds']}s")
        if not r["ok"]:
            print(f"   {r['error'][:500]}")
        results.append(r)

    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    for r in results:
        mark = "OK  " if r["ok"] else "FAIL"
        print(f"  [{mark}] {r['notebook']} ({r['seconds']}s)")

    fails = [r for r in results if not r["ok"]]
    if fails:
        print(f"\n{len(fails)} notebook(s) con error.")
        for r in fails:
            print(f"\n--- {r['notebook']} ---\n{r['error']}")
        sys.exit(1)
    print("\nTodos los notebooks ejecutaron sin errores.")
    sys.exit(0)


if __name__ == "__main__":
    main()
