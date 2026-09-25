"""
generate_data.py
-----------------
Creates a synthetic retail sales dataset so the project runs out-of-the-box
with zero downloads or paid data sources. Run this once before app.py.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

REGIONS = ["North", "South", "East", "West", "Central"]
CATEGORIES = {
    "Electronics": ["Laptop", "Headphones", "Smartphone", "Monitor", "Keyboard"],
    "Furniture": ["Chair", "Desk", "Bookshelf", "Sofa", "Lamp"],
    "Office Supplies": ["Notebook", "Pen Set", "Stapler", "Printer Paper", "Folder"],
}
CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Home Office"]

N_ROWS = 3000
start_date = datetime(2023, 1, 1)
date_range_days = 730  # 2 years of data

rows = []
for i in range(N_ROWS):
    order_date = start_date + timedelta(days=int(np.random.randint(0, date_range_days)))
    category = np.random.choice(list(CATEGORIES.keys()))
    product = np.random.choice(CATEGORIES[category])
    region = np.random.choice(REGIONS)
    segment = np.random.choice(CUSTOMER_SEGMENTS)

    base_price = {
        "Electronics": np.random.uniform(50, 1200),
        "Furniture": np.random.uniform(40, 800),
        "Office Supplies": np.random.uniform(2, 60),
    }[category]

    quantity = np.random.randint(1, 10)
    discount = np.random.choice([0, 0.05, 0.1, 0.15, 0.2], p=[0.4, 0.2, 0.2, 0.1, 0.1])
    unit_price = round(base_price, 2)
    sales = round(unit_price * quantity * (1 - discount), 2)
    profit_margin = np.random.uniform(0.05, 0.35)
    profit = round(sales * profit_margin, 2)

    # inject a few missing / messy values on purpose so the cleaning step has real work to do
    if np.random.rand() < 0.02:
        discount = np.nan
    if np.random.rand() < 0.01:
        region = None

    rows.append({
        "OrderID": f"ORD-{10000+i}",
        "OrderDate": order_date.strftime("%Y-%m-%d"),
        "Region": region,
        "Category": category,
        "Product": product,
        "CustomerSegment": segment,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
    })

df = pd.DataFrame(rows)
df.to_csv("data/sample_sales_data.csv", index=False)
print(f"Generated data/sample_sales_data.csv with {len(df)} rows.")
