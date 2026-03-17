from quotes.schema import Quote
from quotes.utils import now_ms

from .schema import Spread
from .utils import calculate_spread, ensure_quotes_compatible, normalize_exchange


def create_spread(
    *,
    quote_buy: Quote,
    quote_sell: Quote,
    exchange_buy: str,
    exchange_sell: str,
    ts_calculated: int | None = None,
) -> Spread:
    ensure_quotes_compatible(quote_buy, quote_sell)

    normalized_exchange_buy = normalize_exchange(exchange_buy, "exchange_buy")
    normalized_exchange_sell = normalize_exchange(exchange_sell, "exchange_sell")
    spread_absolute, spread_percent = calculate_spread(quote_buy.ask, quote_sell.bid)

    return Spread(
        asset_id=quote_buy.asset_id,
        name=quote_buy.name,
        address=quote_buy.address,
        network=quote_buy.network,
        exchange_buy=normalized_exchange_buy,
        exchange_sell=normalized_exchange_sell,
        price_buy=quote_buy.ask,
        price_sell=quote_sell.bid,
        spread_absolute=spread_absolute,
        spread_percent=spread_percent,
        ts_exchange_buy=quote_buy.ts_exchange,
        ts_exchange_sell=quote_sell.ts_exchange,
        ts_written_buy=quote_buy.ts_written,
        ts_written_sell=quote_sell.ts_written,
        ts_calculated=ts_calculated if ts_calculated is not None else now_ms(),
    )
