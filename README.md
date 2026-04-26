# Brew Intelligence — Coffee Shop Sales Dashboard

An interactive, single-file analytics dashboard built from six months of real transaction data across three NYC coffee shop locations. The dashboard visualises $698.8K in revenue, 149,116 transactions, and granular traffic patterns using Chart.js — no server required.

**Live demo:** open `CoffeDash.html` directly in any modern browser, or serve it via GitHub Pages.

---

## Project Overview

| Detail | Value |
|---|---|
| Dataset | Coffee Shop Sales.xlsx |
| Period | January – June 2023 |
| Locations | Astoria · Hell's Kitchen · Lower Manhattan |
| Transactions | 149,116 |
| Total Revenue | $698,812.33 |
| Stack | Vanilla HTML/CSS/JS · Chart.js 4.4 |

The project has two parts:

1. **`data_cleaning.py`** — Python script that ingests the raw Excel file, cleans it, derives computed columns, and exports seven CSV aggregates.
2. **`CoffeDash.html`** — Self-contained dashboard that embeds those aggregates as inline JavaScript and renders eight interactive chart types with filter controls.

---

## Data Cleaning Steps (`data_cleaning.py`)

Run the script once to produce all aggregates:

```bash
pip install pandas openpyxl
python data_cleaning.py
```

### Step-by-step

| Step | What it does | Why |
|---|---|---|
| **1. Load** | Reads `Coffee Shop Sales.xlsx` with `pandas.read_excel` | Raw source data |
| **2. Standardise column names** | Strips whitespace, lowercases, replaces spaces with underscores, removes special characters | Ensures consistent programmatic access |
| **3. Parse dates & times** | Converts `transaction_date` to `datetime64`, `transaction_time` to `time` objects | Enables temporal feature extraction |
| **4. Drop nulls** | Removes rows missing any of: date, time, store, category, product type, unit price, quantity | Prevents silent calculation errors |
| **5. Remove duplicates** | Deduplicates on `transaction_id` | Avoids double-counting transactions |
| **6. Validate numeric ranges** | Filters out rows where `transaction_qty ≤ 0` or `unit_price ≤ 0` | Removes data-entry errors and refund artefacts |
| **7. Derive columns** | Adds `revenue = qty × unit_price`, plus `hour`, `month`, `dow`, `date_str` | Avoids recomputing these in every aggregation |
| **8. Restrict to study period** | Keeps only Jan 1 – Jun 30 2023 | Removes any out-of-range test rows |
| **9. Standardise store names** | Strips whitespace; asserts exactly three expected location values | Guards against typos that would create phantom stores |
| **10. Standardise categories** | Applies `.str.title()` to product categories | Prevents case-mismatch splits (e.g. `"coffee"` vs `"Coffee"`) |
| **11. Sanity checks** | Asserts positive revenue, hours 0–23, months 1–6 | Fails fast if the source file changes unexpectedly |
| **12. Export aggregates** | Writes seven CSVs used by the dashboard | Separates heavy computation from the browser |

### Output files

| File | Contents |
|---|---|
| `agg_monthly.csv` | Orders and revenue per month |
| `agg_store_monthly.csv` | Orders and revenue per store × month |
| `agg_categories.csv` | Orders and revenue per product category |
| `agg_hourly.csv` | Orders and revenue per hour of day |
| `agg_dow.csv` | Orders and revenue per day of week |
| `agg_top_products.csv` | Top 10 product types by revenue |
| `agg_daily.csv` | Orders and revenue per calendar day (heatmap source) |

---

## Dashboard Charts

The dashboard has interactive filters for **Month**, **Store Location**, and **Product Category** that update all charts in real time.

### Key Performance Indicators (KPI row)

Five headline cards update with every filter change.

