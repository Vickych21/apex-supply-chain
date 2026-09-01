import os
import oracledb
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# -----------------------------
# Database connection
# -----------------------------

connection = oracledb.connect(
    user=os.getenv("ORACLE_USER"),
    password=os.getenv("ORACLE_PASSWORD"),
    dsn=os.getenv("ORACLE_DSN")
)

engine = create_engine(
    "oracle+oracledb://",
    creator=lambda: connection
)

print("Connected to Oracle successfully!")


# -----------------------------
# EXTRACT
# -----------------------------

query = """
SELECT
    SHIPMENT_ID,
    PO_ID,
    SUPPLIER_ID,
    SUPPLIER_NAME,
    TRACKING_NUMBER,
    CARRIER,
    SHIP_DATE,
    EXPECTED_ARRIVAL_DATE,
    ACTUAL_ARRIVAL_DATE,
    STATUS,
    ORIGIN_LOCATION,
    DESTINATION_LOCATION,
    TRANSIT_DAYS,
    DAYS_EARLY_LATE
FROM V_SHIPMENT_PERFORMANCE
"""

df = pd.read_sql(query, engine)

# Ensure column names are uppercase
df.columns = df.columns.str.upper()

print(f"Extracted {len(df)} shipment records.")


# -----------------------------
# TRANSFORM
# -----------------------------

df["SHIP_DATE"] = pd.to_datetime(df["SHIP_DATE"])

df["EXPECTED_ARRIVAL_DATE"] = pd.to_datetime(
    df["EXPECTED_ARRIVAL_DATE"]
)

df["ACTUAL_ARRIVAL_DATE"] = pd.to_datetime(
    df["ACTUAL_ARRIVAL_DATE"]
)


# Create a simple delivery classification
df["DELIVERY_PERFORMANCE"] = df["DAYS_EARLY_LATE"].apply(
    lambda x:
        "Early" if x < 0
        else "On Time" if x == 0
        else "Late" if x > 0
        else "Pending"
)

print("Shipment transformation complete.")


# -----------------------------
# LOAD
# -----------------------------

output_path = (
    Path(__file__).parent.parent
    / "data"
    / "shipment_performance.csv"
)

df.to_csv(output_path, index=False)

print(f"Saved transformed data to: {output_path}")


# -----------------------------
# Close connection
# -----------------------------

engine.dispose()

print("Oracle connection closed.")
print("Shipment ETL completed successfully!")