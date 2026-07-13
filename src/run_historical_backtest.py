from pathlib import Path

import pandas as pd

from src.moving_average_strategy import run_moving_average_strategy
from src.performance import calculate_performance
from src.total_return import calculate_total_return


PRICE_PATH = Path("data/processed/510300_unadjusted.csv")
DIVIDEND_PATH = Path("data/dividends_510300.csv")


def main() -> None:
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

    result = run_moving_average_strategy(
        total_return_data,
        short_window=20,
        long_window=60,
        transaction_cost=0.001,
        return_column="total_return",
    )

    strategy_metrics = calculate_performance(
        result["net_strategy_return"]
    )

    benchmark_metrics = calculate_performance(
        result["buy_hold_return"]
    )

    print("rows:", len(result))
    print(
        "date range:",
        result["Date"].min().date(),
        "->",
        result["Date"].max().date(),
    )

    print("\nStrategy metrics:")
    print(strategy_metrics)

    print("\nBuy-and-hold metrics:")
    print(benchmark_metrics)


if __name__ == "__main__":
    main()
