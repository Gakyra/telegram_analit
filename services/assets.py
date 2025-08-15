def get_available_assets():
    return ["BTC", "ETH", "SOL", "BNB"]

def get_asset_price(asset: str) -> float:
    prices = {
        "BTC": 65000.0,
        "ETH": 3400.0,
        "SOL": 150.0,
        "BNB": 600.0
    }
    return prices.get(asset, 0.0)