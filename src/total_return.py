import pandas as pd


def calculate_total_return(
    prices: pd.DataFrame,
    dividends: pd.DataFrame,
) -> pd.DataFrame:
    result = prices.copy()

    dividend_data = dividends.rename(
        columns={"ExDate": "Date"}
    )

    result = result.merge(
        dividend_data,
        on="Date",
        how="left",
        validate="one_to_one",
    )

    result["DividendPerShare"] = (
        result["DividendPerShare"].fillna(0.0)
    )

    previous_close = result["Close"].shift(1)

    result["price_return"] = (
        result["Close"] / previous_close - 1
    ).fillna(0.0)

    result["total_return"] = (
        (result["Close"] + result["DividendPerShare"])
        / previous_close
        - 1
    ).fillna(0.0)

    result["total_return_equity"] = (
        1 + result["total_return"]
    ).cumprod()

    return result
