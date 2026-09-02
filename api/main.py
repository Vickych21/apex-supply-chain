from fastapi import FastAPI
import os
import csv
import oracledb
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Apex Electronics Supply Chain API",
    description="REST API for supply chain analytics and operations",
    version="1.0.0"
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

# Azure will set AZURE_MODE=true.
# Local development continues to use Oracle.
AZURE_MODE = os.getenv("AZURE_MODE", "false").lower() == "true"

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data"
)


# ---------------------------------------------------------
# Oracle Connection - Local Development
# ---------------------------------------------------------

def get_connection():
    dsn = os.getenv("ORACLE_DOCKER_DSN") or os.getenv("ORACLE_DSN")

    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=dsn
    )


# ---------------------------------------------------------
# CSV Helper - Azure
# ---------------------------------------------------------

def read_csv(filename):
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, mode="r", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Apex Electronics Supply Chain API",
        "status": "running",
        "environment": "azure-csv" if AZURE_MODE else "local-oracle"
    }


# ---------------------------------------------------------
# Products
# ---------------------------------------------------------

@app.get("/products")
def get_products():

    if AZURE_MODE:
        rows = read_csv("inventory_risk.csv")

        products = {}

        for row in rows:
            product_id = int(row["PRODUCT_ID"])

            products[product_id] = {
                "product_id": product_id,
                "product_name": row["PRODUCT_NAME"],
                "category": row["CATEGORY"]
            }

        return sorted(
            products.values(),
            key=lambda x: x["product_id"]
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            PRODUCT_ID,
            PRODUCT_NAME
        FROM PRODUCTS
        ORDER BY PRODUCT_ID
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "product_id": row[0],
            "product_name": row[1]
        }
        for row in rows
    ]


# ---------------------------------------------------------
# Suppliers
# ---------------------------------------------------------

@app.get("/suppliers")
def get_suppliers():

    if AZURE_MODE:
        rows = read_csv("supplier_performance.csv")

        return [
            {
                "supplier_id": int(row["SUPPLIER_ID"]),
                "supplier_name": row["SUPPLIER_NAME"],
                "country": row["COUNTRY"],
                "supplier_category": row["SUPPLIER_CATEGORY"],
                "lead_time_days": int(row["LEAD_TIME_DAYS"]),
                "reliability_score": float(row["RELIABILITY_SCORE"]),
                "total_purchase_orders": int(row["TOTAL_PURCHASE_ORDERS"]),
                "total_spend": float(row["TOTAL_SPEND"])
            }
            for row in rows
        ]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SUPPLIER_ID,
            SUPPLIER_NAME,
            COUNTRY,
            SUPPLIER_CATEGORY,
            LEAD_TIME_DAYS,
            RELIABILITY_SCORE
        FROM SUPPLIERS
        ORDER BY SUPPLIER_ID
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "supplier_id": row[0],
            "supplier_name": row[1],
            "country": row[2],
            "supplier_category": row[3],
            "lead_time_days": row[4],
            "reliability_score": row[5]
        }
        for row in rows
    ]


# ---------------------------------------------------------
# Inventory
# ---------------------------------------------------------

@app.get("/inventory")
def get_inventory():

    if AZURE_MODE:
        rows = read_csv("inventory_risk.csv")

        inventory = []

        inventory_id = 1

        for row in rows:
            inventory.append({
                "inventory_id": inventory_id,
                "product_id": int(row["PRODUCT_ID"]),
                "product_name": row["PRODUCT_NAME"],
                "category": row["CATEGORY"],
                "warehouse_id": int(row["WAREHOUSE_ID"]),
                "warehouse_name": row["WAREHOUSE_NAME"],
                "quantity_on_hand": int(row["QUANTITY_ON_HAND"]),
                "quantity_reserved": int(row["QUANTITY_RESERVED"]),
                "available_quantity": int(row["AVAILABLE_QUANTITY"]),
                "reorder_point": int(row["REORDER_POINT"]),
                "safety_stock": int(row["SAFETY_STOCK"]),
                "inventory_status": row["INVENTORY_STATUS"]
            })

            inventory_id += 1

        return inventory

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            i.INVENTORY_ID,
            i.PRODUCT_ID,
            p.PRODUCT_NAME,
            i.WAREHOUSE_ID,
            w.WAREHOUSE_NAME,
            i.QUANTITY_ON_HAND,
            i.QUANTITY_RESERVED,
            i.LAST_UPDATED
        FROM INVENTORY i
        JOIN PRODUCTS p
            ON i.PRODUCT_ID = p.PRODUCT_ID
        JOIN WAREHOUSES w
            ON i.WAREHOUSE_ID = w.WAREHOUSE_ID
        ORDER BY i.INVENTORY_ID
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "inventory_id": row[0],
            "product_id": row[1],
            "product_name": row[2],
            "warehouse_id": row[3],
            "warehouse_name": row[4],
            "quantity_on_hand": row[5],
            "quantity_reserved": row[6],
            "last_updated": row[7]
        }
        for row in rows
    ]


