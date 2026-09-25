"""
forecasting.py
--------------
Sales forecasting module for Nova Analytics.
"""

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


def prepare_monthly_sales(df):
    """
    Aggregate daily/order-level sales into monthly sales.
    """

    data = df.copy()

    data["OrderDate"] = pd.to_datetime(
        data["OrderDate"]
    )

    monthly = (
        data
        .set_index("OrderDate")
        .resample("MS")["Sales"]
        .sum()
        .reset_index()
    )

    monthly.columns = [
        "Month",
        "Sales"
    ]

    return monthly


def create_features(monthly):
    """
    Create time-based features for ML forecasting.
    """

    data = monthly.copy()

    data["TimeIndex"] = np.arange(
        len(data)
    )

    data["MonthNumber"] = (
        data["Month"].dt.month
    )

    data["Year"] = (
        data["Month"].dt.year
    )

    return data


def train_forecast_model(monthly):
    """
    Train a Linear Regression model
    using historical monthly sales.
    """

    data = create_features(
        monthly
    )

    features = [
        "TimeIndex",
        "MonthNumber",
    ]

    X = data[features]

    y = data["Sales"]

    model = LinearRegression()

    model.fit(
        X,
        y
    )

    return model, data


def generate_forecast(
    monthly,
    periods=6
):
    """
    Generate future monthly sales forecast.
    """

    model, data = train_forecast_model(
        monthly
    )

    last_month = data["Month"].max()

    future_dates = pd.date_range(
        start=last_month + pd.offsets.MonthBegin(1),
        periods=periods,
        freq="MS",
    )

    future = pd.DataFrame(
        {
            "Month": future_dates
        }
    )

    future["TimeIndex"] = np.arange(
        len(data),
        len(data) + periods
    )

    future["MonthNumber"] = (
        future["Month"].dt.month
    )

    future["Year"] = (
        future["Month"].dt.year
    )

    future["Forecast"] = model.predict(
        future[
            [
                "TimeIndex",
                "MonthNumber"
            ]
        ]
    )

    future["Forecast"] = future[
        "Forecast"
    ].clip(lower=0)

    return future


def evaluate_model(monthly):
    """
    Evaluate model using a chronological
    train/test split.
    """

    data = create_features(
        monthly
    )

    if len(data) < 6:
        return {
            "MAE": None,
            "RMSE": None,
            "MAPE": None,
        }

    split = int(
        len(data) * 0.8
    )

    train = data.iloc[:split]

    test = data.iloc[split:]

    features = [
        "TimeIndex",
        "MonthNumber",
    ]

    model = LinearRegression()

    model.fit(
        train[features],
        train["Sales"]
    )

    predictions = model.predict(
        test[features]
    )

    mae = mean_absolute_error(
        test["Sales"],
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            test["Sales"],
            predictions
        )
    )

    actual = test["Sales"].values

    safe_actual = np.where(
        actual == 0,
        1,
        actual
    )

    mape = np.mean(
        np.abs(
            (actual - predictions)
            / safe_actual
        )
    ) * 100

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
    }