import pandas as pd


DATA_PATH = "data/sample_prices.csv"


df = pd.read_csv(DATA_PATH, parse_dates=["Date"])

print("File:", DATA_PATH)
print("Shape:", df.shape)
print("Date range:", df["Date"].min(), "to", df["Date"].max())
print("Columns:", df.columns.tolist())
print("Missing values:")
print(df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate dates:", df["Date"].duplicated().sum())
print("Dates sorted:", df["Date"].is_monotonic_increasing)
