from django.urls import path
from .views import PedidoAdmAPI, PedidosAdmAPI, PedidoAPI, PedidosAPI

urlpatterns = [
    path('pedidosadm/', PedidosAdmAPI.as_view(), name='pedidosadmapi'),
    path('pedidosadm/<int:pk>', PedidoAdmAPI.as_view(), name='pedidoadmapi'),
    path('pedidos/', PedidosAPI.as_view(), name='pedidosapi'),
    path('pedidos/<int:pk>', PedidoAPI.as_view(), name='pedidoapi'),
    
]
