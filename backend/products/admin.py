from django.contrib import admin
from products.models import Produtos, Avaliacao

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ['id','nome', 'quantidade', 'categoria', 'preco']
    list_display_links = ['id','nome']
    ordering = ['id']
    list_editable = ['quantidade', 'categoria', 'preco']
    list_max_show_all = 100
    list_per_page = 10


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'usuario', 'estrelas', 'comentario', 'data_avaliacao')
    list_filter = ('produto', 'estrelas') 
    search_fields = ('usuario__username', 'comentario') 
    list_editable = ('estrelas', 'comentario')  
    ordering = ('estrelas',)
