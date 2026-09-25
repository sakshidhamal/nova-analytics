import pandas as pd
import numpy as np


def detect_monthly_anomalies(df, z_threshold=2.0):
    """
    Detect unusual monthly sales and profit periods
    using z-score based statistical analysis.
    """

    data = df.copy()

    # Make sure date is datetime
    data["OrderDate"] = pd.to_datetime(
        data["OrderDate"],
        errors="coerce"
    )

    # Remove invalid dates
    data = data.dropna(
        subset=["OrderDate"]
    )

    # Create monthly period
    data["Month"] = (
        data["OrderDate"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    # Aggregate monthly business performance
    monthly = (
        data
        .groupby("Month")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("OrderDate", "count")
        )
        .reset_index()
    )

    # Rename Month to OrderDate so the rest of the dashboard
    # can use a consistent date field
    monthly = monthly.rename(
        columns={
            "Month": "OrderDate"
        }
    )

    # Need enough observations for meaningful z-scores
    if len(monthly) < 3:

        monthly["Sales_ZScore"] = 0.0
        monthly["Profit_ZScore"] = 0.0
        monthly["Anomaly"] = False
        monthly["AnomalyType"] = "Normal"

        return monthly

    # -----------------------------------------------------
    # SALES Z-SCORE
    # -----------------------------------------------------

    sales_std = monthly["Sales"].std()

    if pd.isna(sales_std) or sales_std == 0:

        monthly["Sales_ZScore"] = 0.0

    else:

        monthly["Sales_ZScore"] = (
            monthly["Sales"]
            - monthly["Sales"].mean()
        ) / sales_std

    # -----------------------------------------------------
    # PROFIT Z-SCORE
    # -----------------------------------------------------

    profit_std = monthly["Profit"].std()

    if pd.isna(profit_std) or profit_std == 0:

        monthly["Profit_ZScore"] = 0.0

    else:

        monthly["Profit_ZScore"] = (
            monthly["Profit"]
            - monthly["Profit"].mean()
        ) / profit_std

    # -----------------------------------------------------
    # ANOMALY FLAG
    # -----------------------------------------------------

    monthly["Anomaly"] = (
        monthly["Sales_ZScore"].abs() >= z_threshold
    ) | (
        monthly["Profit_ZScore"].abs() >= z_threshold
    )

    # -----------------------------------------------------
    # ANOMALY CLASSIFICATION
    # -----------------------------------------------------

    def classify_anomaly(row):

        sales_z = row["Sales_ZScore"]
        profit_z = row["Profit_ZScore"]

        if not row["Anomaly"]:
            return "Normal"

        if (
            sales_z >= z_threshold
            and profit_z >= z_threshold
        ):
            return "High Performance"

        if (
            sales_z <= -z_threshold
            and profit_z <= -z_threshold
        ):
            return "Critical Decline"

        if sales_z >= z_threshold:
            return "Sales Spike"

        if sales_z <= -z_threshold:
            return "Sales Drop"

        if profit_z >= z_threshold:
            return "Profit Spike"

        if profit_z <= -z_threshold:
            return "Profit Drop"

        return "Anomaly"

    monthly["AnomalyType"] = monthly.apply(
        classify_anomaly,
        axis=1
    )

    return monthly