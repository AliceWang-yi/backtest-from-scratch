import pandas as pd
import pytest

from src.total_return import calculate_total_return


def test_total_return_includes_dividend() -> None:
    prices = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                ["2024-01-01", "2024-01-02"]
            ),
            "Close": [100.0, 99.0],
        }
    )

    dividends = pd.DataFrame(
        {
            "ExDate": pd.to_datetime(["2024-01-02"]),
            "DividendPerShare": [2.0],
        }
    )

    result = calculate_total_return(
        prices,
        dividends,
    )

    assert result.loc[1, "price_return"] == pytest.approx(-0.01)
    assert result.loc[1, "total_return"] == pytest.approx(0.01)
    assert result.loc[1, "total_return_equity"] == pytest.approx(1.01)

