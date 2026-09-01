import os
import oracledb
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

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
    SUPPLIER_ID,
    SUPPLIER_NAME,
    COUNTRY,
    SUPPLIER_CATEGORY,
    LEAD_TIME_DAYS,
    RELIABILITY_SCORE,
    TOTAL_PURCHASE_ORDERS,
    TOTAL_SPEND
FROM V_SUPPLIER_PERFORMANCE
"""

df = pd.read_sql(query, engine)

df.columns = df.columns.str.upper()

print(f"Extracted {len(df)} supplier records.")


# -----------------------------
# TRANSFORM
# -----------------------------

df["TOTAL_SPEND"] = df["TOTAL_SPEND"].round(2)

df["RELIABILITY_SCORE"] = df["RELIABILITY_SCORE"].round(2)

print("Supplier transformation complete.")


# -----------------------------
# LOAD
# -----------------------------

output_path = (
    Path(__file__).parent.parent
    / "data"
    / "supplier_performance.csv"
)

df.to_csv(output_path, index=False)

print(f"Saved transformed data to: {output_path}")


# -----------------------------
# Close connection
# -----------------------------

engine.dispose()

print("Oracle connection closed.")
print("Supplier ETL completed successfully!")