| Metric | Value |
|---|---|
| Total Revenue | **$698,812** (Jan $81.7K → Jun $166.5K) |
| Transactions | **149,116** |
| Avg. Transaction Value | **$4.69** |
| Peak Single Day | **1,343 orders** (Jun 19) |
| Top Product | **Barista Espresso** — $91,406 revenue |

---

### Chart 1 — Monthly Revenue by Location (Line)

**What it shows:** Per-store revenue trend across the six months, with each of the three locations as a separate filled line series.

**Insight:** All three stores grew in near-perfect lockstep — a 104% revenue increase from January to June — with no single location outpacing the others. This rules out location-specific promotions or events as the driver; the growth is system-wide.

---

### Chart 2 — Category Revenue Mix (Donut)

**What it shows:** Proportional share of total $698.8K revenue broken down by product category.

| Category | Revenue | Share |
|---|---|---|
| Coffee | $269,952 | 38.6% |
| Tea | $196,406 | 28.1% |
| Bakery | $82,316 | 11.8% |
| Drinking Chocolate | $72,416 | 10.4% |
| Coffee Beans | $40,085 | 5.7% |
| Other | $37,637 | 5.4% |

**Insight:** Coffee and Tea together account for nearly 67% of revenue. Drinking Chocolate punches above its weight in revenue per transaction — it averages $6.32 per order vs. $4.69 overall.

---

### Chart 3 — Hourly Traffic Pattern (Bar + Line)

**What it shows:** A dual-axis combo chart with order count (bars, left axis) and revenue (line, right axis) for each hour from 6 AM to 8 PM. The 8–10 AM window is highlighted.

**Insight:** The morning rush window (8–10 AM) drives a disproportionate share of daily volume. The 10:00 hour alone accounts for 18,545 orders — the single busiest hour. Traffic drops sharply after 11 AM and is nearly absent after 7 PM. Staffing and inventory should be weighted heavily toward the first four hours of the day.

---

### Chart 4 — Day of Week Revenue (Bar)

**What it shows:** Total revenue aggregated by day of the week across all six months, Monday through Sunday.

**Insight:** Revenue is remarkably stable across the working week ($99K–$102K per day). Monday is the highest-revenue day ($101.7K total). Saturday is the quietest day ($96.9K), representing a clear opportunity for weekend promotions or loyalty-day offers.

---

### Chart 5 — Store Revenue by Month (Grouped Bar)

**What it shows:** Side-by-side monthly revenue bars for each of the three locations, making month-over-month growth visible per store.

**Insight:** Hell's Kitchen consistently edges ahead in monthly revenue (e.g. $56,957 in June vs. $55,083 for Astoria and $54,446 for Lower Manhattan), but the margin is under 4%. No store has a meaningful structural advantage — operational decisions can be applied uniformly.

---

### Chart 6 — Top 10 Product Types (Horizontal Bar)

**What it shows:** The ten highest-grossing product types ranked by total revenue, colour-coded by category.

| Rank | Product | Category | Revenue |
|---|---|---|---|
| 1 | Barista Espresso | Coffee | $91,406 |
| 2 | Brewed Chai Tea | Tea | $77,082 |
| 3 | Hot Chocolate | Drinking Chocolate | $72,416 |
| 4 | Gourmet Brewed Coffee | Coffee | $70,035 |
| 5 | Brewed Black Tea | Tea | $47,932 |
| 6 | Brewed Herbal Tea | Tea | $47,540 |
| 7 | Premium Brewed Coffee | Coffee | $38,781 |
| 8 | Organic Brewed Coffee | Coffee | $37,747 |
| 9 | Scone | Bakery | $36,866 |
| 10 | Drip Coffee | Coffee | $31,984 |

**Insight:** The top 3 products alone generate $240.9K — 34% of all revenue. Tea occupies three of the top six slots, suggesting it is underweighted in marketing relative to its sales performance.

---

### Chart 7 — Category Revenue Growth (Stacked Bar)

**What it shows:** Monthly revenue stacked by category (Coffee, Tea, Bakery, Drinking Chocolate), making both absolute growth and relative category mix visible over time.

