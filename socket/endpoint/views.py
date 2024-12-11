from django.http import JsonResponse
from .models import Coin

def index(request):
    coins = Coin.objects.values()
    return JsonResponse(list(coins), safe=False)
