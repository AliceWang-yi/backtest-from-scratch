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
## 正式历史数据候选

- 标的：沪深300ETF华泰柏瑞
- 证券代码：510300
- 市场：上海证券交易所
- 数据频率：日频
- 数据来源：东方财富
- 获取工具：AKShare
- 接口：`fund_etf_hist_em`
- 下载日期：2026-07-13
- 请求日期范围：2012-01-01 至 2025-12-31
- 实际日期范围：以数据验证输出为准
- 当前价格处理：不复权
- 原始文件：`data/raw/510300_unadjusted_20120101_20251231_20260713.csv`
- 标准化候选文件：`data/processed/510300_unadjusted.csv`

当前文件只作为正式数据候选，不作为最终回测输入。

不复权价格可能在分红除权日产生非投资损失意义上的价格跳变，因此在明确收益口径前，不应直接用它评价策略表现。




