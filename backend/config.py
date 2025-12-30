import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PRODUCT_FILE = os.path.join(BASE_DIR, "data/products.xlsx")
ORDER_FILE = os.path.join(BASE_DIR, "data/orders.xlsx")

SECRET_KEY = os.getenv("SECRET_KEY", "change_me_secret")
JWT_EXPIRE_HOURS = 24

ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

DATABASE_URL = "postgresql://user:password@db:5432/mydb"
