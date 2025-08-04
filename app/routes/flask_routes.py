from flask import Blueprint, jsonify
from app.services.portfolio_service import get_user_portfolio

bp = Blueprint("api", __name__)

@bp.route("/api/portfolio/<int:user_id>")
def portfolio(user_id):
    data = get_user_portfolio(user_id)
    return jsonify([{"asset": p.asset_name, "amount": p.amount} for p in data])
