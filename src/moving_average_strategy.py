import pandas as pd


DATA_PATH = "data/sample_prices.csv"


def run_moving_average_strategy(
    df: pd.DataFrame,
    short_window: int = 2,
    long_window: int = 3,
    transaction_cost: float = 0.001,
    return_column: str | None = None,
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

    if return_column is None:
        selected_return = result["daily_return"]
    else:
        if return_column not in result.columns:
            raise ValueError(
                f"收益率列不存在: {return_column}"
            )

        selected_return = result[return_column]

    result["buy_hold_return"] = selected_return
    result["buy_hold_equity"] = (
        1 + result["buy_hold_return"]
    ).cumprod()

    result["strategy_return"] = (
        result["position"] * selected_return
    )

    result["turnover"] = (
        result["position"].diff().abs().fillna(0.0)
    )

    result["cost"] = (
        result["turnover"] * transaction_cost
    )

    result["net_strategy_return"] = (
        result["strategy_return"] - result["cost"]
    )

    result["net_strategy_equity"] = (
        1 + result["net_strategy_return"]
    ).cumprod()

    return result


if __name__ == "__main__":
    prices = pd.read_csv(
        DATA_PATH,
        parse_dates=["Date"],
    )

    result = run_moving_average_strategy(prices)

    from src.performance import calculate_performance

    print(
        result[
            [
                "Date",
                "Close",
                "short_ma",
                "long_ma",
                "signal",
                "position",
                "daily_return",
                "turnover",
                "cost",
                "buy_hold_return",
                "buy_hold_equity",
                "net_strategy_return",
                "net_strategy_equity",
            ]
        ]
    )

    strategy_metrics = calculate_performance(
        result["net_strategy_return"]
    )

    benchmark_metrics = calculate_performance(
        result["buy_hold_return"]
    )

    print("\nStrategy metrics:")
    print(strategy_metrics)

    print("\nBuy-and-hold metrics:")
    print(benchmark_metrics)
