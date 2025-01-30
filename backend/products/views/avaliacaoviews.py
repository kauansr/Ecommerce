from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from products.models import Avaliacao, Produtos
from products.serializers import AvaliacaoSerializer


@api_view(['GET'])
@permission_classes([])  # No permission restrictions for this endpoint
def ver_avaliacoes(request):
    """
    Retrieves all reviews made by the authenticated user.
    
    Method: GET
    Permissions: None (but user must be authenticated)
    """
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    # Fetch reviews related to the authenticated user
    user_avaliacoes = Avaliacao.objects.filter(usuario=request.user.id)

    # Serialize the reviews and return them
    serializer = AvaliacaoSerializer(user_avaliacoes, many=True)
    return Response(serializer.data)


class AvaliacaoAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Permission: Requires authentication for modification

    def get(self, request, produto_id=None):
        """
        List reviews for a product or all reviews if no product ID is provided.
        
        Method: GET
        Permissions: Read-only access for all, authentication required for write operations.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if produto_id:
            # Retrieve reviews for a specific product
            produto = Produtos.objects.filter(id=produto_id).first()
            avaliacoes = Avaliacao.objects.filter(produto=produto)
            serializer = AvaliacaoSerializer(avaliacoes, many=True)
            return Response(serializer.data)
        else:
            # Retrieve all reviews
            avaliacoes = Avaliacao.objects.all()
            serializer = AvaliacaoSerializer(avaliacoes, many=True)
            return Response(serializer.data)

    def post(self, request, produto_id):
        """
        Create a new review for a product.
        
        Method: POST
        Permissions: Requires authentication.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        produto = Produtos.objects.get(id=produto_id)

        # Prepare the review data
        data = { 
            'produto': produto.id,
            'usuario': request.user.id,
            'estrelas': request.data.get('nota'),
            'comentario': request.data.get('comentario')
        }
        serializer = AvaliacaoSerializer(data=data)
        
        # Validate and save the new review
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, avaliacao_id):
        """
        Update an existing review.
        
        Method: PUT
        Permissions: Requires authentication and ownership of the review.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # Fetch the review to be updated
            avaliacao = Avaliacao.objects.get(id=avaliacao_id, usuario=request.user.id)
            data = {
                'produto': avaliacao.produto.id,
                'usuario': request.user.id,
                'estrelas': request.data.get('estrelas'),
                'comentario': request.data.get('comentario')
            }
        except Avaliacao.DoesNotExist:
            # Return error if the review is not found or doesn't belong to the user
            return Response({"detail": "Review not found or does not belong to this user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AvaliacaoSerializer(avaliacao, data=data)
        
        # Validate and save the updated review
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, avaliacao_id):
        """
        Delete an existing review.
        
        Method: DELETE
        Permissions: Requires authentication and ownership of the review.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # Try to find the review to be deleted
            avaliacao = Avaliacao.objects.get(id=avaliacao_id, usuario=request.user.id)
        except Avaliacao.DoesNotExist:
            # Return error if the review is not found or doesn't belong to the user
            return Response({"detail": "Review not found or does not belong to this user."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the review
        avaliacao.delete()
        return Response({"detail": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)