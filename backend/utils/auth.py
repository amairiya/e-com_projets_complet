import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from flask import request, jsonify
from functools import wraps
from config import SECRET_KEY, JWT_EXPIRE_HOURS, ADMIN_USER, ADMIN_PASSWORD_HASH , API_KEY_PRIMARY , API_KEY_SECONDARY
import time

DELAY_SECONDS = 10  # délai en secondes entre chaque tentative

def generate_token(username):
    payload = {
        "user": username,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth.split(" ")[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper


def check_login(username, password , key1 , key2):
    # pause avant toute validation
    # time.sleep(DELAY_SECONDS)

    if username != ADMIN_USER or key1 != API_KEY_PRIMARY or key2 != API_KEY_SECONDARY:
        return False
    return check_password_hash(ADMIN_PASSWORD_HASH, password)

