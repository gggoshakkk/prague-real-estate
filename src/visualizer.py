"""Folium map: heatmap of all listings, prominent markers for top hot deals, popups."""
from pathlib import Path

import folium
import pandas as pd
from folium.plugins import HeatMap

from .analyzer import top_hot_deals

PRAGUE_CENTER = [50.0755, 14.4378]
DEFAULT_MAP_PATH = Path(__file__).resolve().parent.parent / "map.html"


def _popup_html(row: pd.Series) -> str:
    """Build popup HTML: address, price, size, arbitrage %, link."""
    score_pct = row.get("arbitrage_score")
    if score_pct is not None and not pd.isna(score_pct):
        score_str = f"{score_pct * 100:.1f}% below market"
    else:
        score_str = "—"
    addr = row.get("address", "")
    price = row.get("price")
    size = row.get("size_m2")
    price_str = f"{price:,.0f} CZK" if price is not None and not pd.isna(price) else "—"
    size_str = f"{int(size)} m²" if size is not None and not pd.isna(size) else "—"
    url = row.get("url", "")
    link = f'<a href="{url}" target="_blank">View listing</a>' if url else ""
    return (
        f"<b>{addr}</b><br>"
        f"Price: {price_str} | Size: {size_str}<br>"
        f"{score_str}<br>"
        f"{link}"
    )


def build_map(
    df: pd.DataFrame,
    output_path: str | Path | None = None,
) -> folium.Map:
    """
    Build Folium map: Layer 1 = heatmap of all properties, Layer 2 = hot deals (100%, red markers).
    Popups show address, price, size, arbitrage %, and link to url.
    Saves to output_path (default: map.html next to project root).
    """
    out = Path(output_path) if output_path is not None else DEFAULT_MAP_PATH

    # Drop rows without valid coordinates for map
    map_df = df.dropna(subset=["gps_lat", "gps_lon"]).copy()
    map_df = map_df[
        map_df["gps_lat"].between(-90, 90) & map_df["gps_lon"].between(-180, 180)
    ]

    m = folium.Map(location=PRAGUE_CENTER, zoom_start=12)

    # Layer 1: Market overview (heatmap)
    heat_data = map_df[["gps_lat", "gps_lon"]].assign(weight=1).values.tolist()
    fg_overview = folium.FeatureGroup(name="Market overview")
    HeatMap(heat_data, radius=12, blur=18).add_to(fg_overview)
    fg_overview.add_to(m)

    # Layer 2: Hot deals (100% — all deals meeting threshold, red/fire markers with popups)
    top_deals = top_hot_deals(map_df)
    fg_deals = folium.FeatureGroup(name="Hot deals (100%)")
    for _, row in top_deals.iterrows():
        lat, lon = row["gps_lat"], row["gps_lon"]
        popup = folium.Popup(_popup_html(row), max_width=300)
        folium.Marker(
            [lat, lon],
            popup=popup,
            icon=folium.Icon(color="red", icon="fire"),
        ).add_to(fg_deals)
    fg_deals.add_to(m)

    folium.LayerControl().add_to(m)
    m.save(str(out))
    return m
