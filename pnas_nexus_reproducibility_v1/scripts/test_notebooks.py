#!/usr/bin/env python3
from __future__ import annotations

import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if len(notebooks) != 5:
        raise RuntimeError(f"Expected five clean notebooks, found {len(notebooks)}")
    with tempfile.TemporaryDirectory(prefix="pnas-notebooks-") as temporary:
        for path in notebooks:
            nb = nbformat.read(path, as_version=4)
            if any(cell.get("outputs") for cell in nb.cells if cell.cell_type == "code"):
                raise RuntimeError(f"Distributed notebook contains outputs: {path.name}")
            client = NotebookClient(nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}})
            executed = client.execute()
            nbformat.write(executed, Path(temporary) / path.name)
            print(f"passed: {path.name}")


if __name__ == "__main__":
    main()
