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

    data = prices.merge(
        dividends,
        left_on="Date",
        right_on="ExDate",
        how="left",
        validate="one_to_one",
    )

    data["DividendPerShare"] = (
        data["DividendPerShare"].fillna(0.0)
    )

    data["previous_close"] = data["Close"].shift(1)

    data["price_return"] = (
        data["Close"] / data["previous_close"] - 1
    )

    data["total_return"] = (
        (data["Close"] + data["DividendPerShare"])
        / data["previous_close"]
        - 1
    )

    ex_dates = data[data["DividendPerShare"] > 0].copy()

    columns = [
        "Date",
        "previous_close",
        "Close",
        "DividendPerShare",
        "price_return",
        "total_return",
    ]

    print(ex_dates[columns].to_string(index=False))

    price_equity = (1 + data["price_return"].fillna(0)).cumprod()
    total_equity = (1 + data["total_return"].fillna(0)).cumprod()

    print()
    print("price-only final equity:", price_equity.iloc[-1])
    print("total-return final equity:", total_equity.iloc[-1])


if __name__ == "__main__":
    main()
