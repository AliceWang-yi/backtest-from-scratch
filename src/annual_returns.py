from __future__ import annotations

from pathlib import Path

import pandas as pd


def calculate_annual_returns(
    result: pd.DataFrame,
) -> pd.DataFrame:
    """
    按自然年计算策略、基准和超额收益。

    年度收益使用区间内日收益率复利：
    annual_return = product(1 + daily_return) - 1

    excess_return 定义为：
    strategy_return - benchmark_return
    """
    if result.empty:
        raise ValueError("年度收益数据不能为空")

    required_columns = {
        "Date",
        "net_strategy_return",
        "buy_hold_return",
    }
    missing_columns = required_columns.difference(
        result.columns
    )

    if missing_columns:
        missing_text = ", ".join(
            sorted(missing_columns)
        )
        raise ValueError(
            f"缺少年度收益计算所需列: {missing_text}"
        )

    data = result.copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").reset_index(drop=True)

    if data[
        [
            "net_strategy_return",
            "buy_hold_return",
        ]
    ].isna().any().any():
        raise ValueError("年度收益率序列存在缺失值")

    data["year"] = data["Date"].dt.year

    rows: list[dict[str, int | float]] = []

    for year, yearly_data in data.groupby(
        "year",
        sort=True,
    ):
        strategy_return = float(
            (
                1
                + yearly_data[
                    "net_strategy_return"
                ]
            ).prod()
            - 1
        )

        benchmark_return = float(
            (
                1
                + yearly_data[
                    "buy_hold_return"
                ]
            ).prod()
            - 1
        )

        rows.append(
            {
                "year": int(year),
                "trading_days": len(yearly_data),
                "strategy_return": strategy_return,
                "benchmark_return": benchmark_return,
                "excess_return": (
                    strategy_return
                    - benchmark_return
                ),
            }
        )

    return pd.DataFrame(rows)


def save_annual_returns(
    annual_returns: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    将年度收益表保存为 UTF-8 BOM CSV。
    """
    if annual_returns.empty:
        raise ValueError("年度收益表不能为空")

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    annual_returns.to_csv(
        path,
        index=False,
        encoding="utf-8-sig",
    )
