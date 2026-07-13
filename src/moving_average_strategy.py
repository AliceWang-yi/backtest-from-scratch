import pandas as pd


DATA_PATH = "data/sample_prices.csv"


def run_moving_average_strategy(
    df: pd.DataFrame,
    short_window: int = 2,
    long_window: int = 3,
    transaction_cost: float = 0.001,
) -> pd.DataFrame:
    result = df.copy()
    result = result.sort_values("Date").reset_index(drop=True)

    result["short_ma"] = result["Close"].rolling(short_window).mean()
    result["long_ma"] = result["Close"].rolling(long_window).mean()

    result["signal"] = (
        result["short_ma"] > result["long_ma"]
    ).astype(int)

    result["position"] = (
        result["signal"].shift(1).fillna(0).astype(int)
    )

    result["daily_return"] = (
        result["Close"].pct_change().fillna(0.0)
    )

    result["strategy_return"] = (
        result["position"] * result["daily_return"]
    )

    result["turnover"] = (
        result["position"].diff().abs().fillna(0.0)
    )

    result["cost"] = result["turnover"] * transaction_cost

    result["net_strategy_return"] = (
        result["strategy_return"] - result["cost"]
    )

    result["net_strategy_equity"] = (
        1 + result["net_strategy_return"]
    ).cumprod()

    return result


if __name__ == "__main__":
    prices = pd.read_csv(DATA_PATH, parse_dates=["Date"])

    result = run_moving_average_strategy(prices)

    print(
        result[
            [
                "Date",
                "Close",
                "signal",
                "position",
                "daily_return",
                "turnover",
                "cost",
                "net_strategy_return",
                "net_strategy_equity",
            ]
        ]
    )

