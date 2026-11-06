import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_talisman import Talisman

from .routes import accounts_bp, init_storage


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        PORT=int(os.getenv("PORT", "8080")),
        DATABASE_PATH=os.getenv("DATABASE_PATH", "./data/accounts.db"),
        CORS_ORIGINS=os.getenv("CORS_ORIGINS", "*"),
        TALISMAN_FORCE_HTTPS=os.getenv("TALISMAN_FORCE_HTTPS", "false").lower() == "true",
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)

    origins = app.config["CORS_ORIGINS"]
    if isinstance(origins, str) and origins != "*":
        origins = [item.strip() for item in origins.split(",") if item.strip()]
    CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=False)

    Talisman(
        app,
        force_https=app.config["TALISMAN_FORCE_HTTPS"],
        content_security_policy={
            "default-src": ["'self'"],
            "object-src": ["'none'"],
            "frame-ancestors": ["'none'"],
        },
        referrer_policy="strict-origin-when-cross-origin",
    )

    init_storage(app.config["DATABASE_PATH"])
    app.register_blueprint(accounts_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "success", "message": "Customer Accounts service is healthy", "port": app.config["PORT"]}), 200

    @app.get("/")
    def index():
        return jsonify({"service": "Customer Accounts", "status": "running", "port": app.config["PORT"]}), 200

    return app
