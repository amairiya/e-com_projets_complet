from flask import Blueprint, jsonify, request
from services.product_service import load_products
from services.order_service import add_order


public_bp = Blueprint("public", __name__)


# @public_bp.route("/products")
# def products():
#     df = load_products()
#     return jsonify(df.to_dict(orient="records"))
@public_bp.route("/products")
def products():
    products_list = load_products()  # SQLAlchemy → liste de dicts
    return jsonify(products_list)    # pas besoin de .to_dict()

# @public_bp.route("/order", methods=["POST"])
# def order():
#     data = request.json
#     add_order(data["customer"], data["items"])
#     return jsonify({"status": "ok"})

@public_bp.route("/order", methods=["POST"])
def order():
    data = request.json
    print(data)
    customer = data.get("customer")
    items = data.get("items", [])
    print(items)
    if not customer or not items:
        return jsonify({"error": "Customer or items missing"}), 400

    order_number = add_order(customer, items)
    
    return jsonify({"status": "ok", "order_number": order_number})