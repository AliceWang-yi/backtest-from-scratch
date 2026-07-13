from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.moving_average_strategy import run_moving_average_strategy
from src.total_return import calculate_total_return


PRICE_PATH = Path("data/processed/510300_unadjusted.csv")
DIVIDEND_PATH = Path("data/dividends_510300.csv")

PARAMETER_SENSITIVITY_PATH = Path(
    "outputs/tables/parameter_sensitivity.csv"
)
COST_SENSITIVITY_PATH = Path(
    "outputs/tables/cost_sensitivity.csv"
)

EQUITY_OUTPUT_PATH = Path(
    "outputs/figures/historical_equity_curve.png"
)
DRAWDOWN_OUTPUT_PATH = Path(
    "outputs/figures/historical_drawdown.png"
)
PARAMETER_OUTPUT_PATH = Path(
    "outputs/figures/parameter_sensitivity.png"
)
COST_OUTPUT_PATH = Path(
    "outputs/figures/cost_sensitivity.png"
)

SHORT_WINDOW = 20
LONG_WINDOW = 60
TRANSACTION_COST = 0.001
SPLIT_DATE = pd.Timestamp("2021-01-01")


def calculate_drawdown(series: pd.Series) -> pd.Series:
    running_max = series.cummax()
    return series / running_max - 1


def load_historical_result() -> pd.DataFrame:
    prices = pd.read_csv(
        PRICE_PATH,
        parse_dates=["Date"],
    )

    dividends = pd.read_csv(
        DIVIDEND_PATH,
        parse_dates=["ExDate"],
    )

    total_return_data = calculate_total_return(
        prices,
        dividends,
    )

    return run_moving_average_strategy(
        total_return_data,
        short_window=SHORT_WINDOW,
        long_window=LONG_WINDOW,
        transaction_cost=TRANSACTION_COST,
        return_column="total_return",
        signal_price_column="total_return_equity",
    )


def plot_historical_equity(
    result: pd.DataFrame,
) -> None:
    plt.figure(figsize=(10, 5))

    plt.plot(
        result["Date"],
        result["net_strategy_equity"],
        label="Moving Average Strategy",
    )
    plt.plot(
        result["Date"],
        result["buy_hold_equity"],
        label="Buy and Hold",
    )

    plt.axvline(
        SPLIT_DATE,
        linestyle="--",
        label="Out-of-sample start",
    )

    plt.title("Historical Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        EQUITY_OUTPUT_PATH,
        dpi=150,
    )
    plt.close()


def plot_historical_drawdown(
    result: pd.DataFrame,
) -> None:
    strategy_drawdown = calculate_drawdown(
        result["net_strategy_equity"]
    )
    benchmark_drawdown = calculate_drawdown(
        result["buy_hold_equity"]
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        result["Date"],
        strategy_drawdown,
        label="Strategy Drawdown",
    )
    plt.plot(
        result["Date"],
        benchmark_drawdown,
        label="Buy and Hold Drawdown",
    )

    plt.axvline(
        SPLIT_DATE,
        linestyle="--",
        label="Out-of-sample start",
    )

    plt.title("Historical Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        DRAWDOWN_OUTPUT_PATH,
        dpi=150,
    )
    plt.close()


def plot_parameter_sensitivity() -> None:
    sensitivity = pd.read_csv(
        PARAMETER_SENSITIVITY_PATH
    )

    sensitivity["parameter"] = (
        sensitivity["short_window"].astype(str)
        + "/"
        + sensitivity["long_window"].astype(str)
    )

    figure, axes = plt.subplots(
        3,
        1,
        figsize=(10, 11),
        sharex=True,
    )

    axes[0].plot(
        sensitivity["parameter"],
        sensitivity["in_annual_return"],
        marker="o",
        label="In-sample",
    )
    axes[0].plot(
        sensitivity["parameter"],
        sensitivity["out_annual_return"],
        marker="o",
        label="Out-of-sample",
    )
    axes[0].axhline(
        0,
        linewidth=0.8,
        linestyle="--",
    )
    axes[0].set_ylabel("Annual Return")
    axes[0].set_title("Parameter Sensitivity")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(
        sensitivity["parameter"],
        sensitivity["in_sharpe"],
        marker="o",
        label="In-sample",
    )
    axes[1].plot(
        sensitivity["parameter"],
        sensitivity["out_sharpe"],
        marker="o",
        label="Out-of-sample",
    )
    axes[1].axhline(
        0,
        linewidth=0.8,
        linestyle="--",
    )
    axes[1].set_ylabel("Sharpe Ratio")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    axes[2].plot(
        sensitivity["parameter"],
        sensitivity["in_total_turnover"],
        marker="o",
        label="In-sample",
    )
    axes[2].plot(
        sensitivity["parameter"],
        sensitivity["out_total_turnover"],
        marker="o",
        label="Out-of-sample",
    )
    axes[2].set_xlabel("Moving Average Parameters")
    axes[2].set_ylabel("Total Turnover")
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    figure.tight_layout()
    figure.savefig(
        PARAMETER_OUTPUT_PATH,
        dpi=150,
    )
    plt.close(figure)


def plot_cost_sensitivity() -> None:
    sensitivity = pd.read_csv(
        COST_SENSITIVITY_PATH
    )

    figure, axes = plt.subplots(
        3,
        1,
        figsize=(10, 11),
        sharex=True,
    )

    axes[0].plot(
        sensitivity["transaction_cost_bps"],
        sensitivity["in_annual_return"],
        marker="o",
        label="In-sample",
    )
    axes[0].plot(
        sensitivity["transaction_cost_bps"],
        sensitivity["out_annual_return"],
        marker="o",
        label="Out-of-sample",
    )
    axes[0].axhline(
        0,
        linewidth=0.8,
        linestyle="--",
    )
    axes[0].set_ylabel("Annual Return")
    axes[0].set_title("Transaction Cost Sensitivity")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(
        sensitivity["transaction_cost_bps"],
        sensitivity["in_sharpe"],
        marker="o",
        label="In-sample",
    )
    axes[1].plot(
        sensitivity["transaction_cost_bps"],
        sensitivity["out_sharpe"],
        marker="o",
        label="Out-of-sample",
    )
    axes[1].axhline(
        0,
        linewidth=0.8,
        linestyle="--",
    )
    axes[1].set_ylabel("Sharpe Ratio")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    axes[2].plot(
        sensitivity["transaction_cost_bps"],
        sensitivity["in_total_cost"],
        marker="o",
        label="In-sample",
    )
    axes[2].plot(
        sensitivity["transaction_cost_bps"],
        sensitivity["out_total_cost"],
        marker="o",
        label="Out-of-sample",
    )
    axes[2].set_xlabel("Single-side Transaction Cost (bps)")
    axes[2].set_ylabel("Cumulative Cost Deduction")
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    figure.tight_layout()
    figure.savefig(
        COST_OUTPUT_PATH,
        dpi=150,
    )
    plt.close(figure)


def main() -> None:
    EQUITY_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = load_historical_result()

    plot_historical_equity(result)
    plot_historical_drawdown(result)
    plot_parameter_sensitivity()
    plot_cost_sensitivity()

    output_paths = [
        EQUITY_OUTPUT_PATH,
        DRAWDOWN_OUTPUT_PATH,
        PARAMETER_OUTPUT_PATH,
        COST_OUTPUT_PATH,
    ]

    for output_path in output_paths:
        print(f"Saved figure to: {output_path}")


if __name__ == "__main__":
    main()


