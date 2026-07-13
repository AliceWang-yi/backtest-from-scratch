from pathlib import Path

import pandas as pd

from src.moving_average_strategy import run_moving_average_strategy
from src.performance import calculate_performance
from src.split_sample import split_by_date
from src.total_return import calculate_total_return
from src.trade_statistics import calculate_trade_statistics


PRICE_PATH = Path("data/processed/510300_unadjusted.csv")
DIVIDEND_PATH = Path("data/dividends_510300.csv")
OUTPUT_PATH = Path(
    "outputs/tables/parameter_sensitivity.csv"
)

SPLIT_DATE = "2021-01-01"
TRANSACTION_COST = 0.001

PARAMETERS = [
    (10, 40),
    (20, 60),
    (30, 90),
    (50, 120),
]


def evaluate_parameters(
    data: pd.DataFrame,
    parameters: list[tuple[int, int]],
    split_date: str,
    transaction_cost: float,
) -> pd.DataFrame:
    """
    比较多组均线参数的样本内外表现。

    本函数只用于稳健性观察，不根据样本外结果选择最优参数。
    """
    if not parameters:
        raise ValueError("参数列表不能为空")

    if transaction_cost < 0:
        raise ValueError("交易成本不能为负数")

    rows: list[dict[str, int | float]] = []

    for short_window, long_window in parameters:
        if short_window <= 0:
            raise ValueError("短期均线窗口必须为正整数")

        if long_window <= 0:
            raise ValueError("长期均线窗口必须为正整数")

        if short_window >= long_window:
            raise ValueError(
                "短期均线窗口必须小于长期均线窗口"
            )

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
                "short_window": short_window,
                "long_window": long_window,
                "transaction_cost": transaction_cost,
                "transaction_cost_bps": int(
                    round(transaction_cost * 10_000)
                ),
                "in_annual_return": in_metrics[
                    "annual_return"
                ],
                "in_annual_volatility": in_metrics[
                    "annual_volatility"
                ],
                "in_sharpe": in_metrics["sharpe_ratio"],
                "in_max_drawdown": in_metrics[
                    "max_drawdown"
                ],
                "in_average_position": in_trades[
                    "average_position"
                ],
                "in_total_turnover": in_trades[
                    "total_turnover"
                ],
                "in_annualized_turnover": in_trades[
                    "annualized_turnover"
                ],
                "out_annual_return": out_metrics[
                    "annual_return"
                ],
                "out_annual_volatility": out_metrics[
                    "annual_volatility"
                ],
                "out_sharpe": out_metrics["sharpe_ratio"],
                "out_max_drawdown": out_metrics[
                    "max_drawdown"
                ],
                "out_average_position": out_trades[
                    "average_position"
                ],
                "out_total_turnover": out_trades[
                    "total_turnover"
                ],
                "out_annualized_turnover": out_trades[
                    "annualized_turnover"
                ],
            }
        )

    return pd.DataFrame(rows)


def save_parameter_sensitivity(
    summary: pd.DataFrame,
    output_path: str | Path,
) -> None:
    if summary.empty:
        raise ValueError("参数敏感性结果不能为空")

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary.to_csv(
        path,
        index=False,
        encoding="utf-8-sig",
    )


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

    summary = evaluate_parameters(
        data=data,
        parameters=PARAMETERS,
        split_date=SPLIT_DATE,
        transaction_cost=TRANSACTION_COST,
    )

    save_parameter_sensitivity(
        summary,
        OUTPUT_PATH,
    )

    print("Parameter sensitivity analysis")
    print(
        summary.to_string(
            index=False,
            float_format=lambda value: f"{value:.4f}",
        )
    )
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
