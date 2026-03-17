import json
from dataclasses import asdict, dataclass
from math import isfinite

from .utils import normalize_exchange


@dataclass(frozen=True, slots=True)
class Spread:
    asset_id: str
    name: str
    address: str
    network: str
    exchange_buy: str
    exchange_sell: str
    price_buy: float
    price_sell: float
    spread_absolute: float
    spread_percent: float
    ts_exchange_buy: int | float | None
    ts_exchange_sell: int | float | None
    ts_written_buy: int | float | None
    ts_written_sell: int | float | None
    ts_calculated: int

    def __post_init__(self) -> None:
        normalize_exchange(self.exchange_buy, "exchange_buy")
        normalize_exchange(self.exchange_sell, "exchange_sell")
        if not isfinite(self.price_buy) or self.price_buy <= 0:
            raise ValueError("price_buy must be a finite number greater than zero")
        if not isfinite(self.price_sell) or self.price_sell < 0:
            raise ValueError("price_sell must be a finite non-negative number")
        if not isfinite(self.spread_absolute):
            raise ValueError("spread_absolute must be finite")
        if not isfinite(self.spread_percent):
            raise ValueError("spread_percent must be finite")
        if self.ts_calculated < 0:
            raise ValueError("ts_calculated must be non-negative")

    def to_dict(self) -> dict[str, str | float | int | None]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"))

    def to_event(self, action: str = "upsert") -> dict[str, str | int | float | None]:
        return {
            "action": action,
            "asset_id": self.asset_id,
            "name": self.name,
            "address": self.address,
            "network": self.network,
            "exchange_buy": self.exchange_buy,
            "exchange_sell": self.exchange_sell,
            "spread_absolute": self.spread_absolute,
            "spread_percent": self.spread_percent,
            "ts_calculated": self.ts_calculated,
        }
