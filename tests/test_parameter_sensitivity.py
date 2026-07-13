from pathlib import Path

import pandas as pd
import pytest

from src.parameter_sensitivity import (
    evaluate_parameters,
    save_parameter_sensitivity,
)


def make_test_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2020-12-24",
                    "2020-12-25",
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
                106.0,
                104.0,
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
                0.0095,
                -0.0189,
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
                1.06,
                1.04,
            ],
        }
    )


def test_evaluate_parameters_returns_one_row_per_pair() -> None:
    summary = evaluate_parameters(
        data=make_test_data(),
        parameters=[
            (1, 2),
            (2, 3),
        ],
        split_date="2021-01-01",
        transaction_cost=0.001,
    )

    assert len(summary) == 2
    assert summary["short_window"].tolist() == [1, 2]
    assert summary["long_window"].tolist() == [2, 3]


def test_evaluate_parameters_records_cost_in_bps() -> None:
    summary = evaluate_parameters(
        data=make_test_data(),
        parameters=[(1, 2)],
        split_date="2021-01-01",
        transaction_cost=0.001,
    )

    assert summary.loc[
        0,
        "transaction_cost_bps",
    ] == 10


def test_evaluate_parameters_includes_turnover_fields() -> None:
    summary = evaluate_parameters(
        data=make_test_data(),
        parameters=[(1, 2)],
        split_date="2021-01-01",
        transaction_cost=0.001,
    )

    assert "in_total_turnover" in summary.columns
    assert "out_total_turnover" in summary.columns
    assert summary.loc[0, "in_total_turnover"] >= 0
    assert summary.loc[0, "out_total_turnover"] >= 0


def test_evaluate_parameters_rejects_empty_parameter_list() -> None:
    with pytest.raises(
        ValueError,
        match="参数列表不能为空",
    ):
        evaluate_parameters(
            data=make_test_data(),
            parameters=[],
            split_date="2021-01-01",
            transaction_cost=0.001,
        )


def test_evaluate_parameters_rejects_invalid_window_order() -> None:
    with pytest.raises(
        ValueError,
        match="短期均线窗口必须小于长期均线窗口",
    ):
        evaluate_parameters(
            data=make_test_data(),
            parameters=[(3, 2)],
            split_date="2021-01-01",
            transaction_cost=0.001,
        )


def test_save_parameter_sensitivity_creates_csv(
    tmp_path: Path,
) -> None:
    summary = evaluate_parameters(
        data=make_test_data(),
        parameters=[(1, 2)],
        split_date="2021-01-01",
        transaction_cost=0.001,
    )

    output_path = (
        tmp_path
        / "tables"
        / "parameter_sensitivity.csv"
    )

    save_parameter_sensitivity(
        summary,
        output_path,
    )

    assert output_path.exists()

    loaded = pd.read_csv(output_path)

    assert len(loaded) == 1
    assert loaded.loc[0, "short_window"] == 1
    assert loaded.loc[0, "long_window"] == 2
