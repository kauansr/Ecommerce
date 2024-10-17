from rest_framework import serializers
from pedidos.models import Pedidos
from accounts.models import User


class PedidosSerializers(serializers.ModelSerializer):


    def create(self, validated_data):
        return Pedidos.objects.create(**validated_data)

    class Meta:
        model = Pedidos
        fields = '__all__'