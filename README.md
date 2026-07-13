\# Backtest from Scratch



A beginner-friendly implementation of a basic quantitative backtesting workflow using fixed local price data.



\## Project Goals



\* Validate local historical price data

\* Calculate daily and cumulative returns

\* Build a moving-average strategy

\* Avoid look-ahead bias with `shift(1)`

\* Include turnover and transaction costs

\* Compare the strategy with buy-and-hold

\* Calculate basic performance metrics

\* Generate equity curve and drawdown charts

\* Verify core logic with unit tests



\## Project Structure



```text

backtest-from-scratch/

├── data/

├── outputs/

│   └── figures/

├── src/

├── tests/

├── README.md

├── requirements.txt

└── .gitignore

```



\## Installation



```powershell

python -m venv .venv

.venv\\Scripts\\Activate.ps1

python -m pip install -r requirements.txt

```



\## Run



Validate the data:



```powershell

python -m src.validate\_data

```



Run the moving-average backtest:



```powershell

python -m src.moving\_average\_strategy

```



Generate figures:



```powershell

python -m src.plot\_results

```



Run tests:



```powershell

python -m pytest

```



