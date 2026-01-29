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
def export_table_Products_to_csv(csv_file):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM products"))

        rows = result.fetchall()
        headers = result.keys()

        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    print(f"Products exportés vers {csv_file} avec succès.")   
    

def import_products_from_csv(csv_file_path):
    # Lire le CSV
    with open(csv_file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]

    # Remplacer les produits
    with engine.begin() as conn:  # begin() pour transaction
        # Supprimer tous les produits existants
        conn.execute(text("DELETE FROM products"))

        # Insérer les nouveaux produits
        for row in rows:
            conn.execute(
                text("""
                    INSERT INTO products (name, price, promo_price, promo, description, images, product, stock)
                    VALUES (:name, :price, :promo_price, :promo, :description, :images, :product, :stock)
                """),
                {
                    "name": row.get("name"),
                    "price": float(row.get("price", 0)),
                    "promo_price": float(row.get("promo_price", 0)),
                    "promo": row.get("promo", "Non"),
                    "description": row.get("description"),
                    "images": row.get("images"),
                    "product": row.get("product"),
                    "stock": int(row.get("stock", 0))
                }
            )
