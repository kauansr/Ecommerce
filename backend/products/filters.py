import django_filters
from .models import Produtos

class ProdutoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome do Produto')
    categoria = django_filters.ChoiceFilter(choices=Produtos._meta.get_field('categoria').choices, label='Categoria')
    preco_min = django_filters.NumberFilter(field_name='preco', lookup_expr='gte', label='Preço Mínimo')
    preco_max = django_filters.NumberFilter(field_name='preco', lookup_expr='lte', label='Preço Máximo')

    class Meta:
        model = Produtos
        fields = ['nome', 'categoria', 'preco_min', 'preco_max']