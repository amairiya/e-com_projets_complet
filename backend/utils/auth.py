import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from flask import request, jsonify
from functools import wraps
from config import SECRET_KEY, JWT_EXPIRE_HOURS, ADMIN_USER, ADMIN_PASSWORD_HASH , API_KEY_PRIMARY , API_KEY_SECONDARY
import time

from services.logger import log


DELAY_SECONDS = 10  # délai en secondes entre chaque tentative

def generate_token(username):
    payload = {
        "user": username,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    log(f"Token JWT généré pour {username}", level="INFO")
    return token


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


def check_login(username, password, key1, key2):
    """
    Vérifie login + mot de passe + clés API et log chaque tentative
    """
    # pause avant validation pour limiter brute-force
    # time.sleep(DELAY_SECONDS)  # décommente si tu veux un délai global

    if username != ADMIN_USER:
        log(f"Tentative login échouée: utilisateur incorrect ({username})", level="WARNING")
        return False

    if key1 != API_KEY_PRIMARY or key2 != API_KEY_SECONDARY:
        log(f"Tentative login échouée: clés API incorrectes (key1={key1}, key2={key2})", level="WARNING")
        return False

    if not check_password_hash(ADMIN_PASSWORD_HASH, password):
        log(f"Tentative login échouée: mot de passe incorrect pour {username}", level="WARNING")
        return False

    # Succès
    log(f"Login réussi pour {username}", level="INFO")
    return True