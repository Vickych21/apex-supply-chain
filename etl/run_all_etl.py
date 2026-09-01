import subprocess
import sys


# -----------------------------
# ETL scripts
# -----------------------------

etl_scripts = [
    "sales_etl.py",
    "inventory_etl.py",
    "supplier_etl.py",
    "shipment_etl.py",
    "supply_chain_etl.py",
    "excel_etl.py",
    "sharepoint_etl.py",
]


# -----------------------------
# Run ETL pipelines
# -----------------------------

print("=" * 60)
print("APEX SUPPLY CHAIN - MASTER ETL PIPELINE")
print("=" * 60)

for script in etl_scripts:

    print()
    print("-" * 60)
    print(f"Running: {script}")
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, script],
        cwd="etl"
    )

    if result.returncode != 0:
        print()
        print(f"ERROR: {script} failed.")
        sys.exit(result.returncode)

    print(f"{script} completed successfully.")


print()
print("=" * 60)
print("ALL ETL PIPELINES COMPLETED SUCCESSFULLY!")
print("=" * 60)