from django.http import JsonResponse
from .models import Coin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CoinSerializer

def index(request):
    coins = Coin.objects.values()
    return JsonResponse(list(coins), safe=False)

class CoinListView(APIView):
    def get(self, request):
        coins = Coin.objects.all()
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)
    