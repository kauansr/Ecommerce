from django.urls import path
from products.views import ProdutosAPI, ProdutoAPI, ver_produto, ver_produtos

urlpatterns = [
    path('produtosadm/', ProdutosAPI.as_view(), name='produtosadmall'),
    path('produtosadm/<int:pk>/', ProdutoAPI.as_view(), name='produtoadmone'),
    path('produtos/', ver_produtos, name='produtosall'),
    path('produtos/<int:pk>', ver_produto, name='produtoone'),
]
