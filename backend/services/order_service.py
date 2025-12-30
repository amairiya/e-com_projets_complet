from datetime import datetime
from config import ORDER_FILE
from sqlalchemy import create_engine, text, Table, Column, Integer,DateTime, String, Float, MetaData, select, update
from config import DATABASE_URL
import random

COLUMNS = [
    "date", "name", "email", "phone", "address",
    "product", "price", "quantity",
    "livré", "date_livré", "retourné", "date_retour", "fermé"
]

metadata = MetaData()

engine = create_engine(DATABASE_URL)



def load_orders():
    """Récupère toutes les commandes depuis la base de données."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM orders ORDER BY date DESC"))
        # Convertir chaque ligne en dictionnaire
        orders = [dict(row._mapping) for row in result]
    return orders


# orders = Table(
#     "orders",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("date", DateTime, default=datetime.utcnow),
#     Column("name", String),
#     Column("email", String),
#     Column("phone", String),
#     Column("address", String),
#     Column("product", String),
#     Column("price", Float),
#     Column("quantity", Integer),
#     Column("livré", String, default="Non"),
#     Column("date_livré", DateTime, nullable=True),
#     Column("retourné", String, default="Non"),
#     Column("date_retour", DateTime, nullable=True),
#     Column("fermé", String, default="Non")
# )

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_number", String, unique=True),
    Column("date", DateTime, default=datetime.utcnow),
    Column("name", String, nullable=False),
    Column("email", String),
    Column("phone", String),
    Column("address", String),
    Column("product", String),
    Column("price", Float),
    Column("quantity", Integer),
    Column("livré", String, default="Non"),
    Column("date_livré", DateTime, nullable=True),
    Column("retourné", String, default="Non"),
    Column("date_retour", DateTime, nullable=True),
    Column("fermé", String, default="Non")
)

# def add_order(customer, items):
#     with engine.connect() as conn:
#         for item in items:
#             stmt = orders.insert().values(
#                 date=datetime.utcnow(),
#                 name=customer.get("name", ""),
#                 email=customer.get("email"),
#                 phone=customer.get("phone"),
#                 address=customer.get("address"),
#                 product=item.get("name"),
#                 price=item.get("price"),
#                 quantity=item.get("quantity"),
#                 livré="Non",
#                 date_livré= None ,
#                 retourné="Non",
#                 date_retour= None,
#                 fermé="Non"
#             )
#             conn.execute(stmt)
#         conn.commit()

def generate_order_number():
    """Génère un numéro de commande unique basé sur la date + un nombre aléatoire."""
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = str(random.randint(1000, 9999))
    return f"{date_part}-{random_part}"

def add_order(customer, items):
    """Ajoute des articles au panier et crée un order_number unique."""
    order_number = generate_order_number()
    
    with engine.connect() as conn:
        for item in items:
            stmt = orders.insert().values(
                order_number=order_number,
                date=datetime.utcnow(),
                name=customer.get("name", ""),
                email=customer.get("email"),
                phone=customer.get("phone"),
                address=customer.get("address"),
                product=item.get("name"),
                price=item.get("price"),
                quantity=item.get("quantity"),
                livré="Non",
                date_livré=None,
                retourné="Non",
                date_retour=None,
                fermé="Non"
            )
            conn.execute(stmt)
        conn.commit()
    return order_number