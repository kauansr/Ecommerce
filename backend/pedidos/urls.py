from django.urls import path
from .views import PedidoAPI, PedidosAPI

urlpatterns = [
    path('pedidos/', PedidosAPI.as_view(), name='pedidosapi'),
    path('pedidos/<int:pk>', PedidoAPI.as_view(), name='pedidoapi'),
    
]
