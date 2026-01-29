import csv
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from config import DATABASE_URL
from sqlalchemy import create_engine, text, Table, Column, Integer,DateTime, String, Float, MetaData, select, update


engine = create_engine(DATABASE_URL)

# -----------------------------
# Fonction pour exporter une table en CSV
# -----------------------------
def export_table_Orders_to_csv(csv_file):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM orders"))
        print("SELECT * FROM orders")
        print(result)

        rows = result.fetchall()
        headers = result.keys()

        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    print(f"Products exportés vers {csv_file} avec succès.")   
    

