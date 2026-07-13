import pandas as pd
import math


from src.performance import calculate_performance


def test_zero_returns():
    returns = pd.Series([0.0, 0.0, 0.0, 0.0])

    result = calculate_performance(returns)

    assert result["annual_return"] == 0.0
    assert result["annual_volatility"] == 0.0
    assert math.isnan(result["sharpe_ratio"])
def test_max_drawdown():
    returns = pd.Series([0.1, -0.2, 0.05])

    result = calculate_performance(returns)

    assert round(result["max_drawdown"], 6) == -0.2

