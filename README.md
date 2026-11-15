# DSC 190 Assignment 07: reproducible data pipeline

A DVC pipeline (`dvc.yaml`) cleans `data/raw/events.csv` in three stages
(`clean` -> `transform` -> `features`), and a Marimo notebook
(`notebooks/report.py`) plots the distribution of `duration_minutes`.

```
uv sync
uv run dvc repro                     # regenerates data/clean, data/transformed, data/features
uv run marimo edit notebooks/report.py
```
