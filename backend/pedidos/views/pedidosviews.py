from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from pedidos.models import Pedidos, ItemPedido
from pedidos.serializers import PedidosSerializers, ItemPedidoSerializer
from products.models import Produtos
from decimal import Decimal

class PedidosAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves a list of orders for the authenticated user.

        - Permissions: The user must be authenticated.
        - Response:
            - 200 OK: Returns a list of orders with their details.
            - 401 Unauthorized: If the user is not authenticated.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        orders = Pedidos.objects.filter(cliente=request.user.pk)

        serializer = PedidosSerializers(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a new order for the authenticated user.

        - Permissions: The user must be authenticated.
        - Request Data:
            - `itens`: A list of items in the order, with each item having the following fields:
                - `produto`: The ID of the product.
                - `quantidade`: The quantity of the product.
        - Response:
            - 201 Created: Returns the order details.
            - 400 Bad Request: If no items are provided, or if there is insufficient stock.
            - 404 Not Found: If a product is not found.
            - 500 Internal Server Error: If there is an error while saving the order.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        items_data = request.data.get('itens', [])

        if not items_data:
            return Response({'msg': 'You must provide items for the order!'}, status=status.HTTP_400_BAD_REQUEST)

        order_data = {
            'cliente': request.user.id,
            'email': request.user.email,
        }

        serializer = PedidosSerializers(data=order_data)
        
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()

            total = Decimal("0.00")
            
            for item_data in items_data:
                try:
                    product = Produtos.objects.get(id=item_data['produto'])
                except Produtos.DoesNotExist:
                    return Response({'msg': f"Product with id {item_data['produto']} not found."}, status=status.HTTP_404_NOT_FOUND)

                if product.quantidade < item_data['quantidade']:
                    return Response({'msg': 'Insufficient stock for the product!'}, status=status.HTTP_400_BAD_REQUEST)

                product.quantidade -= item_data['quantidade']
                product.save()

                order_item = ItemPedido.objects.create(
                    pedido=order,
                    produto=product,
                    quantidade=item_data['quantidade'],
                    preco_unitario=product.preco,
                )

                total += order_item.total_item

            try:
                order.total = total
                order.save()
            except Exception as e:
                print(f"Error while saving the order: {e}")
                return Response({'msg': 'Error while saving the order!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get a specific order by its primary key (id).
        """
        try:
            return Pedidos.objects.get(pk=pk)
        except Pedidos.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        """
        Retrieves the details of a specific order.

        - Permissions: The user must be authenticated.
        - Response:
            - 200 OK: Returns the order details and its associated items.
            - 401 Unauthorized: If the user is not authenticated.
        """
        order = self.get_object(pk=pk)

        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PedidosSerializers(order)
        items = ItemPedido.objects.filter(pedido=order)

        item_serializer = ItemPedidoSerializer(items, many=True)

        return Response({
            'pedido': serializer.data,
            'itens': item_serializer.data
        })

    def delete(self, request, pk):
        """
        Deletes a specific order and restores stock quantities for the ordered items.

        - Permissions: The user must be authenticated.
        - Response:
            - 204 No Content: If the order is successfully deleted.
            - 401 Unauthorized: If the user is not authenticated.
        """
        order = self.get_object(pk=pk)

        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Restore the stock quantity for each item in the order
        for item in order.itens.all():
            product = item.produto
            product.quantidade += item.quantidade
            product.save()

        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)