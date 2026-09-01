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
SELECT *
FROM V_SUPPLY_CHAIN_SUMMARY
"""

df = pd.read_sql(query, engine)

# Ensure column names are uppercase
df.columns = df.columns.str.upper()

print(f"Extracted {len(df)} summary records.")


# -----------------------------
# TRANSFORM
# -----------------------------

# Round numeric values
for column in df.select_dtypes(include="number").columns:
    df[column] = df[column].round(2)

print("Supply chain summary transformation complete.")


# -----------------------------
# LOAD
# -----------------------------

output_path = (
    Path(__file__).parent.parent
    / "data"
    / "supply_chain_summary.csv"
)

df.to_csv(output_path, index=False)

print(f"Saved transformed data to: {output_path}")


# -----------------------------
# Close connection
# -----------------------------

engine.dispose()

print("Oracle connection closed.")
print("Supply Chain ETL completed successfully!")