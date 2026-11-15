import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return Path, mo, pd, plt


@app.cell
def _(mo):
    mo.md(r"""
    # Event duration report

    Loads `data/features/events.csv` (the output of the DVC pipeline) and shows
    the distribution of event durations in minutes.
    """)
    return


@app.cell
def _(Path, pd):
    features_path = Path(__file__).resolve().parent.parent / "data" / "features" / "events.csv"
    df = pd.read_csv(features_path)
    df.head()
    return (df,)


@app.cell
def _(df, plt):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["duration_minutes"], bins=30, edgecolor="black")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of events")
    ax.set_title("Distribution of event durations")
    fig
    return


if __name__ == "__main__":
    app.run()
