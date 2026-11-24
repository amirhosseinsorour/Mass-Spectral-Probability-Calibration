# Data documentation

## Source and analysis unit

The underlying research data were created by **Arun S. Moorthy and Edward Sisco, NIST**, for *The min-max test: an objective method for discriminating mass spectra* (2021).

- [Official dataset record](https://data.nist.gov/od/id/mds2-2418)
- [Original article](https://doi.org/10.1021/acs.analchem.1c03053)
- [Data notice and terms](../THIRD_PARTY_NOTICES.md)

The full study describes 144 compound standards with 10 replicate GC–EI–MS spectra per standard: 1,440 raw spectra. The upstream analysis produced comparison summaries using cosine similarity and Identity Match Factor (IdentityMF). This project's models use **IdentityMF min–max summaries** only.

A model input row is a replicate-based comparison between two compound standards. It is not an individual spectrum, an individual peak or a direct spectrum-to-spectrum match factor. In the full min–max dataset, all 144 × 144 ordered compound pairs are compared across 100 repeated replicate selections, producing 2,073,600 rows. Reverse directions and repeated selections share one unordered `pair_id`.

## Included example and excluded files

| Property | Included sample | Full study described in the report |
| --- | ---: | ---: |
| Rows | 20,736 | 2,073,600 |
| Same-compound rows | 144 | 14,400 |
| Different-compound rows | 20,592 | 2,059,200 |
| Positive prevalence | 0.6944% | 0.6944% |
| Unique compound codes | 144 | 144 |
| Unique unordered pairs | 10,440 | 10,440 |
| Rows per different-compound unordered pair | 2 | 200 |
| Rows per same-compound pair | 1 | 100 |

The included file, [`sample/identitymf_minmax_sample.tsv`](sample/identitymf_minmax_sample.tsv), is an unchanged byte copy of `IdentityMF/IdentityMF_MinMax_fullResults.txt` from the supplied `R-AnalyzingResults.zip`. It has been **renamed to identify it as a sample**. Despite its original `fullResults` filename, its inspected contents are incomplete relative to the full study. It has one row per ordered pair; the exact upstream procedure used to select this example was not documented in the supplied archive.

The archive contains eight `.txt` files: two min–max examples, two direct-similarity examples, and four upstream threshold-study summaries. It contains **no R source code and no raw mass spectra**. Only the IdentityMF min–max example needed by this workflow is included here. Upstream summary files were not copied because their full-data statistics should not be confused with results from the small example or this project's held-out evaluation.

The full raw spectra, full precomputed comparison tables, all processed row-level data and prediction files are intentionally excluded from the repository. Aggregate report tables and selected historical figures are published under [`results/`](../results/README.md) and [`assets/`](../assets/README.md).

## Input schema

Both input modes expect a **tab-separated text file with no header**, in this exact column order:

| Position | Name assigned by the notebook | Meaning |
| ---: | --- | --- |
| 1 | `compound_1` | First exact compound code, such as `CM1/01` |
| 2 | `compound_2` | Second exact compound code |
| 3 | `minS11` | Minimum similarity among the selected replicates within the first sample |
| 4 | `minS22` | Minimum similarity among the selected replicates within the second sample |
| 5 | `maxS12` | Maximum similarity between the two selected replicate groups |
| 6 | `delta_prime` | Original transformed min–max index, $1-\max(0,\delta)$ |
| 7 | `label` | `1` for the same exact compound code; `0` for different codes |

The score columns lie in `[0, 1]`. The supplied precision creates reconstruction differences of about `1e-6`; the publication notebooks use an absolute tolerance of `2e-6` with no relative tolerance. Positive labels require exact code equality; membership in the same chemical folder or class does not make two compounds a positive pair.

## Derived base dataset

Preprocessing creates 12 columns locally:

| Column | Derivation or purpose |
| --- | --- |
| `compound_1`, `compound_2` | Original compound identifiers |
| `pair_id` | Sorted compound codes joined with `__`; same for A–B and B–A |
| `minS11`, `minS22`, `maxS12` | Original comparison components |
| `within_min` | `min(minS11, minS22)` |
| `delta_raw` | `within_min - maxS12` |
| `r_overlap` | `maxS12 - within_min`, equivalent to `-delta_raw` |
| `delta_prime` | Original transformed index |
| `delta_prime_reconstructed` | `1 - max(0, delta_raw)` |
| `label` | Original binary target |

The label and compound identifiers are used for grouping and evaluation; compound identifiers are **not predictors** in any model. Calibration adds a probability and thresholded prediction column to each model's local test-prediction file.

## Supplying the full input locally

If you independently obtain the full IdentityMF min–max comparison table from the official source, place it at:

```text
data/raw/IdentityMF_MinMax_fullResults.txt
```

The full-input path uses an explicit local filename regardless of the original upstream folder or filename. It must be the seven-column IdentityMF min–max table, not a four-column direct-similarity table or the small example supplied here. Preprocessing checks the expected full-study row count and positive count, so renaming the sample does not make it a valid full input.

Run `python scripts/run_notebooks.py --mode full` from an environment with the analysis requirements. This uses separate `data/processed/full/` and `outputs/full/` directories. No download is performed automatically. Full-data execution was not verified when preparing this public edition because the full input was not supplied.

See [`docs/reproducibility.md`](../docs/reproducibility.md) for exact notebook order, expected outputs and verification scope.
