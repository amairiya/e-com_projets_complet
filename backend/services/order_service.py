from datetime import datetime
from sqlalchemy import create_engine, text, Table, Column, Integer,DateTime, String, Float, MetaData, select, update
from config import DATABASE_URL , MAIL_SERVER , MAIL_PORT , MAIL_USE_TLS , MAIL_USERNAME , MAIL_PASSWORD , MAIL_DEFAULT_SENDER


import random
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


COLUMNS = [
    "date", "name", "email", "phone", "address",
    "product", "price", "quantity",
    "livré", "date_livré", "retourné", "date_retour", "fermé"
]

metadata = MetaData()

engine = create_engine(DATABASE_URL)



def load_orders():
    """Récupère toutes les commandes depuis la base de données."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM orders ORDER BY date DESC"))
        # Convertir chaque ligne en dictionnaire
        orders = [dict(row._mapping) for row in result]
    return orders




orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_number", String),
    Column("date", DateTime, default=datetime.utcnow),
    Column("name", String, nullable=False),
    Column("email", String),
    Column("phone", String),
    Column("address", String),
    Column("product", String),
    Column("price", Float),
    Column("quantity", Integer),
    Column("livré", String, default="Non"),
    Column("date_livré", DateTime, nullable=True),
    Column("retourné", String, default="Non"),
    Column("date_retour", DateTime, nullable=True),
    Column("fermé", String, default="Non")
)




def add_order(customer, items):
    """Ajoute des articles au panier et crée un order_number unique."""
    order_number = str(uuid.uuid4())  # Génère un UUID unique
    
    with engine.connect() as conn:
        for item in items:
            stmt = orders.insert().values(
                order_number=order_number,
                date=datetime.utcnow(),
                name=customer.get("name", ""),
                email=customer.get("email"),
                phone=customer.get("phone"),
                address=customer.get("address"),
                product=item.get("name"),
                price=item.get("price"),
                quantity=item.get("quantity"),
                livré="Non",
                date_livré=None,
                retourné="Non",
                date_retour=None,
                fermé="Non"
            )
            conn.execute(stmt)
        conn.commit()
        
        print("Facture HTML générée : facture.html")
                
    
        
    return order_number



def get_order_items(order_number):
    """Récupère tous les items d'une commande par order_number"""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM orders WHERE order_number=:num ORDER BY id"),
            {"num": order_number}
        )
        return [dict(row._mapping) for row in result]

def generate_invoice_html(order_number):
    items = get_order_items(order_number)
    if not items:
        return "<p>Aucune commande trouvée pour ce numéro.</p>"

    # Infos client
    client = items[0]

    total_sum = sum(item['price'] * item['quantity'] for item in items)

    # Génération HTML
    html = f"""
    <!DOCTYPE html>
    <html lang='fr'>
    <head>
        <meta charset='UTF-8'>
        <title>Facture {order_number}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

        <style>
            body {{
                background-color: #f8f9fa;
            }}

            .invoice-wrapper {{
                width: 25vw;            /* 1/4 de la page */
                min-width: 360px;
                margin: 40px ; 
                background: white;
                padding: 20px;
                border-radius: 6px;
            }}

            .invoice-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}

            .invoice-logo {{
                font-size: 1.3rem;
                font-weight: bold;
                color: #8B008B;
            }}

            .invoice-title {{
                font-size: 1.6rem;
                font-weight: bold;
            }}

            table {{
                font-size: 0.9rem;
            }}
        </style>
    </head>

    <body>
        <div class="invoice-wrapper shadow-sm">

            <div class="invoice-header">
                <div class="invoice-logo">💎 Bijoux & Glam</div>
                <div class="invoice-title">FACTURE</div>
            </div>

            <p><strong>Commande :</strong> {order_number}</p>
            <p><strong>Date :</strong> {client['date'].strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p><strong>Client :</strong> {client['name']}</p>
            <p><strong>Email :</strong> {client.get('email', '-')}</p>
            <p><strong>Téléphone :</strong> {client.get('phone', '-')}</p>
            <p><strong>Adresse :</strong> {client.get('address', '-')}</p>

            <table class="table table-bordered mt-3">
                <thead class="table-dark">
                    <tr>
                        <th>#</th>
                        <th>Produit</th>
                        <th>Prix</th>
                        <th>Qté</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
    """

    for idx, item in enumerate(items, start=1):
        total = item['price'] * item['quantity']
        html += f"""
                    <tr>
                        <td>{idx}</td>
                        <td>{item['product']}</td>
                        <td>{item['price']:.2f} €</td>
                        <td>{item['quantity']}</td>
                        <td>{total:.2f} €</td>
                    </tr>
        """

    html += f"""
                </tbody>
            </table>

            <h5 class="text-end mt-3">
                <strong>Total : {total_sum:.2f} €</strong>
            </h5>

        </div>
    </body>
    </html>
    """


    


    return html




def send_email(recipient_email,html):
    send_email_gmail(
        sender_email=MAIL_DEFAULT_SENDER,
        app_password=MAIL_PASSWORD,
        recipient_email=recipient_email,
        subject="Votre facture - Bijoux & Glam",
        html_content=html,
        text_content="Veuillez trouver votre facture en pièce jointe."
    )






def send_email_gmail(
    sender_email,
    app_password,
    recipient_email,
    subject,
    html_content,
    text_content=None
):
    """
    Envoie un email via Gmail (SMTP)

    sender_email   : email Gmail expéditeur
    app_password   : mot de passe d'application Gmail
    recipient_email : email destinataire
    subject        : sujet de l'email
    html_content   : contenu HTML
    text_content   : contenu texte (optionnel)
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    if text_content:
        msg.attach(MIMEText(text_content, "plain", "utf-8"))

    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)

        return True

    except Exception as e:
        print("Erreur envoi email :", e)
        return False