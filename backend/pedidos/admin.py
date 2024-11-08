from django.contrib import admin
from .models import Pedidos, ItemPedido

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'data_pedido', 'entrega_status', 'total']
    list_display_links = ['id', 'cliente']
    ordering = ['id']
    list_editable = ['entrega_status']
    list_max_show_all = 100
    list_per_page = 10


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'produto', 'quantidade', 'preco_unitario']
    list_display_links = ['id', 'pedido', 'produto']
    ordering = ['id']
    list_editable = ['quantidade']
    list_max_show_all = 100
    list_per_page = 10