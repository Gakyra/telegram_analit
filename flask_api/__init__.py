from flask import Flask
from flask_analit.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("flask_api.config.Config")

    db.init_app(app)

    # 📦 Подключение маршрутов
    from flask_api.routes.portfolio import portfolio_bp
    app.register_blueprint(portfolio_bp)

    return app
