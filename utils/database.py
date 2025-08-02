import os
import sys
from flask import Flask

# Добавляем путь к flask_analit, если не установлен как пакет
current_dir = os.path.dirname(os.path.abspath(__file__))
flask_analit_path = os.path.join(current_dir, '..', 'flask_analit')
sys.path.append(flask_analit_path)

# Импорты из flask_analit
from flask_analit.extensions import db
from flask_analit.models import User, Investment

# Инициализируем Flask-контекст для SQLAlchemy
def init_flask_context():
    app = Flask(__name__)
    app.config.from_object("flask_analit.config")  # при наличии flask_analit/config.py
    db.init_app(app)
    return app

app = init_flask_context()

def get_user_portfolio(telegram_id):
    with app.app_context():
        user = User.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            return "Пользователь не найден."

        investments = Investment.query.filter_by(user_id=user.id).all()
        if not investments:
            return "Портфель пуст."

        assets = [f"{inv.name} ({inv.symbol}) — {inv.quantity} шт." for inv in investments]
        return "\n".join(assets)

