from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/processed/510300_unadjusted.csv")


def main() -> None:
    data = pd.read_csv(INPUT_PATH, parse_dates=["Date"])

    data["previous_close"] = data["Close"].shift(1)
    data["close_return"] = data["Close"].pct_change()
    data["overnight_return"] = (
        data["Open"] / data["previous_close"] - 1
    )
    data["intraday_return"] = (
        data["Close"] / data["Open"] - 1
    )

    columns = [
        "Date",
        "previous_close",
        "Open",
        "Close",
        "close_return",
        "overnight_return",
        "intraday_return",
        "Volume",
    ]

    print("最低的 20 个收盘到收盘收益率:")
    print(
        data.nsmallest(20, "close_return")[columns]
        .to_string(index=False)
    )

    print("\n最低的 20 个隔夜收益率:")
    print(
        data.nsmallest(20, "overnight_return")[columns]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
