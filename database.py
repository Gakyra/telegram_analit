_user_portfolios = {}

def add_to_portfolio(user_id: int, asset: str, amount: float, price: float):
    if user_id not in _user_portfolios:
        _user_portfolios[user_id] = []
    _user_portfolios[user_id].append({
        "asset": asset,
        "amount": amount,
        "price": price
    })

def get_user_portfolio(user_id: int):
    return _user_portfolios.get(user_id, [])