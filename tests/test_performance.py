import pandas as pd
import math


from src.performance import calculate_performance


def test_zero_returns():
    returns = pd.Series([0.0, 0.0, 0.0, 0.0])

    result = calculate_performance(returns)

    assert result["annual_return"] == 0.0
    assert result["annual_volatility"] == 0.0
    assert math.isnan(result["sharpe_ratio"])

