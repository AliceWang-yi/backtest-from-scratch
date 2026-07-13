from __future__ import annotations

import pandas as pd


EQUITY_COLUMNS = (
    "net_strategy_equity",
    "buy_hold_equity",
)


def normalize_period_equity(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    将一个展示区间内的策略净值和基准净值重新基准化为 1。

    本函数只处理已经在完整时间序列上计算完成的净值列，
    不重新计算信号、持仓、收益率或交易成本。
    """
    if df.empty:
        raise ValueError("净值归一化数据不能为空")

    required_columns = {
        "Date",
        *EQUITY_COLUMNS,
    }
    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"缺少净值归一化所需列: {missing_text}")

    result = df.copy()
    result["Date"] = pd.to_datetime(result["Date"])
    result = result.sort_values("Date").reset_index(drop=True)

    for column in EQUITY_COLUMNS:
        if result[column].isna().any():
            raise ValueError(f"净值列存在缺失值: {column}")

        first_equity = float(result[column].iloc[0])

        if first_equity <= 0:
            raise ValueError(
                f"区间第一天净值必须为正数: {column}"
            )

        normalized_column = f"normalized_{column}"
        result[normalized_column] = (
            result[column] / first_equity
        )

    return result
