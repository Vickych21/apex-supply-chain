import pandas as pd
from pathlib import Path


# -----------------------------
# File path
# -----------------------------

output_path = (
    Path(__file__).parent.parent
    / "data"
    / "sharepoint"
    / "supplier_quality_report.xlsx"
)


# -----------------------------
# Generate SharePoint data
# -----------------------------

data = [
    [1, "Global Components Inc.", "2026-01-15", 1250, 34, 2.72, "Reviewed"],
    [2, "EuroTech Manufacturing", "2026-01-20", 980, 18, 1.84, "Approved"],
    [3, "Pacific Electronics Ltd.", "2026-01-25", 1420, 51, 3.59, "Action Required"],

    [1, "Global Components Inc.", "2026-02-15", 1380, 21, 1.52, "Approved"],
    [2, "EuroTech Manufacturing", "2026-02-20", 1150, 14, 1.22, "Approved"],
    [3, "Pacific Electronics Ltd.", "2026-02-25", 1290, 46, 3.57, "Action Required"],

    [1, "Global Components Inc.", "2026-03-15", 1520, 27, 1.78, "Approved"],
    [2, "EuroTech Manufacturing", "2026-03-20", 1075, 31, 2.88, "Reviewed"],
    [3, "Pacific Electronics Ltd.", "2026-03-25", 1480, 39, 2.64, "Reviewed"],

    [1, "Global Components Inc.", "2026-04-15", 1640, 19, 1.16, "Approved"],
    [2, "EuroTech Manufacturing", "2026-04-20", 1210, 11, 0.91, "Approved"],
    [3, "Pacific Electronics Ltd.", "2026-04-25", 1560, 43, 2.76, "Reviewed"],

    [1, "Global Components Inc.", "2026-05-15", 1710, 23, 1.35, "Approved"],
    [2, "EuroTech Manufacturing", "2026-05-20", 1340, 17, 1.27, "Approved"],
    [3, "Pacific Electronics Ltd.", "2026-05-25", 1620, 55, 3.40, "Action Required"],

    [1, "Global Components Inc.", "2026-06-15", 1590, 16, 1.01, "Approved"],
    [2, "EuroTech Manufacturing", "2026-06-20", 1280, 13, 1.02, "Approved"],
    [3, "Pacific Electronics Ltd.", "2026-06-25", 1750, 61, 3.49, "Action Required"],

    [1, "Global Components Inc.", "2026-07-15", 1820, 20, 1.10, "Approved"],
    [2, "EuroTech Manufacturing", "2026-07-20", 1410, 15, 1.06, "Approved"],
    [3, "Pacific Electronics Ltd.", "2026-07-25", 1690, 37, 2.19, "Reviewed"],

    [1, "Global Components Inc.", "2026-08-15", 1900, 18, 0.95, "Approved"],
    [2, "EuroTech Manufacturing", "2026-08-20", 1490, 12, 0.81, "Approved"],
    [3, "Pacific Electronics Ltd.", "2026-08-25", 1810, 49, 2.71, "Reviewed"],
]


columns = [
    "SUPPLIER_ID",
    "SUPPLIER_NAME",
    "REPORT_DATE",
    "UNITS_INSPECTED",
    "DEFECTIVE_UNITS",
    "DEFECT_RATE",
    "QUALITY_STATUS",
]


df = pd.DataFrame(data, columns=columns)


# -----------------------------
# Convert date
# -----------------------------

df["REPORT_DATE"] = pd.to_datetime(df["REPORT_DATE"])


# -----------------------------
# Save Excel document
# -----------------------------

df.to_excel(output_path, index=False)


print("SharePoint supplier quality report generated successfully!")
print(f"Generated {len(df)} quality records.")
print(f"Saved file to: {output_path}")