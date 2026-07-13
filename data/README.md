\# Data Specification



\## Development Data



`sample\_prices.csv` is a small synthetic dataset used only for testing the code workflow.



It must not be used to evaluate strategy performance.



\## Final Backtest Data



The final local price file should be named:



`historical\_prices.csv`



Required columns:



\- `Date`

\- `Open`

\- `High`

\- `Low`

\- `Close`

\- `Volume`



Requirements:



\- One row per trading day

\- Dates sorted from earliest to latest

\- No duplicate dates

\- Prices must be positive

\- Volume must be non-negative

\- No missing values in required columns

\- Prices must use a consistent adjustment convention

\- The asset name, source, download date, and adjustment method must be documented



