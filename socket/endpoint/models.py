from django.db import models

class Coin(models.Model):
    symbol_text = models.CharField(max_length=10, unique=True)
    unix_timestamp = models.IntegerField(default=0)
    bid_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    ask_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    spot_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    price_change_24hr = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.symbol_text