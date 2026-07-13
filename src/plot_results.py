import matplotlib.pyplot as plt
import pandas as pd

from src.moving_average_strategy import run_moving_average_strategy


DATA_PATH = "data/sample_prices.csv"
OUTPUT_PATH = "outputs/figures/equity_curve.png"


prices = pd.read_csv(DATA_PATH, parse_dates=["Date"])
result = run_moving_average_strategy(prices)

plt.figure(figsize=(9, 5))
plt.plot(
    result["Date"],
    result["net_strategy_equity"],
    label="Moving Average Strategy",
)
plt.plot(
    result["Date"],
    result["buy_hold_equity"],
    label="Buy and Hold",
)

plt.title("Equity Curve Comparison")
plt.xlabel("Date")
plt.ylabel("Equity")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()
result["strategy_running_max"] = result["net_strategy_equity"].cummax()
result["strategy_drawdown"] = (
    result["net_strategy_equity"] / result["strategy_running_max"] - 1
)

plt.figure(figsize=(9, 5))
plt.plot(
    result["Date"],
    result["strategy_drawdown"],
    label="Strategy Drawdown",
)

plt.title("Strategy Drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/figures/drawdown.png", dpi=150)
plt.close()


print(f"Saved figure to: {OUTPUT_PATH}")
