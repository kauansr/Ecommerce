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
        
        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)

        
        ped = Pedidos.objects.filter(cliente=request.user.pk)
        
        
        serializer = PedidosSerializers(ped, many=True)
        return Response(serializer.data)

    def post(self, request):
       
        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)

        
        itens_data = request.data.get('itens', [])

        
        if not itens_data:
            return Response({'msg': 'É necessário fornecer itens para o pedido!'}, status=status.HTTP_400_BAD_REQUEST)

        
        pedido_data = {
            'cliente': request.user.id,
            'email': request.user.email,
        }

        
        serializer = PedidosSerializers(data=pedido_data)
        
        if serializer.is_valid(raise_exception=True):
            pedido = serializer.save()

            total = Decimal("0.00")
            
            for item_data in itens_data:
                try:
                    
                    produto = Produtos.objects.get(id=item_data['produto'])
                except Produtos.DoesNotExist:
                    return Response({'msg': f"Produto com id {item_data['produto']} não encontrado."}, status=status.HTTP_404_NOT_FOUND)

                
                if produto.quantidade < item_data['quantidade']:
                    return Response({'msg': 'Quantidade insuficiente para o produto!'}, status=status.HTTP_400_BAD_REQUEST)

                
                produto.quantidade -= item_data['quantidade']
                produto.save()

                
                items_pedido = ItemPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=item_data['quantidade'],
                    preco_unitario=produto.preco,
                )

                total += items_pedido.total_item
                
            try:
                pedido.total = total
                pedido.save()
            except Exception as e:
                print(f"Erro ao salvar o pedido: {e}")
                return Response({'msg': 'Erro ao salvar o pedido!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Pedidos.objects.get(pk=pk)
        except Pedidos.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
       
        pedido = self.get_object(pk=pk)

        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PedidosSerializers(pedido)

        itens = ItemPedido.objects.filter(pedido=pedido)

        
        item_serializer = ItemPedidoSerializer(itens, many=True)

        
        return Response({
            'pedido': serializer.data,
            'itens': item_serializer.data 
        })

    def delete(self, request, pk):
        pedido = self.get_object(pk=pk)

        
        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)

        
        for item in pedido.itens.all():
            produto = item.produto
            produto.quantidade += item.quantidade
            produto.save()

        pedido.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)