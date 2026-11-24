"""Common local paths for the four research notebooks.

Sample mode is the default. Full data must be supplied locally by the reader.
This module does not download data or change model settings.
"""

from dataclasses import dataclass
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class ProjectPaths:
    mode: str
    input_path: Path
    processed_dir: Path
    evaluation_dir: Path


def get_paths(mode: str | None = None) -> ProjectPaths:
    selected = (mode or os.environ.get("MINMAX_DATA_MODE", "sample")).strip().lower()
    if selected not in {"sample", "full"}:
        raise ValueError("MINMAX_DATA_MODE must be 'sample' or 'full'.")

    source = (
        ROOT / "data" / "sample" / "identitymf_minmax_sample.tsv"
        if selected == "sample"
        else ROOT / "data" / "raw" / "IdentityMF_MinMax_fullResults.txt"
    )
    return ProjectPaths(
        mode=selected,
        input_path=source,
        processed_dir=ROOT / "data" / "processed" / selected,
        evaluation_dir=ROOT / "outputs" / selected,
    )
