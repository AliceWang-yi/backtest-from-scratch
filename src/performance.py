import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_performance(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
) -> dict:
    clean_returns = returns.dropna()

    total_periods = len(clean_returns)
    final_equity = (1 + clean_returns).prod()

    annual_return = final_equity ** (
        TRADING_DAYS / total_periods
    ) - 1

    annual_volatility = (
        clean_returns.std(ddof=1) * np.sqrt(TRADING_DAYS)
    )

    excess_return = clean_returns - risk_free_rate / TRADING_DAYS
    excess_volatility = excess_return.std(ddof=1)

    if excess_volatility == 0:
        sharpe_ratio = float("nan")
    else:
        sharpe_ratio = (
            excess_return.mean()
            / excess_volatility
            * np.sqrt(TRADING_DAYS)
        )
    equity_curve = (1 + clean_returns).cumprod()
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    max_drawdown = drawdown.min()
    return {
        "annual_return": annual_return,
        "annual_volatility": annual_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
    }

