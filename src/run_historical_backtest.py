from pathlib import Path

import pandas as pd

from src.annual_returns import (
    calculate_annual_returns,
    save_annual_returns,
)
from src.backtest_summary import (
    build_backtest_summary,
    save_backtest_summary,
)
from src.equity_normalization import normalize_period_equity
from src.moving_average_strategy import run_moving_average_strategy
from src.performance import calculate_performance
from src.split_sample import split_by_date
from src.total_return import calculate_total_return
from src.trade_statistics import calculate_trade_statistics


PRICE_PATH = Path("data/processed/510300_unadjusted.csv")
DIVIDEND_PATH = Path("data/dividends_510300.csv")

SUMMARY_OUTPUT_PATH = Path(
    "outputs/tables/backtest_summary.csv"
)
ANNUAL_RETURNS_OUTPUT_PATH = Path(
    "outputs/tables/annual_returns.csv"
)

SPLIT_DATE = "2021-01-01"
SHORT_WINDOW = 20
LONG_WINDOW = 60
TRANSACTION_COST = 0.001


def print_trade_statistics(
    statistics: dict[str, int | float],
) -> None:
    print("\nTrade statistics:")
    print("buy count:", statistics["buy_count"])
    print("sell count:", statistics["sell_count"])
    print(
        "complete trade count:",
        statistics["complete_trade_count"],
    )
    print(
        "average position:",
        f"{statistics['average_position']:.2%}",
    )
    print(
        "days in market:",
        statistics["days_in_market"],
    )
    print(
        "total turnover:",
        f"{statistics['total_turnover']:.4f}",
    )
    print(
        "annualized turnover:",
        f"{statistics['annualized_turnover']:.4f}",
    )
    print(
        "total transaction cost:",
        f"{statistics['total_transaction_cost']:.4f}",
    )


def evaluate_period(
    result: pd.DataFrame,
    period_name: str,
) -> None:
    normalized_result = normalize_period_equity(result)

    strategy_metrics = calculate_performance(
        normalized_result["net_strategy_return"]
    )
    benchmark_metrics = calculate_performance(
        normalized_result["buy_hold_return"]
    )
    trade_statistics = calculate_trade_statistics(
        normalized_result
    )

    print(f"\n{'=' * 60}")
    print(period_name)
    print("=" * 60)

    print(
        "date range:",
        normalized_result["Date"].min().date(),
        "->",
        normalized_result["Date"].max().date(),
    )
    print("rows:", len(normalized_result))

    print("\nNormalized equity:")
    print(
        "strategy first equity:",
        f"{normalized_result['normalized_net_strategy_equity'].iloc[0]:.4f}",
    )
    print(
        "strategy final equity:",
        f"{normalized_result['normalized_net_strategy_equity'].iloc[-1]:.4f}",
    )
    print(
        "benchmark first equity:",
        f"{normalized_result['normalized_buy_hold_equity'].iloc[0]:.4f}",
    )
    print(
        "benchmark final equity:",
        f"{normalized_result['normalized_buy_hold_equity'].iloc[-1]:.4f}",
    )

    print("\nStrategy metrics:")
    print(strategy_metrics)

    print("\nBuy-and-hold metrics:")
    print(benchmark_metrics)

    print_trade_statistics(trade_statistics)


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

    full_result = run_moving_average_strategy(
        total_return_data,
        short_window=SHORT_WINDOW,
        long_window=LONG_WINDOW,
        transaction_cost=TRANSACTION_COST,
        return_column="total_return",
        signal_price_column="total_return_equity",
    )

    in_sample, out_of_sample = split_by_date(
        full_result,
        split_date=SPLIT_DATE,
    )

    print("\nBacktest parameters")
    print("-" * 60)
    print("short window:", SHORT_WINDOW)
    print("long window:", LONG_WINDOW)
    print(
        "single-side transaction cost:",
        f"{TRANSACTION_COST:.2%}",
    )
    print("split date:", SPLIT_DATE)

    evaluate_period(
        full_result,
        period_name="Full sample",
    )
    evaluate_period(
        in_sample,
        period_name="In-sample",
    )
    evaluate_period(
        out_of_sample,
        period_name="Out-of-sample",
    )

    summary = build_backtest_summary(
        [
            ("full_sample", full_result),
            ("in_sample", in_sample),
            ("out_of_sample", out_of_sample),
        ]
    )

    save_backtest_summary(
        summary,
        SUMMARY_OUTPUT_PATH,
    )

    annual_returns = calculate_annual_returns(
        full_result
    )

    save_annual_returns(
        annual_returns,
        ANNUAL_RETURNS_OUTPUT_PATH,
    )

    print(
        f"\nSaved summary to: {SUMMARY_OUTPUT_PATH}"
    )
    print(
        "Saved annual returns to:",
        ANNUAL_RETURNS_OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()
