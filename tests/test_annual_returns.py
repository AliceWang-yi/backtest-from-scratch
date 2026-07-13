from pathlib import Path

import pandas as pd
import pytest

from src.annual_returns import (
    calculate_annual_returns,
    save_annual_returns,
)


def make_return_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2023-12-29",
                    "2024-01-02",
                    "2024-01-03",
                    "2024-12-31",
                ]
            ),
            "net_strategy_return": [
                0.10,
                0.05,
                -0.02,
                0.03,
            ],
            "buy_hold_return": [
                0.08,
                0.02,
                0.01,
                -0.01,
            ],
        }
    )


def test_calculate_annual_returns_groups_by_calendar_year(
) -> None:
    result = calculate_annual_returns(
        make_return_data()
    )

    assert result["year"].tolist() == [
        2023,
        2024,
    ]
    assert result["trading_days"].tolist() == [
        1,
        3,
    ]


def test_calculate_annual_returns_uses_compounding(
) -> None:
    result = calculate_annual_returns(
        make_return_data()
    )

    row_2024 = result[
        result["year"] == 2024
    ].iloc[0]

    expected_strategy = (
        1.05
        * 0.98
        * 1.03
        - 1
    )
    expected_benchmark = (
        1.02
        * 1.01
        * 0.99
        - 1
    )

    assert row_2024[
        "strategy_return"
    ] == pytest.approx(expected_strategy)

    assert row_2024[
        "benchmark_return"
    ] == pytest.approx(expected_benchmark)


def test_excess_return_is_strategy_minus_benchmark(
) -> None:
    result = calculate_annual_returns(
        make_return_data()
    )

    row_2024 = result[
        result["year"] == 2024
    ].iloc[0]

    expected_excess = (
        row_2024["strategy_return"]
        - row_2024["benchmark_return"]
    )

    assert row_2024[
        "excess_return"
    ] == pytest.approx(expected_excess)


def test_calculate_annual_returns_sorts_dates() -> None:
    data = (
        make_return_data()
        .iloc[::-1]
        .reset_index(drop=True)
    )

    result = calculate_annual_returns(data)

    assert result["year"].tolist() == [
        2023,
        2024,
    ]


def test_calculate_annual_returns_rejects_empty_data(
) -> None:
    with pytest.raises(
        ValueError,
        match="年度收益数据不能为空",
    ):
        calculate_annual_returns(
            make_return_data().iloc[0:0]
        )


def test_calculate_annual_returns_rejects_missing_column(
) -> None:
    data = make_return_data().drop(
        columns=["buy_hold_return"]
    )

    with pytest.raises(
        ValueError,
        match="缺少年度收益计算所需列",
    ):
        calculate_annual_returns(data)


def test_save_annual_returns_creates_csv(
    tmp_path: Path,
) -> None:
    annual_returns = calculate_annual_returns(
        make_return_data()
    )

    output_path = (
        tmp_path
        / "tables"
        / "annual_returns.csv"
    )

    save_annual_returns(
        annual_returns,
        output_path,
    )

    assert output_path.exists()

    loaded = pd.read_csv(output_path)

    assert len(loaded) == 2
    assert loaded["year"].tolist() == [
        2023,
        2024,
    ]
