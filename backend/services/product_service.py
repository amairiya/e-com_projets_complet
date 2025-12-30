from sqlalchemy import create_engine, text, Table, Column, Integer, String, Float, MetaData, select, update
from config import DATABASE_URL

# Configuration de la base de données
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Définition de la table products
products_table = Table(
    "products", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("product", String(255), nullable=False),
    Column("price", Float, nullable=False),
    Column("promo_price", Float, nullable=False),
    Column("promo", String(50), default="Non"),
    Column("description", String(1000), default=""),
    Column("images", String(1000), default=""),
    Column("stock", Integer, default=0)
)

# Charger tous les produits
def load_products():
    with engine.connect() as conn:
        # Utiliser text() pour une requête SQL brute
        result = conn.execute(text("SELECT * FROM products"))
        products = [dict(row._mapping) for row in result]
    return products


# Sauvegarder ou mettre à jour la liste des produits
def add_product(product):
    with engine.connect() as conn:
        # vérifier si l'ID existe déjà
        existing = conn.execute(select(products_table).where(products_table.c.id == product["id"])).fetchone()
        if existing:
            return {"status": "error", "message": "ID existe déjà"}

        # insérer le produit
        stmt = products_table.insert().values(
            id=product["id"],
            name=product.get("name", ""),
            product=product.get("name", ""),
            price=product.get("price", 0),
            promo_price=product.get("promo_price", 0),
            promo=product.get("promo", "non"),
            description=product.get("description", ""),
            images=product.get("images", ""),
            stock=product.get("stock", 0)
        )
        conn.execute(stmt)
        conn.commit()
        return {"status": "ok"}

def delete_product(product_id):
    """Supprime un produit par son ID"""
    with engine.connect() as conn:
        stmt = products_table.delete().where(products_table.c.id == product_id)
        result = conn.execute(stmt)
        conn.commit()
        return result.rowcount  # nombre de lignes supprimées