from flask import Blueprint, jsonify, request
from services.product_service import load_products
from services.order_service import add_order , generate_invoice_html , send_email

from services.validation_sec import check_order_prices , validate_items , process_total , validate_customer

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
#     print(data)
#     customer = data.get("customer")
#     items = data.get("items", [])
#     print(items)
#     if not customer or not items:
#         return jsonify({"error": "Customer or items missing"}), 400

#     order_number = add_order(customer, items)
    
#     return jsonify({"status": "ok", "order_number": order_number})





@public_bp.route("/order", methods=["POST"])
def order():
    print("=== /order endpoint called ===")
    
    

    data = request.json
    print("Raw request data:", data)
    customer = data.get("customer")
    
    # 1️⃣ Validation customer
    try:
        customer_validated = validate_customer(customer)
        print("Customer validated:", customer_validated)
    except ValueError as e:
        print("Customer validation error:", e)
        return jsonify({"error": f"Invalid customer data: {e}"}), 400
    
    items = data.get("items")
    print("Received items:", items)

    # 1️⃣ Validation regex anti-malware
    try:
        items_validated = validate_items(items)
        print("Items validated:", items_validated)
    except ValueError as e:
        print("Validation error:", e)
        return jsonify({"error": str(e)}), 400

    # 2️⃣ Vérification prix réel en DB
    try:
        # items_checked = check_order_prices(items_validated)
        items_checked= check_order_prices(items_validated)
        print("Items checked against DB prices:", items_checked)
        total = process_total(items_checked)
        _ , total = process_total(items_checked)
        print("Total order price:", total)
    except ValueError as e:
        print("Price check error:", e)
        return jsonify({"error": str(e)}), 400
    
    

    # 3️⃣ Processus commande (ex : add_order)
    order_number = add_order(customer_validated , items_checked)
    print("Order added with order_number:", order_number)

    response = {
        "status": "ok",
        "order_number": order_number,
        "total": str(total),
        "items": items_checked
    }
    
    html = generate_invoice_html(order_number)
    send_email(customer_validated.get("email"),html)

    print("Response sent:", response)

    return jsonify(response), 201

    