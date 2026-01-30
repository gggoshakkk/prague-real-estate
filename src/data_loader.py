"""Load and clean sreality JSON; extract district from address."""
import re
from pathlib import Path

import pandas as pd

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "dataset_sreality-scraper_2026-01-30_12-54-43-532.json"
DISTRICT_PATTERN = re.compile(r"Praha\s*(\d{1,2})")


def extract_district(address: str) -> str | None:
    """Extract district (e.g. 'Praha 1') from address string."""
    if pd.isna(address) or not isinstance(address, str):
        return None
    match = DISTRICT_PATTERN.search(address)
    if match is None:
        return None
    return f"Praha {match.group(1)}"


def load_and_clean(path: str | Path | None = None) -> pd.DataFrame:
    """
    Load JSON, add district column, drop invalid rows.
    Returns DataFrame with at least: address, price, size_m2, gps_lat, gps_lon, condition, url, district.
    """
    p = Path(path) if path is not None else DEFAULT_DATA_PATH
    df = pd.read_json(p)

    # Extract district from address
    df["district"] = df["address"].astype(str).map(extract_district)

    # Drop rows with missing or invalid price
    df = df.dropna(subset=["price"])
    df = df[df["price"].gt(0)]

    # Drop rows with missing or invalid size_m2
    df = df.dropna(subset=["size_m2"])
    df = df[df["size_m2"].gt(0)]

    # Drop rows where district could not be parsed
    df = df.dropna(subset=["district"])

    return df.reset_index(drop=True)
