from pathlib import Path

import pandas as pd

from src.moving_average_strategy import run_moving_average_strategy
from src.performance import calculate_performance
from src.split_sample import split_by_date
from src.total_return import calculate_total_return
from src.trade_statistics import calculate_trade_statistics


PRICE_PATH = Path("data/processed/510300_unadjusted.csv")
DIVIDEND_PATH = Path("data/dividends_510300.csv")
OUTPUT_PATH = Path("outputs/tables/cost_sensitivity.csv")

SPLIT_DATE = "2021-01-01"
SHORT_WINDOW = 20
LONG_WINDOW = 60

TRANSACTION_COSTS = [
    0.0000,
    0.0005,
    0.0010,
    0.0020,
]


def evaluate_costs(
    data: pd.DataFrame,
    transaction_costs: list[float],
    split_date: str,
    short_window: int,
    long_window: int,
) -> pd.DataFrame:
    """
    比较不同单边交易成本下的样本内外表现。

    transaction_cost 表示每次仓位变化 1 个单位时收取的
    单边成本率。例如 0.001 表示 10 bps。
    """
    if not transaction_costs:
        raise ValueError("交易成本列表不能为空")

    if any(cost < 0 for cost in transaction_costs):
        raise ValueError("交易成本不能为负数")

    rows: list[dict[str, int | float]] = []

    for transaction_cost in transaction_costs:
        result = run_moving_average_strategy(
            data,
            short_window=short_window,
            long_window=long_window,
            transaction_cost=transaction_cost,
            return_column="total_return",
            signal_price_column="total_return_equity",
        )

        in_sample, out_of_sample = split_by_date(
            result,
            split_date=split_date,
        )

        in_metrics = calculate_performance(
            in_sample["net_strategy_return"]
        )
        out_metrics = calculate_performance(
            out_of_sample["net_strategy_return"]
        )

        in_trades = calculate_trade_statistics(in_sample)
        out_trades = calculate_trade_statistics(out_of_sample)

        rows.append(
            {
                "transaction_cost": transaction_cost,
                "transaction_cost_bps": int(
                    round(transaction_cost * 10_000)
                ),
                "in_annual_return": in_metrics["annual_return"],
                "in_annual_volatility": in_metrics[
                    "annual_volatility"
                ],
                "in_sharpe": in_metrics["sharpe_ratio"],
                "in_max_drawdown": in_metrics["max_drawdown"],
                "in_total_turnover": in_trades["total_turnover"],
                "in_total_cost": in_trades[
                    "total_transaction_cost"
                ],
                "out_annual_return": out_metrics["annual_return"],
                "out_annual_volatility": out_metrics[
                    "annual_volatility"
                ],
                "out_sharpe": out_metrics["sharpe_ratio"],
                "out_max_drawdown": out_metrics["max_drawdown"],
                "out_total_turnover": out_trades["total_turnover"],
                "out_total_cost": out_trades[
                    "total_transaction_cost"
                ],
            }
        )

    return pd.DataFrame(rows)


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

    summary = evaluate_costs(
        data=data,
        transaction_costs=TRANSACTION_COSTS,
        split_date=SPLIT_DATE,
        short_window=SHORT_WINDOW,
        long_window=LONG_WINDOW,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("Single-side transaction cost sensitivity")
    print(
        summary.to_string(
            index=False,
            float_format=lambda value: f"{value:.4f}",
        )
    )
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
