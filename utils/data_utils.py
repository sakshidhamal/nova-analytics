"""
data_utils.py
-------------
Reusable data-cleaning and KPI functions, kept separate from the Streamlit
app so they're easy to unit test and reuse in a notebook.
"""

import pandas as pd


def load_and_clean_data(path: str) -> pd.DataFrame:
    """Load the raw CSV and apply standard cleaning steps."""
    df = pd.read_csv(path)

    # Parse dates
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

    # Fill missing discount with 0 (no discount applied)
    df["Discount"] = df["Discount"].fillna(0)

    # Drop rows with missing region (small fraction, safe to drop)
    df = df.dropna(subset=["Region"])

    # Derived columns useful for analysis
    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
    df["Year"] = df["OrderDate"].dt.year
    df["ProfitMargin"] = (df["Profit"] / df["Sales"]).round(3)

    return df.reset_index(drop=True)


def compute_kpis(df: pd.DataFrame) -> dict:
    """Return headline KPIs for the dashboard's top row."""
    return {
        "total_sales": round(df["Sales"].sum(), 2),
        "total_profit": round(df["Profit"].sum(), 2),
        "avg_order_value": round(df["Sales"].mean(), 2),
        "total_orders": df["OrderID"].nunique(),
        "avg_profit_margin": round(df["ProfitMargin"].mean() * 100, 2),
    }


def sales_by_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Aggregate sales and profit by a chosen categorical column."""
    return (
        df.groupby(dimension)[["Sales", "Profit"]]
        .sum()
        .sort_values("Sales", ascending=False)
        .reset_index()
    )


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Sales and profit trend over time, aggregated by month."""
    return (
        df.groupby("Month")[["Sales", "Profit"]]
        .sum()
        .reset_index()
        .sort_values("Month")
    )


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top N products by total sales."""
    return (
        df.groupby("Product")[["Sales", "Profit", "Quantity"]]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(n)
        .reset_index()
    )
