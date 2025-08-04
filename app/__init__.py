from flask import Flask
import os
from dotenv import load_dotenv
from flask_analit.extensions import db, login_manager, migrate

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.models import (
            User, Asset, Post, Comment,
            Forecast, Investment, PortfolioHistory
        )

    return app
