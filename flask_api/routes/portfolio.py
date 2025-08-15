from flask import Blueprint, jsonify
from flask_analit.extensions import db
from app.models import PortfolioHistory

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("/api/portfolio/<int:user_id>", methods=["GET"])
def get_portfolio(user_id):
    assets = PortfolioHistory.query.filter_by(user_id=user_id).all()
    result = [
        {"asset_name": asset.asset_name, "amount": asset.amount}
        for asset in assets
    ]
    return jsonify({"assets": result})
