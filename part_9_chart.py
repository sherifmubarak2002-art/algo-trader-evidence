from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "part_9_chart_data.csv"
OUTPUT_PATH = HERE / "part_9_dev_vs_oos_returns.png"


def main() -> None:
    data = pd.read_csv(CSV_PATH)
    periods = ["Development + Validation", "Out of Sample"]
    timeframes = ["Daily", "Hourly"]
    positions = range(len(periods))
    width = 0.34

    fig, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    for offset, timeframe in ((-width / 2, "Daily"), (width / 2, "Hourly")):
        values = [
            float(
                data.loc[
                    (data["Period"] == period)
                    & (data["Timeframe"] == timeframe),
                    "ReturnPercent",
                ].iloc[0]
            )
            for period in periods
        ]
        bars = ax.bar(
            [position + offset for position in positions],
            values,
            width,
            color=[
                "#38946A" if value >= 0 else "#C9534D"
                for value in values
            ],
            hatch="//" if timeframe == "Hourly" else None,
            edgecolor="#18324A",
            linewidth=0.6,
        )
        for bar, value in zip(bars, values):
            ax.annotate(
                f"{value:+.2f}%",
                (bar.get_x() + bar.get_width() / 2, value),
                xytext=(0, 5 if value >= 0 else -5),
                textcoords="offset points",
                ha="center",
                va="bottom" if value >= 0 else "top",
                fontsize=10,
                fontweight="bold",
            )

    ax.axhline(0, color="#222222", linewidth=1.1)
    ax.set_xticks(list(positions), periods)
    ax.set_ylabel("Portfolio return (%)")
    ax.set_xlabel("Evaluation period")
    ax.set_title("Portfolio Backtest Returns: Development + Validation vs OOS")
    sign_legend = ax.legend(
        handles=[
            Patch(facecolor="#38946A", label="Positive return"),
            Patch(facecolor="#C9534D", label="Negative return"),
        ],
        title="Return sign (color)",
        frameon=False,
        loc="upper left",
    )
    ax.add_artist(sign_legend)
    ax.legend(
        handles=[
            Patch(facecolor="#EEEEEE", edgecolor="#18324A", label="Daily"),
            Patch(
                facecolor="#EEEEEE",
                edgecolor="#18324A",
                hatch="//",
                label="Hourly",
            ),
        ],
        title="Timeframe (hatch)",
        frameon=False,
        loc="upper right",
    )
    ax.grid(axis="y", linestyle=":", linewidth=0.7, alpha=0.55)
    ax.set_axisbelow(True)
    ax.text(
        0.5,
        -0.18,
        "Historical portfolio backtest results; not live returns.",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9,
        color="#444444",
    )

    fig.savefig(OUTPUT_PATH, dpi=180, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
