from rest_framework import serializers
from pedidos.models import Pedidos, ItemPedido


class ItemPedidoSerializer(serializers.ModelSerializer):
    # Read-only field to calculate the total price of an item
    total_item = serializers.ReadOnlyField()

    # A field for the product name, sourced from the related product object
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    # A field for the product image, sourced from the related product object
    produto_imagem = serializers.SerializerMethodField()

    def create(self, validated_data):
        # Method to create a new ItemPedido instance
        return ItemPedido.objects.create(**validated_data)

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'produto_imagem', 'quantidade', 'preco_unitario', 'total_item']

    def get_produto_imagem(self, obj):
        # Method to retrieve the product image URL if it exists
        if obj.produto.produto_imagem:
            return obj.produto.produto_imagem.url 
        return None 


class PedidosSerializers(serializers.ModelSerializer):
    # Method to create a new Pedidos instance
    def create(self, validated_data):
        return Pedidos.objects.create(**validated_data)

    class Meta:
        model = Pedidos
        fields = ['id', 'cliente', 'email', 'data_pedido', 'entrega_status', 'total']