import pandas as pd

from src.calculate_returns import add_return_columns


def test_return_calculation():
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
            "Close": [100.0, 110.0],
        }
    )

    result = add_return_columns(data)

    assert result.loc[0, "daily_return"] == 0.0
    assert round(result.loc[1, "daily_return"], 6) == 0.1
    assert round(result.loc[1, "equity_curve"], 6) == 1.1

