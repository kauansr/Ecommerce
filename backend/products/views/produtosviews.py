from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from products.models import Produtos
from products.serializers import ProdutosSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from products.filters import ProdutoFilter

class ProdutosAPI(APIView):
    """
    API view for managing multiple products (GET and POST).
    Only accessible by admin users.
    """
    
    permission_classes = (IsAdminUser,)  # Only admin users can access this view

    def get(self, request):
        """
        Handles GET request to retrieve all products.
        Returns a list of serialized products.
        """
        produtos = Produtos.objects.all()  # Retrieves all products from the database
        serializer = ProdutosSerializer(produtos, many=True)  # Serializes the products
        return Response(serializer.data)  # Returns the serialized data in the response
    
    def post(self, request):
        """
        Handles POST request to create a new product.
        Validates the data, saves it, and returns the created product.
        """
        serializer = ProdutosSerializer(data=request.data)  # Serializes the input data
        if serializer.is_valid(raise_exception=True):  # Checks if the data is valid
            serializer.save()  # Saves the new product
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Returns the serialized product data and 201 status
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Returns validation errors if the data is not valid


class ProdutoAPI(APIView):
    """
    API view for managing a single product (GET, PUT, DELETE).
    Only accessible by admin users.
    """
    
    permission_classes = (IsAdminUser,)  # Only admin users can access this view

    def get_object(self, pk):
        """
        Retrieves a product by its primary key (pk).
        Raises Http404 if the product does not exist.
        """
        try:
            return Produtos.objects.get(pk=pk)  # Retrieves the product by pk
        except Produtos.DoesNotExist:
            raise Http404  # Raises an HTTP 404 error if the product does not exist

    def get(self, request, pk):
        """
        Handles GET request to retrieve a single product by pk.
        Returns the serialized product data.
        """
        produto = self.get_object(pk=pk)  # Retrieves the product
        serializer = ProdutosSerializer(produto)  # Serializes the product
        return Response(serializer.data)  # Returns the serialized product data in the response
    
    def put(self, request, pk):
        """
        Handles PUT request to update a product by pk.
        Validates the updated data and saves the changes.
        """
        produto = self.get_object(pk=pk)  # Retrieves the product to update
        serializer = ProdutosSerializer(produto, data=request.data)  # Serializes the updated data
        
        if serializer.is_valid(raise_exception=True):  # Validates the updated data
            serializer.save()  # Saves the updated product
            return Response(serializer.data)  # Returns the updated product data
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Returns validation errors if the data is not valid
    
    def delete(self, request, pk):
        """
        Handles DELETE request to remove a product by pk.
        Deletes the product and returns a 204 No Content status.
        """
        produto = self.get_object(pk=pk)  # Retrieves the product to delete
        produto.delete()  # Deletes the product
        return Response(status=status.HTTP_204_NO_CONTENT)  # Returns 204 No Content as the response


def get_object(pk):
    """
    Helper function to retrieve a product by its primary key (pk).
    Raises Http404 if the product does not exist.
    """
    try:
        return Produtos.objects.get(pk=pk)  # Retrieves the product by pk
    except Produtos.DoesNotExist:
        raise Http404  # Raises an HTTP 404 error if the product does not exist
        

@api_view(['GET'])
@permission_classes([])  # No authentication required for this view
def ver_produtos(request):
    """
    API view to list products publicly (no authentication required).
    Supports filtering via query parameters.
    """
    produto_filter = ProdutoFilter(request.GET, queryset=Produtos.objects.all())  # Applies filters from query parameters
    produtos = produto_filter.qs  # Retrieves filtered products
    serializer = ProdutosSerializer(produtos, many=True)  # Serializes the products
    return Response(serializer.data)  # Returns the serialized products in the response


@api_view(['GET'])
@permission_classes([])  # No authentication required for this view
def ver_produto(request, pk):
    """
    API view to retrieve a single product publicly by its pk.
    No authentication is required.
    """
    produto = get_object(pk=pk)  # Retrieves the product by pk
    serializer = ProdutosSerializer(produto)  # Serializes the product
    return Response(serializer.data)  # Returns the serialized product in the response