import pandas as pd


def split_by_date(
    data: pd.DataFrame,
    split_date: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    result = data.copy()
    result["Date"] = pd.to_datetime(result["Date"])

    split_timestamp = pd.Timestamp(split_date)

    in_sample = result[
        result["Date"] < split_timestamp
    ].copy()

    out_of_sample = result[
        result["Date"] >= split_timestamp
    ].copy()

    if in_sample.empty:
        raise ValueError("样本内数据为空")

    if out_of_sample.empty:
        raise ValueError("样本外数据为空")

    return (
        in_sample.reset_index(drop=True),
        out_of_sample.reset_index(drop=True),
    )
