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
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    WAREHOUSE_ID,
    WAREHOUSE_NAME,
    QUANTITY_ON_HAND,
    QUANTITY_RESERVED,
    AVAILABLE_QUANTITY,
    REORDER_POINT,
    SAFETY_STOCK,
    INVENTORY_STATUS
FROM V_INVENTORY_RISK
"""

df = pd.read_sql(query, engine)

df.columns = df.columns.str.upper()

print(f"Extracted {len(df)} inventory records.")


# -----------------------------
# TRANSFORM
# -----------------------------

df["AVAILABLE_QUANTITY"] = (
    df["QUANTITY_ON_HAND"] - df["QUANTITY_RESERVED"]
)

print("Inventory transformation complete.")


# -----------------------------
# LOAD
# -----------------------------

output_path = Path(__file__).parent.parent / "data" / "inventory_risk.csv"

df.to_csv(output_path, index=False)

print(f"Saved transformed data to: {output_path}")


# -----------------------------
# Close connection
# -----------------------------

engine.dispose()

print("Oracle connection closed.")
print("Inventory ETL completed successfully!")