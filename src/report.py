import pandas as pd

from src.moving_average_strategy import run_moving_average_strategy
from src.performance import calculate_performance


DATA_PATH = "data/sample_prices.csv"


prices = pd.read_csv(DATA_PATH, parse_dates=["Date"])

result = run_moving_average_strategy(prices)

strategy_report = calculate_performance(
    result["net_strategy_return"]
)

benchmark_report = calculate_performance(
    result["buy_hold_return"]
)


print("Strategy Performance")
print("====================")
for key, value in strategy_report.items():
    print(f"{key}: {value:.4f}")


print("\nBuy and Hold Performance")
print("========================")
for key, value in benchmark_report.items():
    print(f"{key}: {value:.4f}")
