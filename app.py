from flask import Flask
import os
from flask_analit.extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    print(f"[LOG] Flask подключился к базе: {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    #  ИМПОРТИРУЕМ МОДЕЛИ ПОСЛЕ ИНИЦИАЛИЗАЦИИ
    with app.app_context():
        from flask_analit.models import (
            User, Asset, Post, Comment,
            Forecast, Investment, PortfolioHistory
        )

    return app

