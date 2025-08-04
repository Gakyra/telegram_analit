from app.models import PortfolioHistory

def get_user_portfolio(user_id):
    return PortfolioHistory.query.filter_by(user_id=user_id).all()
