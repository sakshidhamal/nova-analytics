import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

from utils.data_utils import (
    load_and_clean_data,
    compute_kpis,
    sales_by_dimension,
    monthly_trend,
    top_products,
)

from utils.forecasting import (
    prepare_monthly_sales,
    generate_forecast,
    evaluate_model,
)


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Nova Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

DATA_PATH = "data/sample_sales_data.csv"


# =========================================================
# PROFESSIONAL NOVA THEME
# =========================================================

st.markdown(
    """
<style>
/* ---------- APP ---------- */

.stApp {
    background: #f4f7fb;
}

/* Keep normal Streamlit top header space.
   Do NOT force the content to the very top. */
div[data-testid="stAppViewContainer"] .main .block-container {
    max-width: 1500px;
    padding-top: 1.6rem !important;
    padding-bottom: 3rem !important;
}

/* Streamlit toolbar/header */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0b1220 0%,
        #111827 100%
    );
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

section[data-testid="stSidebar"] h2 {
    font-size: 27px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stCaption {
    color: #94a3b8 !important;
    font-size: 11px !important;
    letter-spacing: 1.5px;
    font-weight: 600;
}

section[data-testid="stSidebar"] hr {
    border-color: #263244 !important;
}

section[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

/* ---------- SIDEBAR NAVIGATION ---------- */

/* Hide radio circles */
section[data-testid="stSidebar"]
div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 11px 13px !important;
    margin: 4px 0 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label:hover {
    background: #1e293b !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label p {
    color: #cbd5e1 !important;
    font-size: 14px !important;
    font-weight: 550 !important;
}

/* Selected page */
section[data-testid="stSidebar"]
div[data-testid="stRadio"] label:has(input:checked) {
    background: #2563eb !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label:has(input:checked) p {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ---------- MAIN HEADINGS ---------- */

h1 {
    font-size: 36px !important;
    font-weight: 800 !important;
    letter-spacing: -1.2px;
    color: #0f172a !important;
}

h2 {
    font-size: 25px !important;
    font-weight: 750 !important;
    color: #172033 !important;
}

h3 {
    font-size: 19px !important;
    font-weight: 700 !important;
    color: #172033 !important;
}

/* ---------- METRIC CARDS ---------- */

div[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 15px !important;
    padding: 20px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 13px !important;
    font-weight: 650 !important;
}

div[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}

/* ---------- BUTTONS ---------- */

.stButton button {
    border-radius: 9px !important;
    font-weight: 650 !important;
    min-height: 42px;
}

/* ---------- TABLE ---------- */

div[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid #e2e8f0 !important;
}

/* ---------- ALERTS ---------- */

div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* ---------- DIVIDERS ---------- */

hr {
    border-color: #e2e8f0 !important;
}

/* ---------- NOVA HEADER ---------- */

.nova-main-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 30px;
    width: 100%;
    margin-bottom: 18px;
}

.nova-brand-title {
    font-size: 36px;
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #0f172a;
    margin: 0 0 7px 0;
}

.nova-brand-subtitle {
    font-size: 16px;
    color: #64748b;
    margin: 0;
}

.nova-active-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    padding: 15px 22px;
    min-width: 175px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}

.nova-active-label {
    font-size: 13px;
    color: #64748b;
    font-weight: 650;
    margin-bottom: 4px;
}

.nova-active-value {
    font-size: 28px;
    color: #0f172a;
    font-weight: 800;
    line-height: 1.1;
}

/* ---------- MOBILE ---------- */

@media (max-width: 900px) {
    .nova-main-header {
        flex-direction: column;
    }

    .nova-active-card {
        width: 100%;
        box-sizing: border-box;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def get_data():
    data = load_and_clean_data(DATA_PATH)

    if "OrderDate" in data.columns:
        data["OrderDate"] = pd.to_datetime(
            data["OrderDate"],
            errors="coerce",
        )

    return data


df = get_data()


# =========================================================
# BASIC VALIDATION
# =========================================================

required_columns = [
    "OrderDate",
    "Sales",
    "Profit",
    "Region",
    "Category",
    "Product",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"Missing required columns: {', '.join(missing_columns)}"
    )
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def money(value):
    try:
        value = float(value)
    except Exception:
        return "$0"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"

    return f"${value:,.0f}"


def monthly_growth(data):
    if data.empty:
        return 0

    temp = data.copy()

    temp["OrderDate"] = pd.to_datetime(
        temp["OrderDate"],
        errors="coerce",
    )

    temp = temp.dropna(subset=["OrderDate"])

    if temp.empty:
        return 0

    monthly = (
        temp.assign(
            Month=temp["OrderDate"].dt.to_period("M")
        )
        .groupby("Month")["Sales"]
        .sum()
        .sort_index()
    )

    if len(monthly) < 2:
        return 0

    previous = monthly.iloc[-2]
    current = monthly.iloc[-1]

    if previous == 0:
        return 0

    return ((current - previous) / previous) * 100


# =========================================================
# SAFE ANOMALY DETECTION
# =========================================================

def detect_anomalies(data):
    temp = data.copy()

    temp["OrderDate"] = pd.to_datetime(
        temp["OrderDate"],
        errors="coerce",
    )

    temp = temp.dropna(subset=["OrderDate"])

    if temp.empty:
        return pd.DataFrame(
            columns=[
                "OrderDate",
                "Sales",
                "Profit",
                "Orders",
                "Sales_Z",
                "Profit_Z",
                "Anomaly",
                "AnomalyType",
            ]
        )

    agg = {
        "Sales": ("Sales", "sum"),
        "Profit": ("Profit", "sum"),
    }

    if "OrderID" in temp.columns:
        agg["Orders"] = ("OrderID", "nunique")
    else:
        agg["Orders"] = ("Sales", "count")

    monthly = (
        temp.set_index("OrderDate")
        .resample("ME")
        .agg(**agg)
        .reset_index()
    )

    if monthly.empty:
        return monthly

    sales_std = monthly["Sales"].std()
    profit_std = monthly["Profit"].std()

    if pd.isna(sales_std) or sales_std == 0:
        monthly["Sales_Z"] = 0.0
    else:
        monthly["Sales_Z"] = (
            monthly["Sales"] - monthly["Sales"].mean()
        ) / sales_std

    if pd.isna(profit_std) or profit_std == 0:
        monthly["Profit_Z"] = 0.0
    else:
        monthly["Profit_Z"] = (
            monthly["Profit"] - monthly["Profit"].mean()
        ) / profit_std

    monthly["Anomaly"] = (
        monthly["Sales_Z"].abs().ge(2)
        | monthly["Profit_Z"].abs().ge(2)
    )

    def classify(row):
        sales_z = row["Sales_Z"]
        profit_z = row["Profit_Z"]

        if sales_z >= 2 and profit_z >= 2:
            return "High Performance"

        if sales_z <= -2 and profit_z <= -2:
            return "Critical Decline"

        if sales_z >= 2:
            return "Sales Spike"

        if sales_z <= -2:
            return "Sales Drop"

        if profit_z >= 2:
            return "Profit Spike"

        if profit_z <= -2:
            return "Profit Drop"

        return "Normal"

    monthly["AnomalyType"] = monthly.apply(
        classify,
        axis=1,
    )

    return monthly


# =========================================================
# AI CONTEXT
# =========================================================

def build_ai_context(data):
    kpis = compute_kpis(data)

    region = sales_by_dimension(
        data,
        "Region",
    ).to_string(index=False)

    category = sales_by_dimension(
        data,
        "Category",
    ).to_string(index=False)

    products = top_products(
        data,
        10,
    ).to_string(index=False)

    trend = monthly_trend(
        data,
    ).to_string(index=False)

    return f"""
BUSINESS KPIs

{kpis}

REGIONAL PERFORMANCE

{region}

CATEGORY PERFORMANCE

{category}

TOP PRODUCTS

{products}

MONTHLY PERFORMANCE

{trend}
""".strip()


# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(question, context):
    from groq import Groq

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from your .env file.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
You are NOVA, a senior business intelligence analyst.

Analyze ONLY the business data supplied by the user.

Rules:
- Never invent numbers.
- Use actual numbers from the supplied data.
- Explain important trends.
- Keep answers professional.
- Use concise headings and bullet points.
- Mention limitations when the data does not support a conclusion.
""",
            },
            {
                "role": "user",
                "content": f"""
BUSINESS DATA

{context}

USER QUESTION

{question}
""",
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## ◈ NOVA")
    st.caption("ANALYTICS PLATFORM")

    st.divider()

    st.markdown("### Workspace")

    page = st.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "Performance Analytics",
            "Sales Forecasting",
            "Anomaly Detection",
            "AI Business Analyst",
            "Data Explorer",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Filters")

    regions = st.multiselect(
        "Region",
        sorted(df["Region"].dropna().unique()),
        default=list(df["Region"].dropna().unique()),
    )

    categories = st.multiselect(
        "Category",
        sorted(df["Category"].dropna().unique()),
        default=list(df["Category"].dropna().unique()),
    )

    date_min = df["OrderDate"].min().date()
    date_max = df["OrderDate"].max().date()

    date_range = st.date_input(
        "Date Range",
        value=(date_min, date_max),
    )

    st.divider()

    st.caption(f"Records: {len(df):,}")
    st.caption(f"Coverage: {date_min} → {date_max}")


# =========================================================
# FILTER DATA
# =========================================================

filtered = df[
    df["Region"].isin(regions)
    & df["Category"].isin(categories)
].copy()

if len(date_range) == 2:
    filtered = filtered[
        (filtered["OrderDate"] >= pd.Timestamp(date_range[0]))
        & (filtered["OrderDate"] <= pd.Timestamp(date_range[1]))
    ]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()


# =========================================================
# TOP HEADER
# =========================================================

st.html(
    f"""
<div class="nova-main-header">
    <div>
        <div class="nova-brand-title">NOVA ANALYTICS</div>
        <div class="nova-brand-subtitle">
            AI-Powered Business Intelligence &amp; Data Analytics Platform
        </div>
    </div>

    <div class="nova-active-card">
        <div class="nova-active-label">Active Records</div>
        <div class="nova-active-value">{len(filtered):,}</div>
    </div>
</div>
"""
)

st.divider()


# =========================================================
# EXECUTIVE DASHBOARD
# =========================================================

if page == "Executive Dashboard":

    st.subheader("Executive Overview")

    st.caption(
        "Monitor revenue, profitability, orders and product performance."
    )

    kpis = compute_kpis(filtered)
    growth = monthly_growth(filtered)

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Revenue",
            money(kpis["total_sales"]),
            f"{growth:+.1f}% latest period",
        )

    with c2:
        st.metric(
            "Profit",
            money(kpis["total_profit"]),
        )

    with c3:
        st.metric(
            "Average Order",
            f"${kpis['avg_order_value']:,.2f}",
        )

    with c4:
        st.metric(
            "Orders",
            f"{kpis['total_orders']:,}",
        )

    with c5:
        st.metric(
            "Profit Margin",
            f"{kpis['avg_profit_margin']}%",
        )

    st.markdown("###")

    left, right = st.columns([1.7, 1])

    with left:
        st.subheader("Revenue & Profit Trend")

        trend = monthly_trend(filtered)

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=trend["Month"],
                y=trend["Sales"],
                mode="lines+markers",
                name="Revenue",
                line=dict(width=3),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=trend["Month"],
                y=trend["Profit"],
                mode="lines+markers",
                name="Profit",
                line=dict(width=3),
            )
        )

        fig.update_layout(
            height=420,
            template="plotly_white",
            margin=dict(l=10, r=10, t=30, b=10),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                y=1.08,
                x=0,
            ),
            xaxis_title=None,
            yaxis_title="Amount",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    with right:
        st.subheader("Regional Revenue")

        region = sales_by_dimension(
            filtered,
            "Region",
        )

        fig = px.bar(
            region,
            x="Sales",
            y="Region",
            orientation="h",
            text="Sales",
        )

        fig.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            height=420,
            template="plotly_white",
            margin=dict(l=5, r=40, t=30, b=10),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    left, right = st.columns([1, 1.5])

    with left:
        st.subheader("Category Mix")

        category = sales_by_dimension(
            filtered,
            "Category",
        )

        fig = px.pie(
            category,
            names="Category",
            values="Sales",
            hole=0.58,
        )

        fig.update_layout(
            height=420,
            template="plotly_white",
            margin=dict(l=5, r=5, t=30, b=10),
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    with right:
        st.subheader("Top 10 Products")

        products = top_products(filtered, 10)

        products = products.sort_values(
            "Sales",
            ascending=True,
        )

        fig = px.bar(
            products,
            x="Sales",
            y="Product",
            orientation="h",
            text="Sales",
        )

        fig.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            height=420,
            template="plotly_white",
            margin=dict(l=5, r=55, t=30, b=10),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    st.divider()

    st.subheader("Business Intelligence")

    region = sales_by_dimension(filtered, "Region")
    category = sales_by_dimension(filtered, "Category")
    products = top_products(filtered, 1)

    a, b, c = st.columns(3)

    with a:
        if not region.empty:
            st.info(
                f"""
**Regional Leader**

{region.iloc[0]["Region"]}

Revenue: **{money(region.iloc[0]["Sales"])}**
"""
            )

    with b:
        if not category.empty:
            st.info(
                f"""
**Category Leader**

{category.iloc[0]["Category"]}

Revenue: **{money(category.iloc[0]["Sales"])}**
"""
            )

    with c:
        if not products.empty:
            st.info(
                f"""
**Top Product**

{products.iloc[0]["Product"]}

Revenue: **{money(products.iloc[0]["Sales"])}**
"""
            )


# =========================================================
# PERFORMANCE ANALYTICS
# =========================================================

elif page == "Performance Analytics":

    st.subheader("Performance Analytics")

    st.caption(
        "Detailed analysis of revenue, profitability and operational performance."
    )

    tabs = st.tabs(
        [
            "Regional Analysis",
            "Category Analysis",
            "Profitability",
            "Monthly Trends",
        ]
    )

    with tabs[0]:
        region = sales_by_dimension(filtered, "Region")

        st.dataframe(
            region,
            width="stretch",
            hide_index=True,
        )

        fig = px.bar(
            region,
            x="Region",
            y="Sales",
            text="Sales",
        )

        fig.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            template="plotly_white",
            height=450,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    with tabs[1]:
        category = sales_by_dimension(filtered, "Category")

        st.dataframe(
            category,
            width="stretch",
            hide_index=True,
        )

        fig = px.bar(
            category,
            x="Category",
            y="Sales",
            text="Sales",
        )

        fig.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            template="plotly_white",
            height=450,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    with tabs[2]:
        profitability = (
            filtered
            .groupby("Region")
            .agg(
                Revenue=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
            .reset_index()
        )

        profitability["Profit Margin %"] = (
            profitability["Profit"]
            .div(
                profitability["Revenue"].replace(0, pd.NA)
            )
            .fillna(0)
            * 100
        ).round(2)

        st.dataframe(
            profitability,
            width="stretch",
            hide_index=True,
        )

        fig = px.scatter(
            profitability,
            x="Revenue",
            y="Profit",
            size="Revenue",
            color="Region",
            text="Region",
        )

        fig.update_layout(
            template="plotly_white",
            height=500,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

    with tabs[3]:
        trend = monthly_trend(filtered)

        st.dataframe(
            trend,
            width="stretch",
            hide_index=True,
        )

        fig = px.area(
            trend,
            x="Month",
            y="Sales",
        )

        fig.update_layout(
            template="plotly_white",
            height=450,
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )


# =========================================================
# SALES FORECASTING
# =========================================================

elif page == "Sales Forecasting":

    st.subheader("Sales Forecasting")

    st.caption(
        "Machine-learning based forecasting of future monthly revenue."
    )

    try:
        monthly = prepare_monthly_sales(filtered)

        if len(monthly) < 6:
            st.warning(
                "At least 6 months of historical data are required "
                "to generate a meaningful forecast."
            )

        else:
            control1, control2 = st.columns([1, 3])

            with control1:
                forecast_periods = st.selectbox(
                    "Forecast Horizon",
                    [3, 6, 9, 12],
                    index=1,
                )

            with control2:
                st.info(
                    f"""
**Forecasting Model**

Linear Regression using time-based features.

Historical observations: **{len(monthly)} months**

Forecast horizon: **{forecast_periods} months**
"""
                )

            forecast = generate_forecast(
                monthly,
                periods=forecast_periods,
            )

            metrics = evaluate_model(monthly)

            st.markdown("### Model Performance")

            m1, m2, m3 = st.columns(3)

            with m1:
                value = metrics.get("MAE")
                st.metric(
                    "MAE",
                    money(value) if value is not None else "N/A",
                )

            with m2:
                value = metrics.get("RMSE")
                st.metric(
                    "RMSE",
                    money(value) if value is not None else "N/A",
                )

            with m3:
                value = metrics.get("MAPE")
                st.metric(
                    "MAPE",
                    f"{value:.1f}%" if value is not None else "N/A",
                )

            st.markdown("### Revenue Forecast")

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=monthly["Month"],
                    y=monthly["Sales"],
                    mode="lines+markers",
                    name="Historical Revenue",
                    line=dict(width=3),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=forecast["Month"],
                    y=forecast["Forecast"],
                    mode="lines+markers",
                    name="Forecast",
                    line=dict(width=3, dash="dash"),
                )
            )

            fig.update_layout(
                template="plotly_white",
                height=500,
                hovermode="x unified",
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis_title=None,
                yaxis_title="Revenue",
            )

            st.plotly_chart(
                fig,
                width="stretch",
            )

            st.markdown("### Forecasted Revenue")

            forecast_display = forecast[
                ["Month", "Forecast"]
            ].copy()

            forecast_display["Month"] = (
                forecast_display["Month"]
                .dt.strftime("%B %Y")
            )

            forecast_display["Forecast"] = (
                forecast_display["Forecast"]
                .round(2)
            )

            forecast_display.columns = [
                "Forecast Month",
                "Predicted Revenue",
            ]

            st.dataframe(
                forecast_display,
                width="stretch",
                hide_index=True,
            )

            total_forecast = forecast["Forecast"].sum()
            average_forecast = forecast["Forecast"].mean()

            highest_forecast = forecast.loc[
                forecast["Forecast"].idxmax()
            ]

            st.markdown("### Forecast Summary")

            s1, s2, s3 = st.columns(3)

            with s1:
                st.metric(
                    "Forecasted Revenue",
                    money(total_forecast),
                )

            with s2:
                st.metric(
                    "Average Monthly Forecast",
                    money(average_forecast),
                )

            with s3:
                st.metric(
                    "Highest Forecast Month",
                    highest_forecast["Month"].strftime("%b %Y"),
                )

            with st.expander(
                "How the forecasting model works"
            ):
                st.markdown(
                    """
### Forecasting Pipeline

**1. Data Preparation**

Order-level sales are aggregated into monthly revenue.

**2. Feature Engineering**

The model uses time-based features.

**3. Machine Learning**

A Linear Regression model learns patterns from historical revenue.

**4. Future Prediction**

The trained model generates future monthly revenue estimates.

**5. Model Evaluation**

MAE, RMSE and MAPE are used to evaluate the model.
"""
                )

    except Exception as error:
        st.error(f"Forecasting error: {error}")


# =========================================================
# ANOMALY DETECTION
# =========================================================

elif page == "Anomaly Detection":

    st.subheader("Anomaly Detection")

    st.caption(
        "Statistical detection of unusual sales and profitability patterns."
    )

    anomaly_data = detect_anomalies(filtered)

    if anomaly_data.empty:
        st.warning(
            "Not enough data available for anomaly detection."
        )

    else:
        anomalies = anomaly_data[
            anomaly_data["Anomaly"]
        ].copy()

        total_months = len(anomaly_data)
        anomaly_count = len(anomalies)
        normal_count = total_months - anomaly_count

        anomaly_rate = (
            anomaly_count / total_months * 100
            if total_months > 0
            else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Months Analysed",
                f"{total_months:,}",
            )

        with c2:
            st.metric(
                "Anomalies Detected",
                f"{anomaly_count:,}",
            )

        with c3:
            st.metric(
                "Normal Periods",
                f"{normal_count:,}",
            )

        with c4:
            st.metric(
                "Anomaly Rate",
                f"{anomaly_rate:.1f}%",
            )

        st.markdown("### Monthly Revenue Anomalies")

        fig = go.Figure()

        normal = anomaly_data[
            ~anomaly_data["Anomaly"]
        ]

        abnormal = anomaly_data[
            anomaly_data["Anomaly"]
        ]

        fig.add_trace(
            go.Scatter(
                x=normal["OrderDate"],
                y=normal["Sales"],
                mode="lines+markers",
                name="Normal",
                line=dict(width=2),
            )
        )

        if not abnormal.empty:
            fig.add_trace(
                go.Scatter(
                    x=abnormal["OrderDate"],
                    y=abnormal["Sales"],
                    mode="markers",
                    name="Anomaly",
                    marker=dict(
                        size=13,
                        symbol="diamond",
                    ),
                    text=abnormal["AnomalyType"],
                    hovertemplate=(
                        "<b>%{x|%B %Y}</b><br>"
                        "Revenue: $%{y:,.0f}<br>"
                        "Type: %{text}"
                        "<extra></extra>"
                    ),
                )
            )

        fig.update_layout(
            template="plotly_white",
            height=450,
            hovermode="x unified",
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_title=None,
            yaxis_title="Revenue",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

        st.markdown("### Detected Events")

        if anomaly_count == 0:
            st.success(
                "No significant anomalies were detected "
                "in the selected period."
            )

        else:
            display = anomalies[
                [
                    "OrderDate",
                    "Sales",
                    "Profit",
                    "Orders",
                    "AnomalyType",
                ]
            ].copy()

            display["OrderDate"] = (
                display["OrderDate"]
                .dt.strftime("%B %Y")
            )

            display["Sales"] = display["Sales"].round(2)
            display["Profit"] = display["Profit"].round(2)

            display.columns = [
                "Period",
                "Revenue",
                "Profit",
                "Orders",
                "Detection",
            ]

            st.dataframe(
                display,
                width="stretch",
                hide_index=True,
            )

        with st.expander(
            "How anomaly detection works"
        ):
            st.markdown(
                """
### Statistical Anomaly Detection

Nova analyses monthly business performance.

Z-scores are calculated for:

- Revenue
- Profit

A z-score measures how far a monthly observation
is from the historical mean.

The default anomaly threshold is:

**±2 standard deviations**

Possible classifications include:

- Sales Spike
- Sales Drop
- Profit Spike
- Profit Drop
- High Performance
- Critical Decline
"""
            )


# =========================================================
# AI BUSINESS ANALYST
# =========================================================

elif page == "AI Business Analyst":

    st.subheader("✦ AI Business Analyst")

    st.caption(
        "Ask natural-language questions about your business data."
    )

    st.info(
        """
**NOVA AI**

Your natural-language analytics assistant.

Ask questions about revenue, profit, regions, categories,
products and monthly performance.
"""
    )

    st.markdown("#### Suggested Questions")

    q1, q2, q3 = st.columns(3)

    with q1:
        st.write(
            "Which region generated the highest revenue?"
        )

    with q2:
        st.write(
            "Which category is performing best?"
        )

    with q3:
        st.write(
            "Summarize the sales trend."
        )

    question = st.text_area(
        "Ask NOVA",
        placeholder=(
            "Example: Which region has the highest profit "
            "and what percentage of total revenue does it contribute?"
        ),
        height=130,
    )

    if st.button(
        "Generate AI Analysis",
        type="primary",
        width="stretch",
    ):
        if not question.strip():
            st.warning("Enter a question first.")

        else:
            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                st.error(
                    "GROQ_API_KEY is missing from your .env file."
                )

            else:
                context = build_ai_context(filtered)

                with st.spinner(
                    "NOVA is analyzing your data..."
                ):
                    try:
                        answer = ask_ai(
                            question,
                            context,
                        )

                        st.success(
                            "Analysis generated successfully."
                        )

                        st.markdown("### AI Response")
                        st.markdown(answer)

                    except Exception as error:
                        st.error(
                            f"AI request failed: {error}"
                        )

    st.divider()

    st.subheader("AI Architecture")

    st.write(
        """
**Data Layer → Pandas**

The dataset is cleaned, filtered and aggregated.

**Analytics Layer → Python**

KPIs, trends, regional performance and product metrics are calculated.

**GenAI Layer → Groq LLM**

The analytical context is passed to the language model.

**Presentation Layer → Streamlit + Plotly**

Results are presented through an interactive analytics dashboard.
"""
    )


# =========================================================
# DATA EXPLORER
# =========================================================

elif page == "Data Explorer":

    st.subheader("Data Explorer")

    st.caption(
        "Inspect, analyze and export the filtered dataset."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Records",
            f"{len(filtered):,}",
        )

    with c2:
        st.metric(
            "Columns",
            f"{len(filtered.columns):,}",
        )

    with c3:
        st.metric(
            "Missing Values",
            f"{int(filtered.isna().sum().sum()):,}",
        )

    with c4:
        st.metric(
            "Products",
            f"{filtered['Product'].nunique():,}",
        )

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        filtered,
        width="stretch",
        height=500,
        hide_index=True,
    )

    csv_data = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Filtered Dataset",
        data=csv_data,
        file_name="nova_filtered_sales_data.csv",
        mime="text/csv",
        width="stretch",
    )

    st.divider()

    st.subheader("Data Quality")

    quality = pd.DataFrame(
        {
            "Column": filtered.columns,
            "Data Type": [
                str(dtype)
                for dtype in filtered.dtypes
            ],
            "Missing Values": [
                int(filtered[column].isna().sum())
                for column in filtered.columns
            ],
            "Unique Values": [
                int(filtered[column].nunique())
                for column in filtered.columns
            ],
        }
    )

    st.dataframe(
        quality,
        width="stretch",
        hide_index=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "NOVA ANALYTICS  •  Python  •  Pandas  •  Plotly  •  Streamlit  •  Generative AI"
)
