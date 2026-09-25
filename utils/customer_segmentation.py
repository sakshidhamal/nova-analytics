import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def build_customer_rfm(df):
    """
    Build RFM metrics for customer segmentation.

    RFM:
    Recency    -> How recently a customer purchased
    Frequency  -> How often a customer purchased
    Monetary   -> How much a customer spent
    """

    data = df.copy()

    data["OrderDate"] = pd.to_datetime(
        data["OrderDate"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["OrderDate"]
    )

    # Determine customer column
    if "CustomerID" in data.columns:
        customer_col = "CustomerID"
    elif "Customer Id" in data.columns:
        customer_col = "Customer Id"
    elif "Customer" in data.columns:
        customer_col = "Customer"
    else:
        # Dataset does not contain a customer identifier.
        # Create a deterministic customer grouping from available fields.
        customer_col = "_CustomerGroup"

        data[customer_col] = (
            data["Region"].astype(str)
            + "_"
            + data["Category"].astype(str)
            + "_"
            + (
                data.index
                .astype(int)
                % 300
            ).astype(str)
        )

    analysis_date = (
        data["OrderDate"].max()
        + pd.Timedelta(days=1)
    )

    rfm = (
        data.groupby(customer_col)
        .agg(
            Recency=(
                "OrderDate",
                lambda x: (
                    analysis_date - x.max()
                ).days
            ),
            Frequency=(
                "OrderDate",
                "count"
            ),
            Monetary=(
                "Sales",
                "sum"
            )
        )
        .reset_index()
    )

    rfm = rfm.rename(
        columns={
            customer_col: "Customer"
        }
    )

    return rfm


def create_customer_segments(
    df,
    n_clusters=4
):
    """
    Create customer segments using K-Means clustering.
    """

    rfm = build_customer_rfm(df)

    if len(rfm) < n_clusters:

        n_clusters = max(
            2,
            min(len(rfm), n_clusters)
        )

    features = [
        "Recency",
        "Frequency",
        "Monetary"
    ]

    X = rfm[features].copy()

    # Log transformation reduces the effect of extreme values
    X["Recency"] = np.log1p(
        X["Recency"]
    )

    X["Frequency"] = np.log1p(
        X["Frequency"]
    )

    X["Monetary"] = np.log1p(
        X["Monetary"].clip(lower=0)
    )

    # Standardize features
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        X
    )

    # K-Means clustering
    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    rfm["Cluster"] = model.fit_predict(
        X_scaled
    )

    # -----------------------------------------------------
    # Create business-friendly segment names
    # -----------------------------------------------------

    summary = (
        rfm.groupby("Cluster")
        .agg(
            Recency=("Recency", "mean"),
            Frequency=("Frequency", "mean"),
            Monetary=("Monetary", "mean"),
            Customers=("Customer", "count")
        )
        .reset_index()
    )

    # Rank clusters
    summary["Score"] = (
        summary["Frequency"].rank(
            pct=True
        )
        + summary["Monetary"].rank(
            pct=True
        )
        + (
            1
            - summary["Recency"].rank(
                pct=True
            )
        )
    )

    summary = summary.sort_values(
        "Score",
        ascending=False
    )

    names = [
        "Champions",
        "Loyal Customers",
        "Potential Customers",
        "At Risk"
    ]

    segment_map = {}

    for i, cluster in enumerate(
        summary["Cluster"]
    ):

        if i < len(names):
            segment_map[cluster] = names[i]
        else:
            segment_map[cluster] = (
                f"Customer Segment {i + 1}"
            )

    rfm["Segment"] = (
        rfm["Cluster"]
        .map(segment_map)
    )

    return rfm