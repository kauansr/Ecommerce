from django.contrib import admin
from products.models import Produtos

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ['id','nome', 'categoria', 'preco']
    list_display_links = ['id','nome']
    ordering = ['id']
    list_editable = ['categoria', 'preco']
    list_max_show_all = 100
    list_per_page = 10
    