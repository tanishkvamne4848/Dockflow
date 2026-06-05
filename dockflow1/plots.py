import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def generate_score_distribution(
    results_csv,
    output_png=None,
    bins=30,
):
    """
    Generate docking score distribution plot.

    Parameters
    ----------
    results_csv : str
        Path to results.csv

    output_png : str | None
        Output image path.
        If None, creates score_distribution.png
        next to results.csv.

    bins : int
        Histogram bins.
    """

    results_csv = Path(results_csv)

    if output_png is None:
        output_png = results_csv.parent / "score_distribution.png"

    df = pd.read_csv(results_csv)

    if "Best Score" not in df.columns:
        raise ValueError(
            "results.csv must contain a 'Best Score' column"
        )

    scores = pd.to_numeric(
        df["Best Score"],
        errors="coerce"
    ).dropna()

    if len(scores) == 0:
        raise ValueError("No valid docking scores found")

    plt.figure(figsize=(10, 6))

    plt.hist(
        scores,
        bins=bins,
        density=True,
        alpha=0.6,
        edgecolor="black",
        label="Scores"
    )

    scores.plot(
        kind="kde",
        linewidth=2,
        label="Density"
    )

    plt.title("Docking Score Distribution")
    plt.xlabel("Docking Score (kcal/mol)")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    plt.close()

    return str(output_png)