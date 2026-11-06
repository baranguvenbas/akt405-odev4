import calendar
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

import pandas as pd
import yfinance as yf


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "kapanis.csv"
START_DATE = "2021-01-01"
END_DATE = "2026-01-01"

ASSETS = {
    "Altin": "GC=F",
    "Sabanci_Holding": "SAHOL.IS",
    "Tahvil_ETF": "TLT",
}


def fetch_chart_price(ticker: str) -> pd.Series:
    period1 = calendar.timegm(datetime(2021, 1, 1, tzinfo=timezone.utc).timetuple())
    period2 = calendar.timegm(datetime(2026, 1, 1, tzinfo=timezone.utc).timetuple())
    url = (
        f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={period1}&period2={period2}&interval=1d"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)

    result = payload["chart"]["result"][0]
    timestamps = result["timestamp"]
    indicators = result["indicators"]
    adjusted = indicators["adjclose"][0]["adjclose"]
    closes = indicators["quote"][0]["close"]
    values = adjusted if any(value is not None for value in adjusted) else closes
    series = pd.Series(values, index=pd.to_datetime(timestamps, unit="s", utc=True))
    series.index = series.index.tz_localize(None)
    series.index = series.index.normalize()
    series.name = ticker
    return series.dropna()


def main() -> None:
    print("Veri çekiliyor...")
    print(f"Semboller: {ASSETS}")

    try:
        prices = yf.download(
            list(ASSETS.values()),
            start=START_DATE,
            end=END_DATE,
            auto_adjust=True,
            progress=False,
            group_by="column",
            threads=True,
        )
        if isinstance(prices.columns, pd.MultiIndex):
            close_prices = prices["Close"].copy()
        else:
            close_prices = prices[["Close"]].copy()
            close_prices.columns = [next(iter(ASSETS.values()))]
    except Exception as error:
        print(f"yfinance hatası: {type(error).__name__}: {error}")
        close_prices = pd.DataFrame()

    if close_prices.empty:
        print("Yahoo chart yedek uç noktası kullanılıyor...")
        close_prices = pd.DataFrame(
            {ticker: fetch_chart_price(ticker) for ticker in ASSETS.values()}
        )

    close_prices = close_prices.rename(
        columns={ticker: name for name, ticker in ASSETS.items()}
    )
    close_prices = close_prices.dropna()
    close_prices.index = pd.to_datetime(close_prices.index).tz_localize(None)
    close_prices.index.name = "Tarih"
    close_prices = close_prices.sort_index()
    close_prices = close_prices.loc[START_DATE:"2025-12-31"]

    if close_prices.empty:
        raise RuntimeError("Seçilen semboller için geçerli veriye ulaşılamadı.")

    close_prices.to_csv(OUTPUT_FILE, encoding="utf-8-sig", date_format="%Y-%m-%d")
    print(f"Ortak işlem günü sayısı: {len(close_prices)}")
    print(f"Veri kaydedildi: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
