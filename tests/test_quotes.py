import json
import unittest

from quotes import Quote, create_quote, quote_from_redis


class TestQuotes(unittest.TestCase):
    def test_create_quote_sets_timestamp(self) -> None:
        quote = create_quote(
            asset_id="BTC",
            name="Bitcoin",
            address="native",
            network="bitcoin",
            bid=100.0,
            ask=101.0,
            last=100.5,
            withdraw_status=True,
            deposit_status=True,
            ts_exchange=123,
        )
        self.assertGreater(quote.ts_written, 0)
        self.assertEqual(quote.ts_exchange, 123)
        self.assertTrue(quote.withdraw_status)
        self.assertTrue(quote.deposit_status)

    def test_to_json_and_to_event(self) -> None:
        quote = create_quote(
            asset_id="ETH",
            name="Ether",
            address="native",
            network="ethereum",
            bid=200.0,
            ask=201.0,
            last=200.5,
            withdraw_status=False,
            deposit_status=True,
            ts_exchange=456,
            ts_written=789,
        )
        payload = json.loads(quote.to_json())
        event = quote.to_event("ByBit")

        self.assertEqual(payload["asset_id"], "ETH")
        self.assertEqual(payload["ts_written"], 789)
        self.assertEqual(payload["withdraw_status"], False)
        self.assertEqual(payload["deposit_status"], True)
        self.assertEqual(event["exchange"], "bybit")
        self.assertEqual(event["asset_id"], "ETH")

    def test_quote_from_redis(self) -> None:
        payload = json.dumps(
            {
                "name": "Solana",
                "address": "native",
                "network": "solana",
                "bid": 1.23,
                "ask": 1.24,
                "last": 1.235,
                "withdraw_status": True,
                "deposit_status": False,
                "ts_exchange": 1,
                "ts_written": 2,
            }
        )
        quote = quote_from_redis("SOL", payload)

        self.assertIsInstance(quote, Quote)
        self.assertEqual(quote.asset_id, "SOL")
        self.assertEqual(quote.bid, 1.23)
        self.assertEqual(quote.ask, 1.24)
        self.assertEqual(quote.last, 1.235)
        self.assertTrue(quote.withdraw_status)
        self.assertFalse(quote.deposit_status)

    def test_decimal_properties(self) -> None:
        quote = create_quote(
            asset_id="SOL",
            name="Solana",
            address="native",
            network="solana",
            bid=1.23,
            ask=1.24,
            last=1.235,
            withdraw_status=True,
            deposit_status=True,
            ts_exchange=1,
            ts_written=2,
        )
        self.assertEqual(str(quote.bid_decimal), "1.23")
        self.assertEqual(str(quote.ask_decimal), "1.24")


if __name__ == "__main__":
    unittest.main()
