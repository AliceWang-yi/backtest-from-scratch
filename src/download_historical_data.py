from pathlib import Path

import akshare as ak


SYMBOL = "510300"
START_DATE = "20120101"
END_DATE = "20251231"
DOWNLOAD_DATE = "20260713"

ADJUSTMENTS = {
    "unadjusted": "",
    "qfq": "qfq",
    "hfq": "hfq",
}


def main() -> None:
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, adjust in ADJUSTMENTS.items():
        data = ak.fund_etf_hist_em(
            symbol=SYMBOL,
            period="daily",
            start_date=START_DATE,
            end_date=END_DATE,
            adjust=adjust,
        )

        output_path = output_dir / (
            f"{SYMBOL}_{name}_{START_DATE}_{END_DATE}_{DOWNLOAD_DATE}.csv"
        )

        data.to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig",
        )

        print(f"saved: {output_path}")
        print(f"shape: {data.shape}")
        print(f"date range: {data['日期'].iloc[0]} -> {data['日期'].iloc[-1]}")
        print()


if __name__ == "__main__":
    main()
