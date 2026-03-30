def calculate_spread(price_buy: float, price_sell: float) -> tuple[float, float]:
    if price_buy <= 0:
        raise ValueError("price_buy must be greater than zero")

    spread_absolute = price_sell - price_buy
    spread_percent = (spread_absolute / price_buy) * 100
    return spread_absolute, spread_percent
