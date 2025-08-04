from flask_analit.extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    risk_profile = db.Column(db.String(20))

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(50))
    category = db.Column(db.String(50))

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(50))
    prediction = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PortfolioHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    asset_name = db.Column(db.String(50))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class log_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
