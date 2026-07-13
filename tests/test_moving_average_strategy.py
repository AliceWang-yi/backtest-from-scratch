import pandas as pd
import pytest


from src.moving_average_strategy import run_moving_average_strategy


def test_position_lag_and_transaction_cost():
    prices = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2026-01-01",
                    "2026-01-02",
                    "2026-01-03",
                    "2026-01-04",
                ]
            ),
            "Close": [100.0, 101.0, 102.0, 103.0],
        }
    )

    result = run_moving_average_strategy(
        prices,
        short_window=2,
        long_window=3,
        transaction_cost=0.001,
    )

    assert result.loc[2, "signal"] == 1
    assert result.loc[2, "position"] == 0
    assert result.loc[3, "position"] == 1
    assert result.loc[3, "turnover"] == 1
    assert result.loc[3, "cost"] == 0.001
def test_buy_and_hold_equity():
    prices = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-03"]
            ),
            "Close": [100.0, 110.0, 121.0],
        }
    )

    result = run_moving_average_strategy(
        prices,
        short_window=2,
        long_window=3,
        transaction_cost=0.001,
    )

    assert round(result.loc[2, "buy_hold_equity"], 6) == 1.21
def test_strategy_can_use_explicit_total_return_column() -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                    "2024-01-04",
                ]
            ),
            "Close": [100.0, 99.0, 101.0, 102.0],
            "total_return": [0.0, 0.01, 0.02, 0.01],
        }
    )

    result = run_moving_average_strategy(
        data,
        short_window=1,
        long_window=2,
        transaction_cost=0.0,
        return_column="total_return",
    )

    pd.testing.assert_series_equal(
        result["buy_hold_return"],
        data["total_return"],
        check_names=False,
    )

    expected_strategy_return = (
        result["position"] * data["total_return"]
    )

    pd.testing.assert_series_equal(
        result["strategy_return"],
        expected_strategy_return,
        check_names=False,
    )
def test_strategy_rejects_missing_return_column() -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                ["2024-01-01", "2024-01-02"]
            ),
            "Close": [100.0, 101.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="收益率列不存在",
    ):
        run_moving_average_strategy(
            data,
            return_column="total_return",
        )

