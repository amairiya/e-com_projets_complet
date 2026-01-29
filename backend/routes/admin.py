from flask import Blueprint, request, jsonify , send_file , Response
import os
from utils.auth import generate_token, check_login, admin_required
from services.product_service import load_products , delete_product  , add_product
from services.order_service import load_orders
from services.order_service import generate_invoice_html

from services.upload_porduct_service import export_table_Products_to_csv
from services.upload_porduct_service import import_products_from_csv

from services.upload_orders_service import export_table_Orders_to_csv


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/login", methods=["POST"])
def login():
    data = request.json
    print(data)
    if check_login(data["user"], data["password"] , data["primary_key"] , data["secondary_key"]):
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

