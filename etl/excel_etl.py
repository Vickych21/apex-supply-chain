import pandas as pd
from pathlib import Path


# -----------------------------
# File paths
# -----------------------------

input_path = (
    Path(__file__).parent.parent
    / "data"
    / "excel"
    / "supplier_monthly_report.xlsx"
)

output_path = (
    Path(__file__).parent.parent
    / "data"
    / "supplier_excel_analysis.csv"
)


print("Starting Excel ETL process...")


# -----------------------------
# EXTRACT
# -----------------------------

df = pd.read_excel(input_path)

print(f"Extracted {len(df)} Excel records.")


# -----------------------------
# TRANSFORM
# -----------------------------

# Make sure column names are consistent
df.columns = df.columns.str.upper().str.strip()

# Convert report month to datetime
df["REPORT_MONTH"] = pd.to_datetime(df["REPORT_MONTH"])

# Round financial and percentage values
df["TOTAL_SPEND"] = df["TOTAL_SPEND"].round(2)

df["ON_TIME_DELIVERY_RATE"] = (
    df["ON_TIME_DELIVERY_RATE"].round(2)
)

df["DEFECT_RATE"] = (
    df["DEFECT_RATE"].round(2)
)

# Calculate average spend per purchase order
df["AVERAGE_SPEND_PER_PO"] = (
    df["TOTAL_SPEND"] / df["PURCHASE_ORDERS"]
).round(2)

# Calculate delayed order percentage
df["DELAY_RATE"] = (
    df["DELAYED_ORDERS"]
    / df["PURCHASE_ORDERS"]
    * 100
).round(2)

# Create supplier performance classification
df["PERFORMANCE_STATUS"] = df.apply(
    lambda row:
        "Excellent"
        if row["ON_TIME_DELIVERY_RATE"] >= 97
        and row["DEFECT_RATE"] <= 1.5

        else "Good"
        if row["ON_TIME_DELIVERY_RATE"] >= 94
        and row["DEFECT_RATE"] <= 2.5

        else "Needs Review",
    axis=1
)

print("Excel data transformation complete.")


# -----------------------------
# LOAD
# -----------------------------

df.to_csv(
    output_path,
    index=False
)

print(f"Saved transformed data to: {output_path}")

print("Excel ETL process completed successfully!")