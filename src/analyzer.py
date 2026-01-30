"""Arbitrage logic: price per m², district median, arbitrage score, hot deals."""
import pandas as pd

HOT_DEAL_THRESHOLD = 0.05  # 5% below district median
TOP_HOT_DEAL_PERCENT = 1.0  # 100% of hot deals shown on map (all deals)


def analyze(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add price_per_m2, district_median_price_m2, arbitrage_score, is_hot_deal.
    arbitrage_score = (district_median - listing_price_m2) / district_median (positive = cheaper).
    """
    df = df.copy()
    df["price_per_m2"] = df["price"] / df["size_m2"]

    district_median = df.groupby("district")["price_per_m2"].transform("median")
    df["district_median_price_m2"] = district_median

    df["arbitrage_score"] = (
        df["district_median_price_m2"] - df["price_per_m2"]
    ) / df["district_median_price_m2"]

    df["is_hot_deal"] = df["arbitrage_score"] > HOT_DEAL_THRESHOLD

    return df


def top_hot_deals(df: pd.DataFrame, fraction: float = TOP_HOT_DEAL_PERCENT) -> pd.DataFrame:
    """Return top fraction (e.g. 100%) of hot deals by arbitrage_score (highest first)."""
    hot = df[df["is_hot_deal"]].copy()
    if hot.empty:
        return hot
    n = max(1, int(len(hot) * fraction))
    return hot.nlargest(n, "arbitrage_score").reset_index(drop=True)
