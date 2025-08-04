from app.models import Forecast

def get_latest_forecasts():
    return Forecast.query.order_by(Forecast.created_at.desc()).limit(5).all()
