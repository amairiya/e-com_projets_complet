from flask import Flask
from routes.public import public_bp
from routes.admin import admin_bp

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 512 * 1024  # 512 KB
app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
