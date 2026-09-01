import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

connection = oracledb.connect(
    user=os.getenv("ORACLE_USER"),
    password=os.getenv("ORACLE_PASSWORD"),
    dsn=os.getenv("ORACLE_DSN")
)

print("Connected to Oracle successfully!")

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM PRODUCTS")

result = cursor.fetchone()

print("Products in database:", result[0])

cursor.close()
connection.close()

print("Connection closed.")