from django.urls import path
from .views import CoinListView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('api/coins/', CoinListView.as_view(), name='coin_list'),
]