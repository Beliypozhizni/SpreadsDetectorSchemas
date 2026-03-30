from quotes.schema import Quote
from quotes.utils import now_ms

from .schema import Spread
from .utils import calculate_spread


def create_spread(
    *,
    quote_buy: Quote,
    quote_sell: Quote,
    exchange_buy: str,
    exchange_sell: str,
    ts_found: int | None = None,
    ts_calculated: int | None = None,
) -> Spread:
    if quote_buy.asset_id != quote_sell.asset_id:
        raise ValueError("quote_buy.asset_id must match quote_sell.asset_id")
    if quote_buy.address != quote_sell.address:
        raise ValueError("quote_buy.address must match quote_sell.address")
    if quote_buy.network != quote_sell.network:
        raise ValueError("quote_buy.network must match quote_sell.network")

    normalized_exchange_buy = exchange_buy.strip().lower()
    normalized_exchange_sell = exchange_sell.strip().lower()
    if not normalized_exchange_buy:
        raise ValueError("exchange_buy must be a non-empty string")
    if not normalized_exchange_sell:
        raise ValueError("exchange_sell must be a non-empty string")

    spread_absolute, spread_percent = calculate_spread(quote_buy.ask, quote_sell.bid)
    resolved_ts_calculated = ts_calculated if ts_calculated is not None else now_ms()
    resolved_ts_found = ts_found if ts_found is not None else resolved_ts_calculated

    return Spread(
        asset_id=quote_buy.asset_id,
        address=quote_buy.address,
        network=quote_buy.network,
        exchange_buy=normalized_exchange_buy,
        exchange_sell=normalized_exchange_sell,
        name_buy=quote_buy.name,
        name_sell=quote_sell.name,
        price_buy=quote_buy.ask,
        price_sell=quote_sell.bid,
        spread_absolute=spread_absolute,
        spread_percent=spread_percent,
        ts_found=resolved_ts_found,
        ts_calculated=resolved_ts_calculated,
    )
