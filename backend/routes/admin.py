from flask import Blueprint, request, jsonify , send_file , Response ,g
import os
import time
from utils.auth import generate_token, check_login, admin_required
from services.product_service import load_products , delete_product  , add_product
from services.order_service import load_orders
from services.order_service import generate_invoice_html

from services.upload_porduct_service import export_table_Products_to_csv
from services.upload_porduct_service import import_products_from_csv

from services.upload_orders_service import export_table_Orders_to_csv

from services.logger import log

admin_bp = Blueprint("admin", __name__)

@admin_bp.before_request
def start_timer():
    g.start_time = time.time()
    
@admin_bp.after_request
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

@admin_bp.route("/admin/login", methods=["POST"])
def login():
    data = request.json

    if check_login(data["user"], data["password"], data["primary_key"], data["secondary_key"]):
        token = generate_token(data["user"])
        log_access(
            message=f"admin_login_success | user={data['user']}",
            status=200,
            level="INFO"
        )
        return jsonify({"token": token})
    else:
        log_access(
            message=f"admin_login_failed | user={data.get('user')}",
            status=401,
            level="WARNING"
        )
        return jsonify({"error": "Invalid credentials"}), 401


@admin_bp.route("/admin/products", methods=["GET", "PUT", "POST"])
@admin_required
def products():
    if request.method == "GET":
        log_access(message="admin_view_products", status=200, level="INFO")
        return jsonify(load_products())

    # POST pour ajouter un produit
    product = request.json  # doit être un dict
    if not product.get("id"):
        log_access(
            message="admin_add_product_failed | missing_id",
            status=400,
            level="WARNING"
        )
        return jsonify({"status": "error", "message": "ID requis"}), 400

    from services.product_service import add_product
    result = add_product(product)
    log_access(
        message=f"admin_add_product | product_id={product['id']}",
        status=200,
        level="INFO"
    )
    return jsonify(result)


@admin_bp.route("/admin/orders")
@admin_required
def orders():
    log_access(message="admin_view_orders", status=200, level="INFO")
    return jsonify(load_orders())


@admin_bp.route("/admin/products/<int:product_id>", methods=["DELETE"])
@admin_required
def remove_product(product_id):
    """Supprime un produit par son ID"""
    deleted_count = delete_product(product_id)
    if deleted_count:
        log_access(
            message=f"admin_remove_product | product_id={product_id}",
            status=200,
            level="INFO"
        )
        return jsonify({"status": "ok", "message": "Produit supprimé"})
    else:
        log_access(
            message=f"admin_remove_product_failed | product_id={product_id}",
            status=404,
            level="WARNING"
        )
        return jsonify({"status": "error", "message": "Produit introuvable"}), 404
    
    

@admin_bp.route("/admin/export/products", methods=["GET"])
@admin_required
def export_table():
    export_table_Products_to_csv("products.csv")

    return send_file(
        "products.csv",
        mimetype="text/csv",
        as_attachment=True,
        download_name="products.csv"
    )



@admin_bp.route("/admin/upload/products", methods=["POST"])
@admin_required
def upload_products():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Sauvegarder temporairement
    tmp_path = f"/tmp/{file.filename}"
    file.save(tmp_path)

    try:
        import_products_from_csv(tmp_path)
        return jsonify({"success": f"Products imported from {file.filename}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(tmp_path)
        
        
        
# -----------------------------
# Endpoint pour le frontend
# -----------------------------
@admin_bp.route("/admin/invoice/<order_number>", methods=["GET"])
@admin_required
def invoice(order_number):
    # Ici tu peux ajouter ton @admin_required si nécessaire
    html = generate_invoice_html(order_number)
        # Renvoie directement le HTML avec le bon type MIME
    return html, 200, {"Content-Type": "text/html"}








@admin_bp.route("/admin/export/orders", methods=["GET"])
@admin_required
def export_table_orders():
    export_table_Orders_to_csv("orders.csv")

    return send_file(
        "orders.csv",
        mimetype="text/csv",
        as_attachment=True,
        download_name="orders.csv"
    )

