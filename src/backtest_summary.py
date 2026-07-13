from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.performance import calculate_performance
from src.trade_statistics import calculate_trade_statistics


def build_period_summary(
    result: pd.DataFrame,
    period_name: str,
) -> dict[str, str | int | float]:
    """
    生成单个回测区间的绩效与交易行为汇总。
    """
    if result.empty:
        raise ValueError("回测汇总数据不能为空")

    required_columns = {
        "Date",
        "net_strategy_return",
        "buy_hold_return",
        "position",
        "turnover",
        "cost",
    }
    missing_columns = required_columns.difference(result.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"缺少回测汇总所需列: {missing_text}")

    data = result.copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").reset_index(drop=True)

    strategy_metrics = calculate_performance(
        data["net_strategy_return"]
    )
    benchmark_metrics = calculate_performance(
        data["buy_hold_return"]
    )
    trade_statistics = calculate_trade_statistics(data)

    return {
        "period": period_name,
        "start_date": data["Date"].iloc[0].date().isoformat(),
        "end_date": data["Date"].iloc[-1].date().isoformat(),
        "rows": len(data),
        "strategy_annual_return": strategy_metrics[
            "annual_return"
        ],
        "strategy_annual_volatility": strategy_metrics[
            "annual_volatility"
        ],
        "strategy_sharpe": strategy_metrics[
            "sharpe_ratio"
        ],
        "strategy_max_drawdown": strategy_metrics[
            "max_drawdown"
        ],
        "benchmark_annual_return": benchmark_metrics[
            "annual_return"
        ],
        "benchmark_annual_volatility": benchmark_metrics[
            "annual_volatility"
        ],
        "benchmark_sharpe": benchmark_metrics[
            "sharpe_ratio"
        ],
        "benchmark_max_drawdown": benchmark_metrics[
            "max_drawdown"
        ],
        "buy_count": trade_statistics["buy_count"],
        "sell_count": trade_statistics["sell_count"],
        "complete_trade_count": trade_statistics[
            "complete_trade_count"
        ],
        "average_position": trade_statistics[
            "average_position"
        ],
        "days_in_market": trade_statistics[
            "days_in_market"
        ],
        "total_turnover": trade_statistics[
            "total_turnover"
        ],
        "annualized_turnover": trade_statistics[
            "annualized_turnover"
        ],
        "total_transaction_cost": trade_statistics[
            "total_transaction_cost"
        ],
    }


def build_backtest_summary(
    periods: list[tuple[str, pd.DataFrame]],
) -> pd.DataFrame:
    """
    将多个回测区间汇总为一张表。
    """
    if not periods:
        raise ValueError("回测区间列表不能为空")

    rows = [
        build_period_summary(
            result=result,
            period_name=period_name,
        )
        for period_name, result in periods
    ]

    return pd.DataFrame(rows)


def save_backtest_summary(
    summary: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    将回测汇总表保存为 UTF-8 BOM CSV。
    """
    if summary.empty:
        raise ValueError("回测汇总表不能为空")

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
