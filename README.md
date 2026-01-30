# Prague Real Estate Arbitrage Analyzer

A data pipeline that finds **underpriced apartment listings** in Prague by comparing each listing’s price per m² to its district median. It outputs an interactive map with a market heatmap and highlighted “hot deals”—listings priced meaningfully below their district benchmark.

---

## Overview

In a high-price market (e.g. median 125k–140k CZK/m²), this tool does not just list properties: it computes **arbitrage score**—the percentage each listing is below its district’s median price/m²—and flags deals that exceed a configurable threshold (default: 5% below district median). All hot deals can be shown on the map for a detailed, district-aware view of value.

**Features:**

- Load and clean sreality-style JSON (district extraction from address, validation of price and size)
- Per-district median price/m² and per-listing arbitrage score
- Configurable hot-deal threshold and share of deals shown on the map (e.g. 100% of hot deals)
- Interactive Folium map: heatmap of all listings + layer of hot deals with popups (address, price, size, arbitrage %, link to listing)

---

## Map preview

GitHub does not render interactive HTML in the README. You can integrate the map in two ways:

1. **Screenshot**  
   After running the pipeline, open `map.html` in a browser, take a screenshot, and add it as `docs/map-preview.png`. It will appear below:

   ![Map preview](docs/map-preview.png)

2. **Live map (GitHub Pages)**  
   Enable [GitHub Pages](https://docs.github.com/en/pages) for this repo (e.g. “Deploy from branch” → branch `main`, folder `/ (root)` or `/docs`). Commit `map.html` (or build it in CI and publish it). Then add a link in this section, e.g.:

   **[View live map](https://YOUR_USERNAME.github.io/real_estate_prague/map.html)**

---

## Requirements

- **Python** 3.10+
- **Data:** JSON export from an sreality-style scraper with at least: `address`, `price`, `size_m2`, `gps_lat`, `gps_lon`, `condition`, `url`. Addresses must contain a district in the form “Praha N” (e.g. “Praha 1”, “Praha 4”) so the loader can extract the district.

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/real_estate_prague.git
cd real_estate_prague

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Data

Place your scraper JSON in the `data/` directory, e.g.:

```text
data/
  dataset_sreality-scraper_2026-01-30_12-54-43-532.json
```

The loader uses the default path in `src/data_loader.py` or you can pass a custom path when calling the loader. Rows with missing or invalid `price`, `size_m2`, or unparseable district (no “Praha N” in `address`) are dropped.

---

## Usage

From the project root:

```bash
python main.py
```

This will:

1. Load and clean the JSON (extract district, drop invalid rows)
2. Compute price/m², district medians, arbitrage score, and hot-deal flags
3. Generate `map.html` (heatmap + hot-deal markers with popups)

Open `map.html` in a browser to explore the map and toggle layers. The console prints the number of listings, hot deals, and how many of them are shown on the map.

---

## Project structure

| Path | Description |
|------|-------------|
| `main.py` | Entry point: load → analyze → build map |
| `src/data_loader.py` | Load JSON, extract district from address, filter invalid rows |
| `src/analyzer.py` | Price/m², district median, arbitrage score, hot-deal threshold and top-% logic |
| `src/visualizer.py` | Folium map: heatmap layer + hot-deal markers and popups |
| `data/` | Input JSON (e.g. sreality scraper export) |
| `requirements.txt` | Python dependencies (pandas, folium, numpy, plotly) |

Threshold and “top %” of hot deals shown on the map are set in `src/analyzer.py` (`HOT_DEAL_THRESHOLD`, `TOP_HOT_DEAL_PERCENT`).

---

## License

Use and adapt as needed. If you publish a live map or a dataset, please respect the data source’s terms (e.g. sreality.cz).
