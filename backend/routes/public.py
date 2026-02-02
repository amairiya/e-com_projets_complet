from flask import Blueprint, jsonify, request , g
from services.product_service import load_products
from services.order_service import add_order , generate_invoice_html , send_email
import time
from services.validation_sec import check_order_prices , validate_items , process_total , validate_customer
from services.logger import log

public_bp = Blueprint("public", __name__)

@public_bp.before_request
def start_timer():
    g.start_time = time.time()
    
@public_bp.after_request
def after_request(response):
    log_access(
        message="request_completed",
        status=response.status_code,
        # duration_ms si tu mesures le temps
        # order_number si tu veux
    )
    return response


def log_access(message, status=None, duration_ms=None, order_number=None, level="INFO"):
    log(
        message=str(message),
        level=level,
        ip=request.headers.get("X-Forwarded-For", request.remote_addr),
        method=request.method,
        path=request.path,
        status=status,
        duration_ms=duration_ms,
        order_number=order_number
    )



@public_bp.route("/products")
def products():
    start = time.time()

    log_access("products_requested")

    products_list = load_products()

    duration_ms = int((time.time() - start) * 1000)

    log_access(
        "products_returned",
        status=200,
        duration_ms=duration_ms
    )

    return jsonify(products_list)




@public_bp.route("/order", methods=["POST"])
def order():
    start = time.time()

    log_access("order_request_received")

    data = request.json or {}
    customer = data.get("customer")
    items = data.get("items")

    # 1️⃣ Validation customer
    try:
        customer_validated = validate_customer(customer)
    except ValueError:
        log_access(
            "invalid_customer",
            level="WARNING",
            status=400
        )
        return jsonify({"error": "Invalid customer data"}), 400

    # 2️⃣ Validation items
    try:
        items_validated = validate_items(items)
    except ValueError as e:
        log_access(
            "invalid_items",
            level="WARNING",
            status=400
        )
        return jsonify({"error": str(e)}), 400

    # 3️⃣ Vérification prix
    try:
        items_checked = check_order_prices(items_validated)
        _, total = process_total(items_checked)
    except ValueError as e:
        log_access(
            "price_validation_failed",
            level="WARNING",
            status=400
        )
        return jsonify({"error": str(e)}), 400

    # 4️⃣ Création commande
    order_number = add_order(customer_validated, items_checked)

    duration_ms = int((time.time() - start) * 1000)

    log_access(
        "order_created",
        status=201,
        duration_ms=duration_ms,
        order_number=order_number
    )

    # 5️⃣ Email
    try:
        html = generate_invoice_html(order_number)
        send_email(customer_validated.get("email"), html)
    except Exception:
        log_access(
            "order_email_failed",
            level="ERROR",
            order_number=order_number
        )

    return jsonify({
        "status": "ok",
        "order_number": order_number,
        "total": str(total),
        "items": items_checked
    }), 201


    