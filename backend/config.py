import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PRODUCT_FILE = os.path.join(BASE_DIR, "data/products.xlsx")
# ORDER_FILE = os.path.join(BASE_DIR, "data/orders.xlsx")

SECRET_KEY = os.getenv("SECRET_KEY", "change_me_secret")
JWT_EXPIRE_HOURS = 24

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

DATABASE_URL = "postgresql://user:password@db:5432/mydb"

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True

API_KEY_PRIMARY = os.getenv("API_KEY_PRIMARY")
API_KEY_SECONDARY = os.getenv("API_KEY_SECONDARY")

# app-bijoux.glam
MAIL_USERNAME = "bijoux.glam.contact@gmail.com"
MAIL_PASSWORD = "rker ouil hqpq nmdk"
MAIL_DEFAULT_SENDER = "bijoux.glam.contact@gmail.com"


POSTGRES_USER=os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD= os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB= os.getenv("POSTGRES_DB", "mydb")
