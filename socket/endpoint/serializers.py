from rest_framework import serializers
from .models import Coin

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['symbol_text', 'unix_timestamp', 'bid_price', 'ask_price', 'spot_price', 'price_change_24hr']
