"""Entry point: load data, analyze arbitrage, generate map."""
from pathlib import Path

from src.data_loader import load_and_clean
from src.analyzer import analyze, top_hot_deals
from src.visualizer import build_map

DATA_PATH = Path(__file__).resolve().parent / "data" / "dataset_sreality-scraper_2026-01-30_12-54-43-532.json"
MAP_PATH = Path(__file__).resolve().parent / "map.html"


def main() -> None:
    df = load_and_clean(DATA_PATH)
    df = analyze(df)

    build_map(df, output_path=MAP_PATH)

    n_listings = len(df)
    n_hot = df["is_hot_deal"].sum()
    n_top5 = len(top_hot_deals(df))
    print(f"Listings: {n_listings}")
    print(f"Hot deals (≥5% below district median): {n_hot}")
    print(f"Hot deals shown on map (100%): {n_top5}")
    print(f"Map saved to: {MAP_PATH}")


if __name__ == "__main__":
    main()
