import random
from pathlib import Path
from datetime import date
import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

OUTPUT_FOLDER = (
    Path(__file__).parent.parent
    / "data"
    / "excel"
)

OUTPUT_FILE = OUTPUT_FOLDER / "supplier_monthly_report.xlsx"

random.seed(42)


# --------------------------------------------------
# Supplier information
# --------------------------------------------------

suppliers = [
    {
        "SUPPLIER_ID": 1,
        "SUPPLIER_NAME": "Global Components Inc.",
        "COUNTRY": "USA",
        "SUPPLIER_CATEGORY": "Semiconductors",
        "BASE_LEAD_TIME": 14,
        "RELIABILITY": 0.965,
    },
    {
        "SUPPLIER_ID": 2,
        "SUPPLIER_NAME": "EuroTech Manufacturing",
        "COUNTRY": "Germany",
        "SUPPLIER_CATEGORY": "Power Components",
        "BASE_LEAD_TIME": 18,
        "RELIABILITY": 0.978,
    },
    {
        "SUPPLIER_ID": 3,
        "SUPPLIER_NAME": "Pacific Electronics Ltd.",
        "COUNTRY": "Taiwan",
        "SUPPLIER_CATEGORY": "Displays",
        "BASE_LEAD_TIME": 21,
        "RELIABILITY": 0.932,
    },
]


# --------------------------------------------------
# Generate monthly supplier data
# --------------------------------------------------

records = []

months = pd.date_range(
    start="2026-01-01",
    end="2026-08-01",
    freq="MS"
)


for month in months:

    for supplier in suppliers:

        purchase_orders = random.randint(8, 25)

        units_ordered = random.randint(500, 2500)

        average_unit_cost = random.uniform(20, 80)

        total_spend = units_ordered * average_unit_cost

        # Small random variation around supplier's normal lead time
        average_lead_time = supplier["BASE_LEAD_TIME"] + random.randint(-2, 3)

        # Reliability varies slightly month-to-month
        on_time_rate = (
            supplier["RELIABILITY"]
            + random.uniform(-0.025, 0.015)
        )

        on_time_rate = max(
            0.80,
            min(0.995, on_time_rate)
        )

        defect_rate = random.uniform(0.005, 0.035)

        delayed_orders = round(
            purchase_orders * (1 - on_time_rate)
        )

        records.append(
            {
                "REPORT_MONTH": month.date(),
                "SUPPLIER_ID": supplier["SUPPLIER_ID"],
                "SUPPLIER_NAME": supplier["SUPPLIER_NAME"],
                "COUNTRY": supplier["COUNTRY"],
                "SUPPLIER_CATEGORY": supplier["SUPPLIER_CATEGORY"],
                "PURCHASE_ORDERS": purchase_orders,
                "UNITS_ORDERED": units_ordered,
                "TOTAL_SPEND": round(total_spend, 2),
                "AVERAGE_LEAD_TIME_DAYS": average_lead_time,
                "ON_TIME_DELIVERY_RATE": round(
                    on_time_rate * 100,
                    2
                ),
                "DELAYED_ORDERS": delayed_orders,
                "DEFECT_RATE": round(
                    defect_rate * 100,
                    2
                ),
            }
        )


# --------------------------------------------------
# Create DataFrame
# --------------------------------------------------

df = pd.DataFrame(records)


# --------------------------------------------------
# Save Excel file
# --------------------------------------------------

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

df.to_excel(
    OUTPUT_FILE,
    index=False
)


print("Excel supplier data generated successfully!")
print(f"Generated {len(df)} supplier records.")
print(f"Saved Excel file to: {OUTPUT_FILE}")