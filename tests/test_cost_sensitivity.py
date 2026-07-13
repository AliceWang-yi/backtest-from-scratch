import pandas as pd
import pytest

from src.cost_sensitivity import evaluate_costs


def make_test_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2020-12-28",
                    "2020-12-29",
                    "2020-12-30",
                    "2020-12-31",
                    "2021-01-04",
                    "2021-01-05",
                    "2021-01-06",
                    "2021-01-07",
                ]
            ),
            "Close": [
                100.0,
                101.0,
                102.0,
                101.0,
                103.0,
                104.0,
                102.0,
                105.0,
            ],
            "total_return": [
                0.0,
                0.01,
                0.0099,
                -0.0098,
                0.0198,
                0.0097,
                -0.0192,
                0.0294,
            ],
            "total_return_equity": [
                1.00,
                1.01,
                1.02,
                1.01,
                1.03,
                1.04,
                1.02,
                1.05,
            ],
        }
    )


def test_evaluate_costs_returns_one_row_per_cost() -> None:
    summary = evaluate_costs(
        data=make_test_data(),
        transaction_costs=[0.0, 0.001],
        split_date="2021-01-01",
        short_window=1,
        long_window=2,
    )

    assert len(summary) == 2
    assert summary["transaction_cost_bps"].tolist() == [0, 10]


def test_higher_cost_does_not_change_turnover() -> None:
    summary = evaluate_costs(
        data=make_test_data(),
        transaction_costs=[0.0, 0.001],
        split_date="2021-01-01",
        short_window=1,
        long_window=2,
    )

    assert summary.loc[0, "in_total_turnover"] == pytest.approx(
        summary.loc[1, "in_total_turnover"]
    )
    assert summary.loc[0, "out_total_turnover"] == pytest.approx(
        summary.loc[1, "out_total_turnover"]
    )


def test_zero_cost_produces_zero_total_cost() -> None:
    summary = evaluate_costs(
        data=make_test_data(),
        transaction_costs=[0.0],
        split_date="2021-01-01",
        short_window=1,
        long_window=2,
    )

    assert summary.loc[0, "in_total_cost"] == pytest.approx(0.0)
    assert summary.loc[0, "out_total_cost"] == pytest.approx(0.0)


def test_positive_cost_produces_nonnegative_total_cost() -> None:
    summary = evaluate_costs(
        data=make_test_data(),
        transaction_costs=[0.001],
        split_date="2021-01-01",
        short_window=1,
        long_window=2,
    )

    assert summary.loc[0, "in_total_cost"] >= 0
    assert summary.loc[0, "out_total_cost"] >= 0


def test_evaluate_costs_rejects_empty_cost_list() -> None:
    with pytest.raises(
        ValueError,
        match="交易成本列表不能为空",
    ):
        evaluate_costs(
            data=make_test_data(),
            transaction_costs=[],
            split_date="2021-01-01",
            short_window=1,
            long_window=2,
        )


def test_evaluate_costs_rejects_negative_cost() -> None:
    with pytest.raises(
        ValueError,
        match="交易成本不能为负数",
    ):
        evaluate_costs(
            data=make_test_data(),
            transaction_costs=[-0.001],
            split_date="2021-01-01",
            short_window=1,
            long_window=2,
        )
