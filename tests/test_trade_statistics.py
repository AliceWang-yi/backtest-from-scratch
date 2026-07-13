import pandas as pd
import pytest

from src.trade_statistics import calculate_trade_statistics


def test_trade_statistics_counts_trades_and_exposure() -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                    "2024-01-04",
                    "2024-01-05",
                    "2024-01-06",
                ]
            ),
            "position": [0, 1, 1, 0, 1, 0],
            "turnover": [0.0, 1.0, 0.0, 1.0, 1.0, 1.0],
            "cost": [0.0, 0.001, 0.0, 0.001, 0.001, 0.001],
        }
    )

    statistics = calculate_trade_statistics(
        data,
        trading_days_per_year=252,
    )

    assert statistics["buy_count"] == 2
    assert statistics["sell_count"] == 2
    assert statistics["complete_trade_count"] == 2
    assert statistics["days_in_market"] == 3
    assert statistics["average_position"] == pytest.approx(0.5)
    assert statistics["total_turnover"] == pytest.approx(4.0)
    assert statistics["annualized_turnover"] == pytest.approx(168.0)
    assert statistics["total_transaction_cost"] == pytest.approx(0.004)


def test_trade_statistics_does_not_count_inherited_position_as_complete_trade(
) -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                ]
            ),
            "position": [1, 1, 0],
            "turnover": [0.0, 0.0, 1.0],
            "cost": [0.0, 0.0, 0.001],
        }
    )

    statistics = calculate_trade_statistics(data)

    assert statistics["buy_count"] == 0
    assert statistics["sell_count"] == 1
    assert statistics["complete_trade_count"] == 0


def test_trade_statistics_returns_zero_when_position_never_changes() -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                ]
            ),
            "position": [0, 0, 0],
            "turnover": [0.0, 0.0, 0.0],
            "cost": [0.0, 0.0, 0.0],
        }
    )

    statistics = calculate_trade_statistics(data)

    assert statistics["buy_count"] == 0
    assert statistics["sell_count"] == 0
    assert statistics["complete_trade_count"] == 0
    assert statistics["days_in_market"] == 0
    assert statistics["average_position"] == pytest.approx(0.0)
    assert statistics["total_turnover"] == pytest.approx(0.0)
    assert statistics["annualized_turnover"] == pytest.approx(0.0)
    assert statistics["total_transaction_cost"] == pytest.approx(0.0)


def test_trade_statistics_sorts_dates() -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-03",
                    "2024-01-01",
                    "2024-01-02",
                ]
            ),
            "position": [0, 0, 1],
            "turnover": [1.0, 0.0, 1.0],
            "cost": [0.001, 0.0, 0.001],
        }
    )

    statistics = calculate_trade_statistics(data)

    assert statistics["buy_count"] == 1
    assert statistics["sell_count"] == 1
    assert statistics["complete_trade_count"] == 1


def test_trade_statistics_rejects_empty_data() -> None:
    data = pd.DataFrame(
        columns=[
            "Date",
            "position",
            "turnover",
            "cost",
        ]
    )

    with pytest.raises(
        ValueError,
        match="交易统计数据不能为空",
    ):
        calculate_trade_statistics(data)


def test_trade_statistics_rejects_missing_columns() -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-01"]),
            "position": [0],
        }
    )

    with pytest.raises(
        ValueError,
        match="缺少交易统计所需列",
    ):
        calculate_trade_statistics(data)
