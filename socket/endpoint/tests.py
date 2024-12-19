from django.test import TestCase
from decimal import Decimal
from .models import Coin
from get_crypto_dict import get_random_dict

class CoinModelTest(TestCase):
    def test_coin_creation(self):
        """Test creating a Coin instance"""
        coin = Coin.objects.create(
            symbol_text="BTC_CAD",
            unix_timestamp=1734563168,
            bid_price=Decimal("143727.53"),
            ask_price=Decimal("143724.67"),
            spot_price=Decimal("143724.67"),
            price_change_24hr=Decimal("-7833.51"),
        )
        self.assertEqual(Coin.objects.count(), 1)
        self.assertEqual(coin.symbol_text, "BTC_CAD")


class CryptoDictTest(TestCase):
    def test_get_random_dict(self):
        """Test random dictionary generation"""
        crypto_data = get_random_dict()
        self.assertIn("data", crypto_data)
        self.assertIn("symbol", crypto_data["data"])
        self.assertIn("timestamp", crypto_data["data"])
