from django.http import JsonResponse
from .models import Coin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CoinSerializer
import logging

logger = logging.getLogger(__name__)

def index(request):
    coins = Coin.objects.values()
    return JsonResponse(list(coins), safe=False)

class CoinListView(APIView):
    def get(self, request):
        logger.info("CoinListView called")  # Logging
        coins = Coin.objects.all()
        logger.info(f"Coins retrieved: {coins}")  # Logging
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)
    