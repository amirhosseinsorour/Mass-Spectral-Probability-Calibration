# Historical full-study results

These small aggregate tables preserve the numerical results of the **full experiment**, not a new fit on the public sample. Their source is the author's final report and saved outputs in the supplied calibration and evaluation notebooks.

| File | Source and precision |
| --- | --- |
| [`reported_metrics.csv`](reported_metrics.csv) | Programmatically extracted from the saved final evaluation table, original cell 15 of `Evaluation(1).ipynb`; values rounded to six decimal places |
| [`reported_confusion_matrices.csv`](reported_confusion_matrices.csv) | Counts checked against final report Table 6 and saved evaluation confusion matrices; threshold 0.5 |
| [`reported_coefficients.csv`](reported_coefficients.csv) | Full displayed precision from saved logistic fitting outputs in `Calibration(1).ipynb`, original cells 9 and 54 |

The evaluation covers 414,700 test rows: 411,800 negative and 2,900 positive, grouped into 2,088 held-out unordered pairs. The primary report comparison is in Table 5, PDF page 19; Table 6 is on PDF page 20.

The column/row label `pr_auc` in the metrics CSV denotes **average precision**, because that is the function used in the original code. It is not trapezoidal PR–AUC. `r_overlap` is the sign-reversed reconstructed raw min–max score, not the clipped `delta_prime` index.

The coefficients are historical numerical summaries. No pretrained estimator or isotonic knot table is included, so these files are not a complete model distribution. The full input, processed data and row-level predictions were not supplied for public packaging, and these metrics have not been independently recalculated on the full test set.

Running the public workflow writes new metrics into `outputs/sample/` or `outputs/full/`. It never overwrites these historical tables. See [methodology](../docs/methodology.md) for interpretation and [reproducibility](../docs/reproducibility.md) for verification scope.
