import pandas as pd
import pytest

from src.split_sample import split_by_date


def test_split_by_date() -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2020-01-01",
                    "2020-01-02",
                    "2020-01-03",
                    "2020-01-04",
                ]
            ),
            "Close": [1.0, 2.0, 3.0, 4.0],
        }
    )

    in_sample, out_of_sample = split_by_date(
        data,
        split_date="2020-01-03",
    )

    assert in_sample["Date"].max() == pd.Timestamp("2020-01-02")
    assert out_of_sample["Date"].min() == pd.Timestamp("2020-01-03")
    assert len(in_sample) == 2
    assert len(out_of_sample) == 2


def test_split_rejects_empty_out_of_sample() -> None:
    data = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                ["2020-01-01", "2020-01-02"]
            ),
            "Close": [1.0, 2.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="样本外数据为空",
    ):
        split_by_date(
            data,
            split_date="2021-01-01",
        )
