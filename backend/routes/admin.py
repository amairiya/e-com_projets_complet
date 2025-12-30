from flask import Blueprint, request, jsonify
from utils.auth import generate_token, check_login, admin_required
from services.product_service import load_products , delete_product  , add_product
from services.order_service import load_orders

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/login", methods=["POST"])
def login():
    data = request.json
    if check_login(data["user"], data["password"]):
        token = generate_token(data["user"])
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401


@admin_bp.route("/admin/products", methods=["GET", "PUT", "POST"])
@admin_required
def products():
    if request.method == "GET":
        return jsonify(load_products())

    # POST pour ajouter un produit
    product = request.json  # doit être un dict, pas une liste
    if not product.get("id"):
        return jsonify({"status": "error", "message": "ID requis"}), 400

    from services.product_service import add_product
    result = add_product(product)
    return jsonify(result)


@admin_bp.route("/admin/orders")
@admin_required
def orders():
    return jsonify(load_orders())

@admin_bp.route("/admin/products/<int:product_id>", methods=["DELETE"])
@admin_required
def remove_product(product_id):
    """Supprime un produit par son ID"""
    deleted_count = delete_product(product_id)
    if deleted_count:
        return jsonify({"status": "ok", "message": "Produit supprimé"})
    else:
        return jsonify({"status": "error", "message": "Produit introuvable"}), 404