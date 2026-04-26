import pandas as pd

# ── 1. Load raw data ──────────────────────────────────────────────────────────
df = pd.read_excel("Coffee Shop Sales.xlsx")
print(f"Loaded {len(df):,} rows × {df.shape[1]} columns")
print(df.dtypes, "\n")

# ── 2. Standardise column names ───────────────────────────────────────────────
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)
# Expected columns after rename:
#   transaction_id, transaction_date, transaction_time, transaction_qty,
#   store_id, store_location, product_id, unit_price, product_category,
#   product_type, product_detail

# ── 3. Parse date & time ──────────────────────────────────────────────────────
df["transaction_date"] = pd.to_datetime(df["transaction_date"], dayfirst=False)
df["transaction_time"] = pd.to_datetime(
    df["transaction_time"], format="%H:%M:%S", errors="coerce"
).dt.time

# ── 4. Drop rows missing critical fields ─────────────────────────────────────
critical = ["transaction_date", "transaction_time", "store_location",
            "product_category", "product_type", "unit_price", "transaction_qty"]
before = len(df)
df = df.dropna(subset=critical)
print(f"Dropped {before - len(df)} rows with missing critical fields")

# ── 5. Remove duplicates ──────────────────────────────────────────────────────
before = len(df)
df = df.drop_duplicates(subset=["transaction_id"])
print(f"Dropped {before - len(df)} duplicate transaction_id rows")

# ── 6. Validate & filter numeric ranges ──────────────────────────────────────
# Reject non-positive quantities or prices (data-entry errors)
before = len(df)
df = df[(df["transaction_qty"] > 0) & (df["unit_price"] > 0)]
print(f"Dropped {before - len(df)} rows with invalid qty/price")

# ── 7. Derive computed columns ────────────────────────────────────────────────
df["revenue"] = df["transaction_qty"] * df["unit_price"]
df["hour"]    = df["transaction_time"].apply(lambda t: t.hour if pd.notna(t) else None)
df["month"]   = df["transaction_date"].dt.month
df["dow"]     = df["transaction_date"].dt.dayofweek   # 0=Monday … 6=Sunday
df["date_str"]= df["transaction_date"].dt.strftime("%Y-%m-%d")

# ── 8. Restrict to study period (Jan–Jun 2023) ────────────────────────────────
before = len(df)
df = df[
    (df["transaction_date"] >= "2023-01-01") &
    (df["transaction_date"] <= "2023-06-30")
]
print(f"Dropped {before - len(df)} rows outside Jan–Jun 2023 window")

# ── 9. Standardise store names (trim whitespace) ─────────────────────────────
df["store_location"] = df["store_location"].str.strip()
assert set(df["store_location"].unique()) == {"Astoria", "Hell's Kitchen", "Lower Manhattan"}, \
    "Unexpected store location values found"

# ── 10. Standardise category capitalisation ───────────────────────────────────
df["product_category"] = df["product_category"].str.strip().str.title()
df["product_type"]     = df["product_type"].str.strip()

# ── 11. Sanity checks ─────────────────────────────────────────────────────────
assert df["revenue"].min() > 0,         "Negative revenue found"
assert df["hour"].between(0, 23).all(), "Hour values out of range"
assert df["month"].between(1, 6).all(), "Month values out of range"
print(f"\nFinal clean dataset: {len(df):,} transactions")
print(f"Date range: {df['transaction_date'].min().date()} → {df['transaction_date'].max().date()}")
print(f"Total revenue: ${df['revenue'].sum():,.2f}")

# ── 12. Export aggregates used by the dashboard ───────────────────────────────

# Monthly totals
monthly = (
    df.groupby("month")
    .agg(orders=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
)
monthly.to_csv("agg_monthly.csv", index=False)

# Store × Month
store_monthly = (
    df.groupby(["month", "store_location"])
    .agg(orders=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
)
store_monthly.to_csv("agg_store_monthly.csv", index=False)

# Category totals
cat_totals = (
    df.groupby("product_category")
    .agg(orders=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
    .sort_values("revenue", ascending=False)
)
cat_totals.to_csv("agg_categories.csv", index=False)

# Hourly pattern
hourly = (
    df.groupby("hour")
    .agg(orders=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
    .sort_values("hour")
)
hourly.to_csv("agg_hourly.csv", index=False)

# Day-of-week pattern
dow = (
    df.groupby("dow")
    .agg(orders=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
    .sort_values("dow")
)
dow.to_csv("agg_dow.csv", index=False)

# Top product types
products = (
    df.groupby(["product_type", "product_category"])
    .agg(orders=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
    .sort_values("revenue", ascending=False)
    .head(10)
)
products.to_csv("agg_top_products.csv", index=False)

# Daily totals (heatmap source)
daily = (
    df.groupby("date_str")
    .agg(orders=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
    .sort_values("date_str")
)
daily.to_csv("agg_daily.csv", index=False)

print("\nAll aggregates exported to CSV.")
