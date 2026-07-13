import argparse

import pandas as pd


def validate_data(file_path: str) -> None:
    df = pd.read_csv(file_path, parse_dates=["Date"])

    print("File:", file_path)
    print("Shape:", df.shape)
    print("Date range:", df["Date"].min(), "to", df["Date"].max())
    print("Columns:", df.columns.tolist())
    print("Missing values:")
    print(df.isna().sum())
    print("Duplicate rows:", df.duplicated().sum())
    print("Duplicate dates:", df["Date"].duplicated().sum())
    print("Dates sorted:", df["Date"].is_monotonic_increasing)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path",
        nargs="?",
        default="data/sample_prices.csv",
    )
    args = parser.parse_args()

    validate_data(args.file_path)


