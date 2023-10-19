from rest_framework import serializers
from products.models import Produtos

class ProdutosSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Produtos.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.nome = validated_data.get('nome', instance.nome)
        instance.preco = validated_data.get('preco', instance.preco)
        instance.descricao = validated_data.get('descricao', instance.descricao)
        instance.categoria = validated_data.get('categoria', instance.categoria)
        instance.produto_imagem = validated_data.get('produto_imagem', instance.produto_imagem)
        instance.save()

        return instance

    class Meta:
        model = Produtos
        fields = '__all__'