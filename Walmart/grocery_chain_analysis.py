import os
import pandas as pd
import matplotlib.pyplot as plt

# === SETTINGS ===
INPUT_CSV = "grocery_chain_data.csv"  # Path to your CSV file
OUT_DIR = "grocery_charts_outputs"
PLOTS_DIR = os.path.join(OUT_DIR, "plots")

# === SETUP ===
os.makedirs(PLOTS_DIR, exist_ok=True)

def load_and_clean(fp):
    df = pd.read_csv(fp, low_memory=False)
    # Parse dates
    if "transaction_date" in df.columns:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
        df["date"] = df["transaction_date"].dt.date
        df["year_month"] = df["transaction_date"].dt.to_period("M").astype(str)
        df["weekday"] = df["transaction_date"].dt.day_name()
    # Numeric cleaning
    num_cols = ["quantity", "unit_price", "total_amount",
                "discount_amount", "final_amount", "loyalty_points"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def save_summary(df):
    summ = {
        'total_sales': df['final_amount'].sum(),
        'total_transactions': df.shape[0],
        'total_quantity': df['quantity'].sum(),
        'avg_transaction_value': df['final_amount'].mean(),
        'median_transaction_value': df['final_amount'].median()
    }
    summary_df = pd.DataFrame.from_dict(summ, orient='index', columns=['value'])
    summary_df.to_csv(os.path.join(OUT_DIR, "summary_metrics.csv"))
    return summary_df

def plot_timeseries(df):
    monthly = df.groupby("year_month")["final_amount"].sum().reset_index()
    monthly['year_month'] = pd.to_datetime(monthly['year_month']).dt.to_period("M").dt.to_timestamp()
    plt.figure(figsize=(10,5))
    plt.plot(monthly['year_month'], monthly['final_amount'], marker='o')
    plt.title("Monthly Sales (Final Amount)")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "monthly_sales.png"))
    plt.close()
    monthly.to_csv(os.path.join(OUT_DIR, "monthly_sales.csv"), index=False)

def plot_sales_by_store(df):
    by_store = df.groupby("store_name")["final_amount"].sum().sort_values(ascending=False)
    top = by_store.head(12)
    plt.figure(figsize=(10,6))
    top.plot(kind='bar')
    plt.title("Top 12 Stores by Sales")
    plt.xlabel("Store")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "top_stores.png"))
    plt.close()
    by_store.to_csv(os.path.join(OUT_DIR, "sales_by_store.csv"))

def plot_category_breakdown(df):
    if "aisle" in df.columns:
        by_aisle = df.groupby("aisle")["final_amount"].sum().sort_values(ascending=False)
        top = by_aisle.head(12)
        plt.figure(figsize=(8,8))
        plt.pie(top.values, labels=top.index, autopct="%1.1f%%", startangle=140)
        plt.title("Sales Share by Aisle (Top 12)")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "aisle_pie_top12.png"))
        plt.close()
        by_aisle.to_csv(os.path.join(OUT_DIR, "sales_by_aisle.csv"))

def plot_top_products(df):
    by_product = df.groupby("product_name")["final_amount"].sum().sort_values(ascending=False)
    top = by_product.head(15)
    plt.figure(figsize=(10,6))
    plt.barh(top.index[::-1], top[::-1])
    plt.title("Top 15 Products by Sales")
    plt.xlabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "top_products.png"))
    plt.close()
    by_product.to_csv(os.path.join(OUT_DIR, "sales_by_product.csv"))

def plot_weekday_pattern(df):
    weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    by_weekday = df.groupby("weekday")["final_amount"].sum().reindex(weekdays)
    plt.figure(figsize=(8,5))
    plt.plot(by_weekday.index, by_weekday.values, marker='o')
    plt.title("Sales by Weekday")
    plt.xlabel("Weekday")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "sales_by_weekday.png"))
    plt.close()
    by_weekday.to_csv(os.path.join(OUT_DIR, "sales_by_weekday.csv"))

def plot_discount_vs_sales(df):
    sample = df.sample(n=min(800, len(df)), random_state=1)
    plt.figure(figsize=(7,5))
    plt.scatter(sample['discount_amount'], sample['final_amount'], alpha=0.6)
    plt.title("Discount Amount vs Final Amount (Sample)")
    plt.xlabel("Discount Amount")
    plt.ylabel("Final Amount")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "discount_vs_final_scatter.png"))
    plt.close()

def plot_store_month_heatmap(df):
    pivot = df.pivot_table(index="store_name", columns="year_month",
                           values="final_amount", aggfunc="sum", fill_value=0)
    store_totals = pivot.sum(axis=1).sort_values(ascending=False)
    top_stores = store_totals.head(12).index
    pivot_top = pivot.loc[top_stores]
    plt.figure(figsize=(12,6))
    plt.imshow(pivot_top.values, aspect='auto', interpolation='nearest')
    plt.colorbar(label='Sales')
    plt.yticks(range(len(pivot_top.index)), pivot_top.index)
    plt.xticks(range(len(pivot_top.columns)), pivot_top.columns, rotation=45, ha='right')
    plt.title("Heatmap: Top 12 Stores vs Month (Sales)")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "store_month_heatmap.png"))
    plt.close()
    pivot_top.to_csv(os.path.join(OUT_DIR, "store_month_pivot_top12.csv"))

def main():
    df = load_and_clean(INPUT_CSV)
    save_summary(df)
    plot_timeseries(df)
    plot_sales_by_store(df)
    plot_category_breakdown(df)
    plot_top_products(df)
    plot_weekday_pattern(df)
    plot_discount_vs_sales(df)
    plot_store_month_heatmap(df)
    print(f"Charts and CSV outputs written to: {OUT_DIR}")

if __name__ == "__main__":
    main()