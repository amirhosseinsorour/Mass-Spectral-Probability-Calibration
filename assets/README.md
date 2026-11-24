# Full-study figures

All five PNGs are extracted directly from image outputs already saved in the author's supplied notebooks. They were **not regenerated using the 20,736-row sample**.

| Figure | Original source |
| --- | --- |
| [`reported_score_distribution.png`](reported_score_distribution.png) | `EDA(1).ipynb`, cell 15 |
| [`reported_probability_curves.png`](reported_probability_curves.png) | `Calibration(1).ipynb`, cell 46 |
| [`reported_calibration_curve.png`](reported_calibration_curve.png) | `Evaluation(1).ipynb`, cell 21 |
| [`reported_roc_curve.png`](reported_roc_curve.png) | `Evaluation(1).ipynb`, cell 23 |
| [`reported_precision_recall_curve.png`](reported_precision_recall_curve.png) | `Evaluation(1).ipynb`, cell 25 |

Cell numbers are one-based positions in the uploaded source notebooks. The [provenance record](../docs/source_provenance.json) records source file hashes. The public notebooks have cleared outputs to prevent historical full-data figures from being mistaken for the results of a new sample run.

The calibration figure uses ten quantile bins, which limits its detail under severe class imbalance. The precision–recall figure's AP labels reflect `average_precision_score`. See [methodology](../docs/methodology.md) for both definitions.
