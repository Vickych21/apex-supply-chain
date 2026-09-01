from fastapi import FastAPI
import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Apex Electronics Supply Chain API",
    description="REST API for supply chain analytics and operations",
    version="1.0.0"
)


def get_connection():
    # Use the Docker Oracle connection when available.
    # Otherwise, use the normal local Oracle connection.
    dsn = os.getenv("ORACLE_DOCKER_DSN") or os.getenv("ORACLE_DSN")

    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=dsn
    )


@app.get("/")
def root():
    return {
        "message": "Apex Electronics Supply Chain API",
        "status": "running"
    }


@app.get("/products")
def get_products():
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


@app.get("/suppliers")
def get_suppliers():
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


@app.get("/inventory")
def get_inventory():
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


@app.get("/shipments")
def get_shipments():
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


@app.get("/purchase-orders")
def get_purchase_orders():
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