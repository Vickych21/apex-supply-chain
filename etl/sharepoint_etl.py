import pandas as pd
from pathlib import Path


print("Starting SharePoint ETL process...")


# -----------------------------
# SOURCE FILE
# -----------------------------

input_path = (
    Path(__file__).parent.parent
    / "data"
    / "sharepoint"
    / "supplier_quality_report.xlsx"
)


# -----------------------------
# EXTRACT
# -----------------------------

df = pd.read_excel(input_path)

print(f"Extracted {len(df)} SharePoint records.")


# -----------------------------
# TRANSFORM
# -----------------------------

# Make sure the date column is a proper date
df["REPORT_DATE"] = pd.to_datetime(df["REPORT_DATE"])


# Calculate defect rate ourselves
df["DEFECT_RATE_CALCULATED"] = (
    df["DEFECTIVE_UNITS"] / df["UNITS_INSPECTED"] * 100
).round(2)


# Calculate quality performance
df["QUALITY_SCORE"] = (
    100 - df["DEFECT_RATE_CALCULATED"]
).round(2)


# Create a quality classification
df["QUALITY_PERFORMANCE"] = df["QUALITY_SCORE"].apply(
    lambda x:
        "Excellent" if x >= 98
        else "Good" if x >= 96
        else "Needs Review"
)


# Round numeric columns
df["DEFECT_RATE"] = df["DEFECT_RATE"].round(2)
df["DEFECT_RATE_CALCULATED"] = df["DEFECT_RATE_CALCULATED"].round(2)
df["QUALITY_SCORE"] = df["QUALITY_SCORE"].round(2)


print("SharePoint data transformation complete.")


# -----------------------------
# LOAD
# -----------------------------

output_path = (
    Path(__file__).parent.parent
    / "data"
    / "supplier_quality_analysis.csv"
)


df.to_csv(output_path, index=False)

print(f"Saved transformed data to: {output_path}")


print("SharePoint ETL process completed successfully!")