from pathlib import Path

import pandas as pd


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

    required_columns = {
        "ExDate",
        "DividendPerShare",
    }

    if set(dividends.columns) != required_columns:
        raise ValueError(
            f"分红文件列名错误: {dividends.columns.tolist()}"
        )

    if dividends.isna().any().any():
        raise ValueError("分红数据存在缺失值")

    if dividends["ExDate"].duplicated().any():
        raise ValueError("分红数据存在重复除息日")

    if not dividends["ExDate"].is_monotonic_increasing:
        raise ValueError("分红日期没有升序排列")

    if (dividends["DividendPerShare"] <= 0).any():
        raise ValueError("每份分红必须为正数")

    missing_dates = dividends.loc[
        ~dividends["ExDate"].isin(prices["Date"]),
        "ExDate",
    ]

    if not missing_dates.empty:
        raise ValueError(
            "以下除息日不在价格数据中: "
            f"{missing_dates.dt.strftime('%Y-%m-%d').tolist()}"
        )

    print("dividend rows:", len(dividends))
    print(
        "date range:",
        dividends["ExDate"].min().date(),
        "->",
        dividends["ExDate"].max().date(),
    )
    print(
        "total dividend per share:",
        dividends["DividendPerShare"].sum(),
    )
    print("all ex-dates matched price data: True")


if __name__ == "__main__":
    main()
