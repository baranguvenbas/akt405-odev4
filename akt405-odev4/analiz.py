from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
PRICE_FILE = BASE_DIR / "kapanis.csv"
PRICE_PLOT_FILE = BASE_DIR / "fiyatlar.png"
TRADING_DAYS = 252


def load_prices() -> pd.DataFrame:
    prices = pd.read_csv(PRICE_FILE, index_col="Tarih", parse_dates=True)
    prices = prices.dropna()
    if prices.empty:
        raise ValueError("kapanis.csv içinde analiz edilecek veri bulunamadı.")
    return prices


def calculate_returns(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    simple_returns = prices.pct_change().dropna()
    log_returns = np.log(prices / prices.shift(1)).dropna()
    return simple_returns, log_returns


def print_risk_table(log_returns: pd.DataFrame) -> None:
    annual_mean = log_returns.mean() * TRADING_DAYS
    annual_volatility = log_returns.std(ddof=1) * np.sqrt(TRADING_DAYS)
    summary = pd.DataFrame(
        {
            "Yıllık Ortalama Getiri": annual_mean,
            "Yıllık Oynaklık": annual_volatility,
        }
    )
    print("\nYıllık Ortalama Getiri ve Oynaklık:")
    print(summary.to_string(float_format=lambda value: f"{value:.4%}"))


def demonstrate_equivalent_gold_return(prices: pd.DataFrame, log_returns: pd.DataFrame) -> None:
    gold_prices = prices.iloc[:, 0]
    log_prices_total = np.exp(log_returns.iloc[:, 0].sum()) - 1
    direct_total = gold_prices.iloc[-1] / gold_prices.iloc[0] - 1

    print("\nAltın toplam getiri karşılaştırması:")
    print(f"Pt/P0 - 1:                         {direct_total:.6%}")
    print(f"exp(toplam(log getiriler)) - 1:    {log_prices_total:.6%}")


def plot_normalized_prices(prices: pd.DataFrame) -> None:
    normalized = prices / prices.iloc[0] * 100
    ax = normalized.plot(figsize=(12, 7), linewidth=1.8)
    ax.set_title("Seçilen Varlıkların Endeksli Kapanış Fiyatları (Başlangıç=100)")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Endeksli Fiyat (Başlangıç = 100)")
    ax.legend(title="Varlıklar")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(PRICE_PLOT_FILE, dpi=180)
    plt.close()
    print(f"\nGrafik kaydedildi: {PRICE_PLOT_FILE}")


def main() -> None:
    prices = load_prices()
    simple_returns, log_returns = calculate_returns(prices)

    print_risk_table(log_returns)
    demonstrate_equivalent_gold_return(prices, log_returns)
    plot_normalized_prices(prices)

    print("\nBasit Günlük Getirilerin Korelasyon Matrisi:")
    print(simple_returns.corr().to_string(float_format=lambda value: f"{value:.4f}"))


if __name__ == "__main__":
    main()
