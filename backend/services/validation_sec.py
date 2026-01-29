from decimal import Decimal
import re
from sqlalchemy import create_engine
from config import DATABASE_URL
from sqlalchemy import text

# Regex ultra-strict
NAME_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\- ]{1,50}$")  # lettres, chiffres, espaces, tirets, accents simples
PRICE_REGEX = re.compile(r"^\d+(\.\d{1,2})?$")  # format 5.00, 10.5
ID_REGEX = re.compile(r"^[1-9][0-9]*$")  # entiers positifs
QTY_REGEX = re.compile(r"^[1-9][0-9]{0,2}$")  # 1 à 999


import re

# Regex strict
NAME_CUSTUMER_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\- ]{1,50}$")  # lettres, chiffres, tirets, accents simples
EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")      # email simple
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")                 # chiffres + optionnel "+"
ADDRESS_REGEX = re.compile(r"^[A-Za-z0-9À-ÖØ-öø-ÿ ,\.\-]{5,100}$")  # lettres, chiffres, espaces, virgules, points, tirets


MAX_ITEMS = 50

# Create engine
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# # Optional: create a sessionmaker for convenience
# SessionLocal = sessionmaker(bind=engine)

def check_order_prices(items):
    validated_items = []
    total_price = Decimal("0.00")

    with engine.connect() as conn:
        for item in items:
            product_id = item["id"]
            quantity = item["quantity"]
            client_price = Decimal(item["price"])

            # ⚠️ Use text() to make raw SQL executable
            query = text("SELECT name, promo_price FROM products WHERE id = :id")
            result = conn.execute(query, {"id": product_id}).fetchone()

            if not result:
                raise ValueError(f"Product {product_id} not found")

            name, db_price = result
            db_price = Decimal(db_price)

            if client_price != db_price:
                raise ValueError(f"Price mismatch for product {product_id}: client {client_price} vs db {db_price}")

            line_total = db_price * quantity
            total_price += line_total

            validated_items.append({
                "id": product_id,
                "name": name,
                "price": str(db_price),
                "quantity": quantity
                # ,
                # "line_total": str(line_total)
            })

    return validated_items




def validate_items(items):
    """
    Vérifie une liste d'items pour prévenir payload malveillant.
    Retourne la liste validée ou lève ValueError.
    """
    if not isinstance(items, list) or not items or len(items) > MAX_ITEMS:
        raise ValueError("Invalid items list")

    validated_items = []

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each item must be a dict")

        item_id = str(item.get("id", ""))
        name = item.get("name", "")
        price = str(item.get("price", ""))
        quantity = str(item.get("quantity", ""))

        # Vérifications regex
        if not ID_REGEX.fullmatch(item_id):
            raise ValueError(f"Invalid id: {item_id}")

        if not NAME_REGEX.fullmatch(name):
            raise ValueError(f"Invalid name: {name}")

        if not PRICE_REGEX.fullmatch(price):
            raise ValueError(f"Invalid price: {price}")

        if not QTY_REGEX.fullmatch(quantity):
            raise ValueError(f"Invalid quantity: {quantity}")

        validated_items.append({
            "id": int(item_id),
            "name": name,
            "price": price,
            "quantity": int(quantity)
        })

    return validated_items






from decimal import Decimal

def process_total(items):
    """
    Calcule le total d'une commande à partir de la liste d'items validés.
    Ajoute 'line_total' pour chaque item et retourne le total général.
    """
    total_price = Decimal("0.00")
    processed_items = []

    for item in items:
        price = Decimal(item["price"])
        quantity = item["quantity"]
        line_total = price * quantity
        total_price += line_total

        processed_items.append({
            "id": item["id"],
            "name": item["name"],
            "price": str(price),
            "quantity": quantity,
            "line_total": str(line_total)
        })

    return processed_items, total_price






def validate_customer(customer):
    """
    Valide les champs du customer pour éviter payload malveillant.
    Retourne le customer nettoyé ou lève ValueError.
    """
    if not isinstance(customer, dict):
        raise ValueError("Customer must be a dict")

    name = customer.get("name", "")
    email = customer.get("email", "")
    phone = customer.get("phone", "")
    address = customer.get("address", "")

    if not NAME_CUSTUMER_REGEX.fullmatch(name):
        raise ValueError(f"Invalid customer name: {name}")
    if not EMAIL_REGEX.fullmatch(email):
        raise ValueError(f"Invalid customer email: {email}")
    if not PHONE_REGEX.fullmatch(phone):
        raise ValueError(f"Invalid customer phone: {phone}")
    if not ADDRESS_REGEX.fullmatch(address):
        raise ValueError(f"Invalid customer address: {address}")

    # Retourne le dict nettoyé pour usage sûr
    return {
        "name": name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "address": address.strip()
    }
