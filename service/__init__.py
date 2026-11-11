import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__, template_folder="../templates")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL", "sqlite:////tmp/product_catalogue.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
    )
    if config:
        app.config.update(config)

    db.init_app(app)

    from service.routes import products_bp

    app.register_blueprint(products_bp)

    with app.app_context():
        db.create_all()

    return app
