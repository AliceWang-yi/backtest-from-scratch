from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "Date",
    "position",
    "turnover",
    "cost",
}


def calculate_trade_statistics(
    df: pd.DataFrame,
    trading_days_per_year: int = 252,
) -> dict[str, int | float]:
    """
    计算单个回测区间的交易行为统计。

    约定：
    - position 仅允许取 0 或 1；
    - turnover 表示仓位绝对变化；
    - cost 表示当日交易成本；
    - 区间开始前建立、区间内卖出的仓位不算完整交易；
    - 完整交易次数取买入次数与卖出次数的较小值。
    """
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"缺少交易统计所需列: {missing_text}")

    if df.empty:
        raise ValueError("交易统计数据不能为空")

    if trading_days_per_year <= 0:
        raise ValueError("年交易日数量必须为正整数")

    result = df.copy()
    result["Date"] = pd.to_datetime(result["Date"])
    result = result.sort_values("Date").reset_index(drop=True)

    if not result["position"].isin([0, 1]).all():
        raise ValueError("position 仅允许取 0 或 1")

    if (result["turnover"] < 0).any():
        raise ValueError("turnover 不能为负数")

    if (result["cost"] < 0).any():
        raise ValueError("cost 不能为负数")

    trade_rows = result["turnover"] > 0

    buy_count = int(
        (
            trade_rows
            & (result["position"] == 1)
        ).sum()
    )

    sell_count = int(
        (
            trade_rows
            & (result["position"] == 0)
        ).sum()
    )

    complete_trade_count = min(
        buy_count,
        sell_count,
    )

    observation_count = len(result)
    days_in_market = int(result["position"].sum())
    average_position = float(result["position"].mean())
    total_turnover = float(result["turnover"].sum())

    annualized_turnover = (
        total_turnover
        * trading_days_per_year
        / observation_count
    )

    total_transaction_cost = float(result["cost"].sum())

    return {
        "buy_count": buy_count,
        "sell_count": sell_count,
        "complete_trade_count": complete_trade_count,
        "average_position": average_position,
        "days_in_market": days_in_market,
        "total_turnover": total_turnover,
        "annualized_turnover": annualized_turnover,
        "total_transaction_cost": total_transaction_cost,
    }
