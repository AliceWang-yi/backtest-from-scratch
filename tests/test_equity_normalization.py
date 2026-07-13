import pandas as pd
import pytest

from src.equity_normalization import normalize_period_equity


def make_equity_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                ]
            ),
            "net_strategy_equity": [
                1.20,
                1.26,
                1.14,
            ],
            "buy_hold_equity": [
                1.50,
                1.65,
                1.80,
            ],
        }
    )


def test_normalized_equity_starts_at_one() -> None:
    result = normalize_period_equity(make_equity_data())

    assert result.loc[
        0,
        "normalized_net_strategy_equity",
    ] == pytest.approx(1.0)

    assert result.loc[
        0,
        "normalized_buy_hold_equity",
    ] == pytest.approx(1.0)


def test_normalized_equity_preserves_relative_change() -> None:
    result = normalize_period_equity(make_equity_data())

    assert result.loc[
        2,
        "normalized_net_strategy_equity",
    ] == pytest.approx(1.14 / 1.20)

    assert result.loc[
        2,
        "normalized_buy_hold_equity",
    ] == pytest.approx(1.80 / 1.50)


def test_normalization_sorts_dates() -> None:
    data = make_equity_data().iloc[::-1].reset_index(drop=True)

    result = normalize_period_equity(data)

    assert result["Date"].is_monotonic_increasing
    assert result.loc[
        0,
        "normalized_net_strategy_equity",
    ] == pytest.approx(1.0)


def test_normalization_does_not_modify_input() -> None:
    data = make_equity_data()
    original = data.copy(deep=True)

    normalize_period_equity(data)

    pd.testing.assert_frame_equal(data, original)


def test_normalization_rejects_empty_data() -> None:
    data = pd.DataFrame(
        columns=[
            "Date",
            "net_strategy_equity",
            "buy_hold_equity",
        ]
    )

    with pytest.raises(
        ValueError,
        match="净值归一化数据不能为空",
    ):
        normalize_period_equity(data)


def test_normalization_rejects_missing_equity_column() -> None:
    data = make_equity_data().drop(
        columns=["buy_hold_equity"]
    )

    with pytest.raises(
        ValueError,
        match="缺少净值归一化所需列",
    ):
        normalize_period_equity(data)


def test_normalization_rejects_nonpositive_first_equity() -> None:
    data = make_equity_data()
    data.loc[0, "net_strategy_equity"] = 0.0

    with pytest.raises(
        ValueError,
        match="区间第一天净值必须为正数",
    ):
        normalize_period_equity(data)
