from rest_framework import serializers
from products.models import Produtos, Avaliacao

class ProdutosSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Produtos.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.nome = validated_data.get('nome', instance.nome)
        instance.preco = validated_data.get('preco', instance.preco)
        instance.descricao = validated_data.get('descricao', instance.descricao)
        instance.quantidade = validated_data.get('quantidade', instance.quantidade)
        instance.categoria = validated_data.get('categoria', instance.categoria)
        instance.produto_imagem = validated_data.get('produto_imagem', instance.produto_imagem)
        instance.save()

        return instance

    class Meta:
        model = Produtos
        fields = '__all__'
    
    def validate_preco(self, value):
        
        value = str(value).replace(',', '.')

        try:
        
            value = round(float(value), 2)
        except ValueError:
            raise serializers.ValidationError('Formato de preço inválido.')

        return value




class AvaliacaoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username')

    class Meta:
        model = Avaliacao
        fields = ['id', 'usuario_nome','produto', 'usuario', 'estrelas', 'comentario', 'data_avaliacao']
    

    def create(self, validated_data):
        return Avaliacao.objects.create(**validated_data)
    
    def update(self, instance, validated_data):

        instance.estrelas = validated_data.get('estrelas', instance.estrelas)
        instance.comentario = validated_data.get('comentario', instance.comentario)
        instance.save()

        return instance

