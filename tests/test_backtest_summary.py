from pathlib import Path

import pandas as pd
import pytest

from src.backtest_summary import (
    build_backtest_summary,
    build_period_summary,
    save_backtest_summary,
)


def make_result() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                    "2024-01-04",
                ]
            ),
            "net_strategy_return": [
                0.0,
                0.01,
                -0.01,
                0.02,
            ],
            "buy_hold_return": [
                0.0,
                0.02,
                -0.01,
                0.01,
            ],
            "position": [0, 1, 1, 0],
            "turnover": [0.0, 1.0, 0.0, 1.0],
            "cost": [0.0, 0.001, 0.0, 0.001],
        }
    )


def test_build_period_summary_contains_expected_fields() -> None:
    summary = build_period_summary(
        make_result(),
        period_name="test_period",
    )

    assert summary["period"] == "test_period"
    assert summary["start_date"] == "2024-01-01"
    assert summary["end_date"] == "2024-01-04"
    assert summary["rows"] == 4
    assert summary["buy_count"] == 1
    assert summary["sell_count"] == 1
    assert summary["complete_trade_count"] == 1
    assert summary["days_in_market"] == 2
    assert summary["total_turnover"] == pytest.approx(2.0)
    assert summary["total_transaction_cost"] == pytest.approx(
        0.002
    )


def test_build_backtest_summary_returns_one_row_per_period() -> None:
    result = make_result()

    summary = build_backtest_summary(
        [
            ("full_sample", result),
            ("in_sample", result.iloc[:2].copy()),
        ]
    )

    assert len(summary) == 2
    assert summary["period"].tolist() == [
        "full_sample",
        "in_sample",
    ]


def test_build_backtest_summary_rejects_empty_period_list() -> None:
    with pytest.raises(
        ValueError,
        match="回测区间列表不能为空",
    ):
        build_backtest_summary([])


def test_build_period_summary_rejects_empty_data() -> None:
    with pytest.raises(
        ValueError,
        match="回测汇总数据不能为空",
    ):
        build_period_summary(
            make_result().iloc[0:0],
            period_name="empty",
        )


def test_build_period_summary_rejects_missing_column() -> None:
    data = make_result().drop(columns=["cost"])

    with pytest.raises(
        ValueError,
        match="缺少回测汇总所需列",
    ):
        build_period_summary(
            data,
            period_name="missing",
        )


def test_save_backtest_summary_creates_csv(
    tmp_path: Path,
) -> None:
    summary = build_backtest_summary(
        [("full_sample", make_result())]
    )
    output_path = tmp_path / "tables" / "summary.csv"

    save_backtest_summary(
        summary,
        output_path,
    )

    assert output_path.exists()

    loaded = pd.read_csv(output_path)

    assert len(loaded) == 1
    assert loaded.loc[0, "period"] == "full_sample"
