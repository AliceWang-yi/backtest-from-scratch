from pathlib import Path

import pandas as pd

from src.moving_average_strategy import run_moving_average_strategy
from src.performance import calculate_performance
from src.split_sample import split_by_date
from src.total_return import calculate_total_return


PRICE_PATH = Path("data/processed/510300_unadjusted.csv")
DIVIDEND_PATH = Path("data/dividends_510300.csv")

SPLIT_DATE = "2021-01-01"
TRANSACTION_COST = 0.001

PARAMETERS = [
    (10, 40),
    (20, 60),
    (30, 90),
    (50, 120),
]


def main() -> None:
    prices = pd.read_csv(
        PRICE_PATH,
        parse_dates=["Date"],
    )

    dividends = pd.read_csv(
        DIVIDEND_PATH,
        parse_dates=["ExDate"],
    )

    data = calculate_total_return(
        prices,
        dividends,
    )

    rows = []

    for short_window, long_window in PARAMETERS:
        result = run_moving_average_strategy(
            data,
            short_window=short_window,
            long_window=long_window,
            transaction_cost=TRANSACTION_COST,
            return_column="total_return",
        )

        in_sample, out_of_sample = split_by_date(
            result,
            split_date=SPLIT_DATE,
        )

        in_metrics = calculate_performance(
            in_sample["net_strategy_return"]
        )

        out_metrics = calculate_performance(
            out_of_sample["net_strategy_return"]
        )

        rows.append(
            {
                "short_window": short_window,
                "long_window": long_window,
                "in_annual_return": in_metrics["annual_return"],
                "in_sharpe": in_metrics["sharpe_ratio"],
                "in_max_drawdown": in_metrics["max_drawdown"],
                "out_annual_return": out_metrics["annual_return"],
                "out_sharpe": out_metrics["sharpe_ratio"],
                "out_max_drawdown": out_metrics["max_drawdown"],
            }
        )

    summary = pd.DataFrame(rows)

    print(
        summary.to_string(
            index=False,
            float_format=lambda value: f"{value:.4f}",
        )
    )


if __name__ == "__main__":
    main()
