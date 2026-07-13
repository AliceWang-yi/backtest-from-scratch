import pandas as pd


DATA_PATH = "data/sample_prices.csv"


def add_return_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result = result.sort_values("Date").reset_index(drop=True)

    result["daily_return"] = result["Close"].pct_change().fillna(0.0)
    result["equity_curve"] = (1 + result["daily_return"]).cumprod()
    result["cumulative_return"] = result["equity_curve"] - 1

    return result


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    result = add_return_columns(df)

    print(
        result[
            [
                "Date",
                "Close",
                "daily_return",
                "equity_curve",
                "cumulative_return",
            ]
        ]
    )
