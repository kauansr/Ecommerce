from django.contrib import admin
from .models import Pedidos

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_pedido', 'preco', 'email', 'user_id', 'entrega_status']
    list_display_links = ['id', 'nome_pedido']
    ordering = ['id']
    list_editable = ['email', 'entrega_status']
    list_max_show_all = 100
    list_per_page = 10