**Insight:** All four categories grew proportionally — the mix remained stable at roughly 46% Coffee, 33% Tea, 14% Bakery, and 12% Chocolate across every month. The growth is volume-driven, not a shift in customer preference.

---

### Chart 8 — Store Performance Radar

**What it shows:** A five-axis radar chart normalising each store across Revenue Score, Order Volume, Average Price, June Growth Rate, and Consistency.

**Insight:** The three polygons overlap almost completely, confirming operational parity across locations. All stores score ~95 on Consistency. Hell's Kitchen scores marginally higher on Growth (it had the best Jan→Jun ratio), making it the leading candidate to pilot new initiatives.

---

### Chart 9 — Daily Orders Heatmap

**What it shows:** A calendar grid (rows = months, columns = day-of-month) where each cell's colour intensity encodes that day's total order count. Hovering shows the exact date, order count, and revenue.

**Insight:** The January–February period is visibly lighter (lower intensity) than May–June, confirming the seasonal ramp-up. There are no blank gaps or anomalously dead days — the business operated every day of the six-month period without closures.

---

### Chart 10 — Store Scorecard (Table + Progress Bars)

**What it shows:** A summary table of revenue, transaction count, and revenue share per location, with horizontal bar indicators.

**Insight:** Revenue share is nearly a perfect three-way split — Hell's Kitchen 33.8%, Astoria 33.2%, Lower Manhattan 32.9% — suggesting consistent brand execution and pricing across all outlets.

---

## Key Metrics Summary

| Metric | Value |
|---|---|
| Total revenue (6 months) | $698,812 |
| Monthly revenue range | $76,145 (Feb) – $166,486 (Jun) |
| Revenue growth Jan→Jun | +104% |
| Total transactions | 149,116 |
| Average transaction value | $4.69 |
| Peak hour | 10:00 AM (18,545 orders) |
| Peak day of week | Monday ($101,677) |
| Quietest day | Saturday ($96,894) |
| Peak single day | Jun 19 — 1,343 orders |
| Top revenue store | Hell's Kitchen — $236,511 |
| Top product | Barista Espresso — $91,406 |
| Top category | Coffee — $269,952 (38.6%) |
| Bakery attach rate | 22,796 transactions alongside beverages |

---

## Deploying to GitHub Pages

### 1. Create a GitHub repository

```bash
git init
git add CoffeDash.html README.md data_cleaning.py
git commit -m "Initial commit: Brew Intelligence dashboard"
```

### 2. Push to GitHub

```bash
gh repo create coffee-dashboard --public --source=. --remote=origin --push
# or manually:
git remote add origin https://github.com/<your-username>/coffee-dashboard.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to your repository on GitHub.
2. Click **Settings** → **Pages** (left sidebar).
3. Under **Source**, select **Deploy from a branch**.
4. Set **Branch** to `main` and **folder** to `/ (root)`.
5. Click **Save**.

GitHub will build and publish the site. After ~60 seconds your dashboard will be live at:

```
https://<your-username>.github.io/coffee-dashboard/CoffeDash.html
```

### 4. Rename for a cleaner URL (optional)

Rename `CoffeDash.html` to `index.html` so the site loads at the root URL without specifying the filename:

```bash
mv CoffeDash.html index.html
git add -A
git commit -m "Rename to index.html for GitHub Pages root URL"
git push
```

Your dashboard will then be accessible at:

```
https://<your-username>.github.io/coffee-dashboard/
```

No build step, no dependencies, no server — the dashboard is a single file and works anywhere static HTML is served.

---

## File Structure

```
coffee-dashboard/
├── CoffeDash.html        # Self-contained interactive dashboard
├── data_cleaning.py      # Data ingestion, cleaning & aggregation script
├── Coffee Shop Sales.xlsx # Raw source data 
└── README.md             # This file
```
