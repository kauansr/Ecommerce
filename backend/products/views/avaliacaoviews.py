from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from products.models import Avaliacao, Produtos
from products.serializers import AvaliacaoSerializer


@api_view(['GET'])
@permission_classes([])
def ver_avaliacoes(request):


    if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)

    user_avaliacoes = Avaliacao.objects.filter(usuario=request.user.id)

    serializer = AvaliacaoSerializer(user_avaliacoes, many=True)

    return Response(serializer.data)

class AvaliacaoAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, produto_id=None):
        """Lista as avaliações de um produto"""

        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)
        

        if produto_id:
            produto = Produtos.objects.filter(id=produto_id).first()
            avaliacoes = Avaliacao.objects.filter(produto=produto)
            serializer = AvaliacaoSerializer(avaliacoes, many=True)
            return Response(serializer.data)
        else:
            avaliacoes = Avaliacao.objects.all()
            serializer = AvaliacaoSerializer(avaliacoes, many=True)
            return Response(serializer.data)

    def post(self, request, produto_id):
        """Cria uma nova avaliação para um produto"""

        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        produto = Produtos.objects.get(id=produto_id)

        data = {
            'usuario_nome': request.user.username,
            'produto': produto.id, 
            'usuario': request.user.id,
            'estrelas': request.data.get('nota'),
            'comentario': request.data.get('comentario')
        }
        serializer = AvaliacaoSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, avaliacao_id):
        """Atualiza uma avaliação existente"""

        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)
        
        

        try:
            avaliacao = Avaliacao.objects.get(id=avaliacao_id, usuario=request.user.id)
            data = {
                'produto': avaliacao.produto.id, 
                'usuario': request.user.id,
                'estrelas': request.data.get('estrelas'),
                'comentario': request.data.get('comentario')
            }

            
        except Avaliacao.DoesNotExist:
            return Response({"detail": "Avaliação não encontrada ou não pertence a este usuário."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AvaliacaoSerializer(avaliacao, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, avaliacao_id):
        """Deleta uma avaliação existente"""

        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        try:
            avaliacao = Avaliacao.objects.get(id=avaliacao_id, usuario=request.user.id)
        except Avaliacao.DoesNotExist:
            return Response({"detail": "Avaliação não encontrada ou não pertence a este usuário."}, status=status.HTTP_404_NOT_FOUND)

        avaliacao.delete()
        return Response({"detail": "Avaliação deletada com sucesso."}, status=status.HTTP_204_NO_CONTENT)