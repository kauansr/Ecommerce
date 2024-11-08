from rest_framework import serializers
from pedidos.models import Pedidos, ItemPedido
from accounts.models import User



class ItemPedidoSerializer(serializers.ModelSerializer):
    total_item = serializers.ReadOnlyField()
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_imagem = serializers.SerializerMethodField() 

    def create(self, validated_data):
        return ItemPedido.objects.create(**validated_data)


    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'produto_imagem', 'quantidade', 'preco_unitario', 'total_item']


    def get_produto_imagem(self, obj):
        
        if obj.produto.produto_imagem:
            return obj.produto.produto_imagem.url 
        return None 

class PedidosSerializers(serializers.ModelSerializer):


    def create(self, validated_data):
        return Pedidos.objects.create(**validated_data)


    class Meta:
        model = Pedidos
        fields = ['id', 'cliente', 'email', 'data_pedido', 'entrega_status', 'total']
    
