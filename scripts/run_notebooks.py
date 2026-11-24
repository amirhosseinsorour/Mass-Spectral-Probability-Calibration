"""Run these pure-Python notebook cells in order without a Jupyter server.

Each notebook gets its own namespace. Tables print to a local log; evaluation
cells save their figures and CSVs as usual. This is a headless execution check,
not an exporter of executed Jupyter notebooks.
"""

import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = (
    "01_preprocess.ipynb",
    "02_eda.ipynb",
    "03_calibration.ipynb",
    "04_evaluation.ipynb",
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("sample", "full"), default="sample")
    args = parser.parse_args()

    sys.path.insert(0, str(ROOT))
    from project_config import get_paths

    paths = get_paths(args.mode)
    if not paths.input_path.is_file():
        parser.error(f"Input file missing: {paths.input_path}. See data/README.md.")

    os.environ["MINMAX_DATA_MODE"] = args.mode
    os.chdir(ROOT)
    log_dir = paths.evaluation_dir / "execution_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "mode": args.mode,
        "execution": "Python code cells, fresh namespace per notebook, Matplotlib Agg",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "packages": {
            package: importlib.metadata.version(package)
            for package in ("numpy", "pandas", "matplotlib", "scipy", "scikit-learn")
        },
        "completed_notebooks": [],
        "status": "running",
    }
    record_path = paths.evaluation_dir / "run_metadata.json"
    try:
        for name in NOTEBOOKS:
            print(f"[{args.mode}] Running {name}", flush=True)
            notebook = json.loads((ROOT / "notebooks" / name).read_text(encoding="utf-8"))
            namespace = {"__name__": "__main__", "display": print}
            with (log_dir / (Path(name).stem + ".log")).open("w", encoding="utf-8") as log:
                with redirect_stdout(log):
                    for number, cell in enumerate(notebook["cells"], 1):
                        if cell["cell_type"] != "code":
                            continue
                        source = "".join(cell["source"])
                        print(f"\n--- Code cell {number} ---")
                        filename = f"{name}:cell-{number}"
                        try:
                            exec(compile(source, filename, "exec"), namespace)
                        finally:
                            plt.close("all")
            record["completed_notebooks"].append(name)
        record["status"] = "completed"
    except Exception:
        record["status"] = "failed"
        raise
    finally:
        record["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    print(f"Finished {args.mode} workflow. Local outputs: {paths.evaluation_dir}")
    if args.mode == "sample":
        print("Sample results demonstrate execution; they do not reproduce the report metrics.")


if __name__ == "__main__":
    main()
