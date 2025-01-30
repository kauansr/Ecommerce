from rest_framework import serializers
from products.models import Produtos, Avaliacao

class ProdutosSerializer(serializers.ModelSerializer):
    """
    Serializer for the Produtos (Product) model.
    
    Fields:
    - id: The unique identifier of the product (auto-generated).
    - nome: The name of the product.
    - descricao: A description of the product.
    - categoria: The category of the product.
    - quantidade: The available quantity of the product.
    - preco: The price of the product (validated and formatted).
    - produto_imagem: The image associated with the product.
    
    Methods:
    - create: Creates a new product instance with validated data.
    - update: Updates an existing product instance with validated data.
    - validate_preco: Ensures that the price is valid and formatted correctly (as a float with two decimal places).
    """
    
    def create(self, validated_data):
        """
        Creates a new product instance using the validated data.

        Args:
        - validated_data: A dictionary containing the product attributes.

        Returns:
        - The created Produtos instance.
        """
        return Produtos.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing product instance with new data.

        Args:
        - instance: The existing Produtos instance to update.
        - validated_data: A dictionary containing the product's new attributes.

        Returns:
        - The updated Produtos instance.
        """
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
        """
        Validates the price field to ensure it is a valid number and is formatted correctly.

        Args:
        - value: The price value to validate.

        Returns:
        - The formatted price value as a float with two decimal places.

        Raises:
        - ValidationError: If the price is invalid or improperly formatted.
        """
        # Replace any commas with periods and try to convert to float
        value = str(value).replace(',', '.')

        try:
            value = round(float(value), 2)
        except ValueError:
            raise serializers.ValidationError('Invalid price format.')

        return value


class AvaliacaoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Avaliacao (Review) model.
    
    Fields:
    - id: The unique identifier for the review (auto-generated).
    - usuario_nome: The username of the user who created the review (read-only).
    - produto: The associated product for the review.
    - usuario: The user who created the review.
    - estrelas: The rating for the product (in stars).
    - comentario: The review comment text.
    - data_avaliacao: The timestamp when the review was created.
    
    Methods:
    - create: Creates a new review instance with validated data.
    - update: Updates an existing review instance with validated data.
    """
    
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Avaliacao
        fields = ['id', 'usuario_nome', 'produto', 'usuario', 'estrelas', 'comentario', 'data_avaliacao']

    def create(self, validated_data):
        """
        Creates a new review instance using the validated data.

        Args:
        - validated_data: A dictionary containing the review attributes.

        Returns:
        - The created Avaliacao instance.
        """
        return Avaliacao.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing review instance with new data.

        Args:
        - instance: The existing Avaliacao instance to update.
        - validated_data: A dictionary containing the review's new attributes.

        Returns:
        - The updated Avaliacao instance.
        """
        instance.estrelas = validated_data.get('estrelas', instance.estrelas)
        instance.comentario = validated_data.get('comentario', instance.comentario)
        instance.save()

        return instance