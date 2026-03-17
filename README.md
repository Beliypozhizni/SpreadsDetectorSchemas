# Spreads Detector Schemas

Shared schemas for microservices that work with market quotes and spread calculation.

## Contents

- `quotes`: market quote schema (`Quote`) plus factories and parsing helpers.
- `spreads`: spread schema (`Spread`) and spread factory based on shared `Quote`.

## Installation

```bash
pip install .
```

or editable mode for development:

```bash
pip install -e .
```

Python requirement: `>=3.13`.

## Usage

```python
from quotes import create_quote, quote_from_redis
from spreads import create_spread

quote_buy = create_quote(
    asset_id="BTC",
    name="Bitcoin",
    address="native",
    network="bitcoin",
    bid=60000.0,
    ask=60100.0,
    last=60050.0,
    ts_exchange=1710000000000,
)

quote_sell = quote_from_redis(
    "BTC",
    '{"name":"Bitcoin","address":"native","network":"bitcoin","bid":60500.0,"ask":60600.0,"last":60550.0,"ts_exchange":1710000000100}',
)

spread = create_spread(
    quote_buy=quote_buy,
    quote_sell=quote_sell,
    exchange_buy="exchange_a",
    exchange_sell="exchange_b",
)
print(spread.to_json())
```

## Development

Run tests:

```bash
python -m unittest discover -s tests -v
```
