from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/raw/510300_unadjusted_20120101_20251231_20260713.csv"
)

OUTPUT_PATH = Path(
    "data/processed/510300_unadjusted.csv"
)

COLUMN_MAPPING = {
    "日期": "Date",
    "开盘": "Open",
    "最高": "High",
    "最低": "Low",
    "收盘": "Close",
    "成交量": "Volume",
}

REQUIRED_COLUMNS = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]


def main() -> None:
    data = pd.read_csv(INPUT_PATH)

    missing_source_columns = [
        column
        for column in COLUMN_MAPPING
        if column not in data.columns
    ]

    if missing_source_columns:
        raise ValueError(
            f"原始数据缺少列: {missing_source_columns}"
        )

    result = (
        data[list(COLUMN_MAPPING)]
        .rename(columns=COLUMN_MAPPING)
        .copy()
    )

    result["Date"] = pd.to_datetime(
        result["Date"],
        errors="raise",
    )

    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    for column in numeric_columns:
        result[column] = pd.to_numeric(
            result[column],
            errors="raise",
        )

    result = (
        result
        .sort_values("Date")
        .reset_index(drop=True)
    )

    if result["Date"].duplicated().any():
        raise ValueError("数据中存在重复日期")

    if result[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("必需列中存在缺失值")

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
        date_format="%Y-%m-%d",
        encoding="utf-8",
    )

    print(f"saved: {OUTPUT_PATH}")
    print(f"shape: {result.shape}")
    print(
        "date range:",
        result["Date"].min().date(),
        "->",
        result["Date"].max().date(),
    )
    print("columns:", result.columns.tolist())


if __name__ == "__main__":
    main()
