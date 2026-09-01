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
    SALES_ORDER_ID,
    ORDER_DATE,
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    QUANTITY_SOLD,
    SELLING_PRICE,
    UNIT_COST,
    SALES_REVENUE,
    ESTIMATED_PROFIT,
    CUSTOMER_REGION
FROM V_SALES_ANALYSIS
"""

df = pd.read_sql(query, engine)

df.columns = df.columns.str.upper()

print(f"Extracted {len(df)} sales records.")


# -----------------------------
# TRANSFORM
# -----------------------------

df["ORDER_DATE"] = pd.to_datetime(df["ORDER_DATE"])

df["PROFIT_MARGIN"] = (
    df["ESTIMATED_PROFIT"] / df["SALES_REVENUE"] * 100
).round(2)

df["SALES_REVENUE"] = df["SALES_REVENUE"].round(2)
df["ESTIMATED_PROFIT"] = df["ESTIMATED_PROFIT"].round(2)

print("Data transformation complete.")


# -----------------------------
# LOAD
# -----------------------------

output_path = Path(__file__).parent.parent / "data" / "sales_analysis.csv"

df.to_csv(output_path, index=False)

print(f"Saved transformed data to: {output_path}")


# -----------------------------
# Close connection
# -----------------------------
engine.dispose()

print("Oracle connection closed.")
print("ETL process completed successfully!")