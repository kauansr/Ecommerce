from django.urls import path
from products.views import ProdutosAPI, ProdutoAPI, ver_produto, ver_produtos, AvaliacaoAPIView, ver_avaliacoes

urlpatterns = [
    path('produtosadm/', ProdutosAPI.as_view(), name='produtosadmall'),
    path('produtosadm/<int:pk>/', ProdutoAPI.as_view(), name='produtoadmone'),
    path('produtos/', ver_produtos, name='produtosall'),
    path('produtos/<int:pk>', ver_produto, name='produtoone'),


    path('avaliacoes/', ver_avaliacoes, name='minhas_avaliacoes'),
    path('avaliacoes/<int:produto_id>/', AvaliacaoAPIView.as_view(), name='avaliacoes-list-create'),
    path('avaliacoes/<int:avaliacao_id>/update', AvaliacaoAPIView.as_view(), name='avaliacoes-update'),
    path('avaliacoes/<int:avaliacao_id>/delete', AvaliacaoAPIView.as_view(), name='avaliacoes-delete'),
]
