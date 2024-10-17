from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from products.models import Produtos
from products.serializers import ProdutosSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class ProdutosAPI(APIView):

    permission_classes = (IsAdminUser,)

    def get(self, request):

        produtos = Produtos.objects.all()
        serializer = ProdutosSerializer(produtos, many=True)

        return Response(serializer.data)
    
    def post(self, request):

        serializer = ProdutosSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProdutoAPI(APIView):
    
    permission_classes = (IsAdminUser,)

    def get_object(self, pk):
        try:
            return Produtos.objects.get(pk=pk)
        
        except Produtos.DoesNotExist:
            raise Http404

    def get(self, request, pk):

        produto = self.get_object(pk=pk)
        serialiler = ProdutosSerializer(produto)

        return Response(serialiler.data)
    
    def put(self, request, pk):
        produto = self.get_object(pk=pk)
        serializer = ProdutosSerializer(produto, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):

        produto = self.get_object(pk=pk)
        produto.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


def get_object(pk):
    try:
        return Produtos.objects.get(pk=pk)
    
    except Produtos.DoesNotExist:
        raise Http404
    

@api_view(['GET'])
@permission_classes([])
def ver_produtos(request):
    produtos = Produtos.objects.all()
    serializer = ProdutosSerializer(produtos, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([])
def ver_produto(request, pk):

    produto = get_object(pk=pk)
    serialiler = ProdutosSerializer(produto)

    return Response(serialiler.data)