import unittest

from quotes import create_quote
from spreads import Spread, create_spread


class TestSpreads(unittest.TestCase):
    def test_spread_create_and_event(self) -> None:
        quote_buy = create_quote(
            asset_id="BTC",
            name="Bitcoin",
            address="native",
            network="bitcoin",
            bid=100.0,
            ask=101.0,
            last=100.5,
            ts_exchange=10,
            ts_written=11,
        )
        quote_sell = create_quote(
            asset_id="BTC",
            name="Bitcoin",
            address="native",
            network="bitcoin",
            bid=105.0,
            ask=106.0,
            last=105.5,
            ts_exchange=20,
            ts_written=21,
        )

        spread = create_spread(
            quote_buy=quote_buy,
            quote_sell=quote_sell,
            exchange_buy="a",
            exchange_sell="b",
        )
        event = spread.to_event()

        self.assertAlmostEqual(spread.spread_absolute, 4.0)
        self.assertAlmostEqual(spread.spread_percent, (4.0 / 101.0) * 100)
        self.assertEqual(event["asset_id"], "BTC")
        self.assertEqual(event["exchange_buy"], "a")
        self.assertEqual(event["exchange_sell"], "b")

    def test_spread_create_raises_on_empty_exchange(self) -> None:
        quote_buy = create_quote(
            asset_id="BTC",
            name="Bitcoin",
            address="native",
            network="bitcoin",
            bid=100.0,
            ask=101.0,
            last=100.5,
            ts_exchange=10,
            ts_written=11,
        )
        quote_sell = create_quote(
            asset_id="BTC",
            name="Bitcoin",
            address="native",
            network="bitcoin",
            bid=106.0,
            ask=106.0,
            last=105.5,
            ts_exchange=20,
            ts_written=21,
        )

        with self.assertRaises(ValueError):
            create_spread(
                quote_buy=quote_buy,
                quote_sell=quote_sell,
                exchange_buy=" ",
                exchange_sell="b",
            )

    def test_spread_create_raises_when_quotes_not_compatible(self) -> None:
        quote_buy = create_quote(
            asset_id="BTC",
            name="Bitcoin",
            address="native",
            network="bitcoin",
            bid=100.0,
            ask=101.0,
            last=100.5,
            ts_exchange=10,
            ts_written=11,
        )
        quote_sell = create_quote(
            asset_id="ETH",
            name="Ether",
            address="native",
            network="ethereum",
            bid=106.0,
            ask=106.5,
            last=105.5,
            ts_exchange=20,
            ts_written=21,
        )

        with self.assertRaises(ValueError):
            create_spread(
                quote_buy=quote_buy,
                quote_sell=quote_sell,
                exchange_buy="a",
                exchange_sell="b",
            )


if __name__ == "__main__":
    unittest.main()