# ---------------------------------------------------------
# Shipments
# ---------------------------------------------------------

@app.get("/shipments")
def get_shipments():

    if AZURE_MODE:
        rows = read_csv("shipment_performance.csv")

        shipments = []

        for row in rows:
            shipments.append({
                "shipment_id": int(row["SHIPMENT_ID"]),
                "po_id": int(row["PO_ID"]),
                "supplier_id": int(row["SUPPLIER_ID"]),
                "supplier_name": row["SUPPLIER_NAME"],
                "tracking_number": row["TRACKING_NUMBER"],
                "carrier": row["CARRIER"],
                "ship_date": row["SHIP_DATE"],
                "expected_arrival_date": row["EXPECTED_ARRIVAL_DATE"],
                "actual_arrival_date": row["ACTUAL_ARRIVAL_DATE"] or None,
                "status": row["STATUS"],
                "origin_location": row["ORIGIN_LOCATION"],
                "destination_location": row["DESTINATION_LOCATION"],
                "transit_days": (
                    float(row["TRANSIT_DAYS"])
                    if row["TRANSIT_DAYS"]
                    else None
                ),
                "days_early_late": (
                    float(row["DAYS_EARLY_LATE"])
                    if row["DAYS_EARLY_LATE"]
                    else None
                ),
                "delivery_performance": row["DELIVERY_PERFORMANCE"]
            })

        return shipments

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SHIPMENT_ID,
            PO_ID,
            TRACKING_NUMBER,
            CARRIER,
            SHIP_DATE,
            EXPECTED_ARRIVAL_DATE,
            ACTUAL_ARRIVAL_DATE,
            ORIGIN_LOCATION,
            DESTINATION_LOCATION,
            STATUS,
            CREATED_DATE
        FROM SHIPMENTS
        ORDER BY SHIPMENT_ID
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "shipment_id": row[0],
            "po_id": row[1],
            "tracking_number": row[2],
            "carrier": row[3],
            "ship_date": row[4],
            "expected_arrival_date": row[5],
            "actual_arrival_date": row[6],
            "origin_location": row[7],
            "destination_location": row[8],
            "status": row[9],
            "created_date": row[10]
        }
        for row in rows
    ]


# ---------------------------------------------------------
# Purchase Orders
# ---------------------------------------------------------

@app.get(
    "/purchase-orders",
    summary="Get Purchase Order Analytics",
    description="Returns monthly supplier purchase-order performance analytics generated by the ETL pipeline."
)
def get_purchase_orders():

    if AZURE_MODE:
        rows = read_csv("supplier_excel_analysis.csv")

        purchase_orders = []

        po_id = 1

        for row in rows:
            purchase_orders.append({
                "po_id": po_id,
                "supplier_id": int(row["SUPPLIER_ID"]),
                "supplier_name": row["SUPPLIER_NAME"],
                "report_month": row["REPORT_MONTH"],
                "purchase_orders": int(row["PURCHASE_ORDERS"]),
                "units_ordered": int(row["UNITS_ORDERED"]),
                "total_spend": float(row["TOTAL_SPEND"]),
                "average_lead_time_days": float(
                    row["AVERAGE_LEAD_TIME_DAYS"]
                ),
                "on_time_delivery_rate": float(
                    row["ON_TIME_DELIVERY_RATE"]
                ),
                "delayed_orders": int(row["DELAYED_ORDERS"]),
                "defect_rate": float(row["DEFECT_RATE"]),
                "delay_rate": float(row["DELAY_RATE"]),
                "performance_status": row["PERFORMANCE_STATUS"]
            })

            po_id += 1

        return purchase_orders

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            po.PO_ID,
            po.SUPPLIER_ID,
            s.SUPPLIER_NAME,
            po.ORDER_DATE,
            po.EXPECTED_DELIVERY_DATE,
            po.ACTUAL_DELIVERY_DATE,
            po.STATUS,
            po.TOTAL_AMOUNT,
            po.CREATED_DATE
        FROM PURCHASE_ORDERS po
        JOIN SUPPLIERS s
            ON po.SUPPLIER_ID = s.SUPPLIER_ID
        ORDER BY po.PO_ID
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "po_id": row[0],
            "supplier_id": row[1],
            "supplier_name": row[2],
            "order_date": row[3],
            "expected_delivery_date": row[4],
            "actual_delivery_date": row[5],
            "status": row[6],
            "total_amount": row[7],
            "created_date": row[8]
        }
        for row in rows
    ]