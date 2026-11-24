# Reproducibility and public-edition notes

## Two different purposes

| Mode | Input | Purpose | Public verification status |
| --- | --- | --- | --- |
| `sample` | Included 20,736-row IdentityMF example | Check that the processing, fitting and evaluation code runs | All four notebooks' Python code cells executed successfully in order |
| `full` | Separately supplied 2,073,600-row IdentityMF table | Rerun the study workflow on the original full comparison data | Not executed: the full input and processed datasets were not supplied |

Historical full-study metrics and figures are retained under [`results/`](../results/README.md) and [`assets/`](../assets/README.md). They were checked against the final report and saved source notebook outputs. Agreement between these supplied artifacts is not an independent reproduction of the underlying full experiment.

No pretrained model objects, full isotonic knot table, full-data checksum or original environment export was supplied. The original notebook metadata names Python **3.13.7** but does not identify dependency versions. The pinned `requirements.txt` records a **new verification environment**, not a recovered lockfile for the original study. Even with the full input, exact numerical agreement with the historical coefficients is not guaranteed across environments.

## Environment setup

Use Python **3.12** for the tested public workflow. In the repository root:

```bash
python -m venv .venv
```

Windows PowerShell, without requiring environment activation:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts/run_notebooks.py --mode sample
```

macOS/Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/run_notebooks.py --mode sample
```

The runner reads each `.ipynb` as JSON, executes its pure-Python code cells in order, uses a fresh namespace per notebook and saves execution logs. Interactive table `display()` calls are printed to those logs; bare notebook display expressions are not rendered. Matplotlib uses `Agg`, and the evaluation cells save their six PNG files normally. No Jupyter server or kernel sockets are required, and executed `.ipynb` files are not produced. This code-cell execution was the verification method used for this edition.

### Interactive notebooks

For JupyterLab, install the optional requirements with the same environment's Python. On Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-notebooks.txt
.venv\Scripts\python.exe -m jupyterlab
```

On macOS/Linux, replace `.venv\Scripts\python.exe` with `.venv/bin/python`. Start in the repository root and use that environment's Python kernel. Run `01_preprocess`, `02_eda`, `03_calibration`, then `04_evaluation`, all in one data mode. VS Code with a suitable Python/Jupyter environment is another interface.

The JupyterLab interface and a native interactive kernel session were not validated in the verification environment. The headless runner executed all analysis code successfully; its purpose and scope are separate from UI verification.

## Full data mode

Place the full seven-column comparison table at `data/raw/IdentityMF_MinMax_fullResults.txt`, following the [data documentation](../data/README.md). This is a local prerequisite; the runner does not fetch the upstream archive or recompute comparisons from spectra.

For the command-line workflow, run the same environment's Python with:

```bash
python scripts/run_notebooks.py --mode full
```

For interactive notebooks, set `MINMAX_DATA_MODE=full` before launching JupyterLab:

```powershell
$env:MINMAX_DATA_MODE = "full"
.venv\Scripts\python.exe -m jupyterlab
```

On macOS/Linux:

```bash
MINMAX_DATA_MODE=full .venv/bin/python -m jupyterlab
```

To return to the sample in PowerShell, set `$env:MINMAX_DATA_MODE = "sample"` before launching. The headless runner's explicit `--mode` argument selects its mode regardless of the inherited environment variable.

Full-data execution loads million-row tables and creates several large CSVs. It will require substantially more memory and disk space than the sample; no full-run resource requirement is claimed here.

## Local generated files

For either mode, preprocessing writes to `data/processed/<mode>/`:

- `IdentityMF_MinMax_base_dataset.csv`
- `IdentityMF_MinMax_train.csv`
- `IdentityMF_MinMax_test.csv`

Calibration adds three 14-column test tables in the same directory:

- `IdentityMF_Logistic_r_overlap_test_predictions.csv`
- `IdentityMF_Isotonic_r_overlap_test_predictions.csv`
- `IdentityMF_Expanded_logistic_test_predictions.csv`

Evaluation writes to `outputs/<mode>/`: `final_model_metrics.csv`, `best_model_by_metric.csv`, a calibration plot, ROC plot, PR plot and three probability-distribution plots. The headless runner also writes `execution_logs/` and `run_metadata.json` with mode, Python/package versions and completion status.

All row-level data and generated directories are ignored by Git and excluded from the distributed starter. A `.gitignore` does not remove files already tracked or filter manual browser uploads; keep these local directories out of uploads. Published `results/reported_*.csv` files are small historical **aggregate** tables and are explicitly allowed.

## Verification performed

The public code-cell workflow completed with Python **3.12.14**, NumPy **2.3.5**, pandas **2.2.3**, SciPy **1.17.0**, Matplotlib **3.10.8** and scikit-learn **1.8.0**.

Checks covered input composition, score reconstruction, both labels, grouped pair membership, disjoint train/test pair IDs, aligned prediction rows, valid probability ranges, and construction of all three metric sets and six evaluation plots. The sample split contains 16,589 training rows and 4,147 test rows, with 115 and 29 positive rows respectively. No model performance threshold is asserted on the small sample.

The supplied aggregate full-study metrics agree with the final report to its displayed precision; classification metrics were additionally checked against the reported confusion counts. Public PDF covers were visually reviewed, and non-cover report content was checked for preservation. File links, notebook structure, sample bytes and packaging exclusions were also checked.

The included GitHub Actions workflow runs the headless sample command on Python 3.12 when enabled in GitHub. It was prepared for upload; it has not been run on the new remote repository. No passing-CI badge or full-data reproduction claim is made.

## Changes from the supplied notebooks

The original uploaded files remain unchanged. Public copies have the following limited changes:

1. Numbered, descriptive filenames and a shared `project_config.py` replace inconsistent input/output paths and directory fallbacks. Sample and full outputs have separate locations.
2. Input checks now require the expected seven columns, finite `[0, 1]` scores, complete records, valid labels consistent with exact code identity, and the expected mode's row/positive counts.
3. The reconstruction check uses `atol=2e-6, rtol=0`. The original strict `max_error < 1e-6` printed a warning for the saved maximum error `1.000000000139778e-6`, although that difference is consistent with source rounding. A genuine larger mismatch now raises an error.
4. Pair overlap raises an error. The calibration stage checks it again when reading saved splits.
5. Evaluation checks all 12 base-data columns across model prediction files, rather than only repeated identifiers and labels, before assuming matching observations.
6. The single-score logistic plot grid is supplied as a named DataFrame, preventing the original feature-name warning without changing its values.
7. Outputs, execution counts and machine-specific metadata are removed. Stable cell IDs and a short public-edition note are added. Historical full-study figures and summary tables are preserved separately with provenance.
8. A headless execution helper, sample workflow configuration, dependency pins and documentation are added.

The score formulas, seed `85`, 80/20 pair split, fitting calls, feature definitions, absence of class weighting, 0.5 decision threshold and metric functions are retained. The proposal's unimplemented extensions are documented as future work, rather than added retrospectively to the original study.

Original file hashes, sample provenance and extracted figure locations are in [`source_provenance.json`](source_provenance.json). The final report, presentation and proposal are public copies with cover attribution and metadata corrected and student identifiers removed. The presentation's empty trailing template slide was removed; analytical contents are retained.
