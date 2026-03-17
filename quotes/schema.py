from dataclasses import asdict, dataclass
from decimal import Decimal
from math import isfinite

from .utils import compact_json, require_non_empty


@dataclass(slots=True, frozen=True)
class Quote:
    asset_id: str
    name: str
    address: str
    network: str
    bid: float
    ask: float
    last: float
    ts_exchange: int
    ts_written: int

    def __post_init__(self) -> None:
        require_non_empty(self.asset_id, "asset_id")
        require_non_empty(self.name, "name")
        require_non_empty(self.address, "address")
        require_non_empty(self.network, "network")
        if not isfinite(self.bid):
            raise ValueError("bid must be a finite number")
        if not isfinite(self.ask):
            raise ValueError("ask must be a finite number")
        if not isfinite(self.last):
            raise ValueError("last must be a finite number")
        if self.ask <= 0:
            raise ValueError("ask must be greater than zero")
        if self.bid < 0:
            raise ValueError("bid must be non-negative")
        if self.ts_exchange < 0:
            raise ValueError("ts_exchange must be non-negative")
        if self.ts_written < 0:
            raise ValueError("ts_written must be non-negative")

    def to_dict(self) -> dict[str, str | float | int]:
        return asdict(self)

    def to_json(self) -> str:
        return compact_json(self.to_dict())

    def to_event(self, exchange: str) -> dict[str, str | int]:
        normalized_exchange = require_non_empty(exchange, "exchange").lower()
        return {
            "type": "quote_upserted",
            "exchange": normalized_exchange,
            "asset_id": self.asset_id,
            "quote": self.to_json(),
            "ts_exchange": self.ts_exchange,
            "ts_written": self.ts_written,
        }

    @property
    def bid_decimal(self) -> Decimal:
        return Decimal(str(self.bid))

    @property
    def ask_decimal(self) -> Decimal:
        return Decimal(str(self.ask))
