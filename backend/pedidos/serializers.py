from rest_framework import serializers
from pedidos.models import Pedidos
from accounts.models import User


class PedidosSerializers(serializers.ModelSerializer):

    def validate_email(self, email):


        data_user = User.objects.filter(email=email).first()

        if not data_user.email:
            raise ValueError('Email not validate')
        
        email_validado = data_user.email

        return email_validado

    def create(self, validated_data):
        return Pedidos.objects.create(**validated_data)

    class Meta:
        model = Pedidos
        fields = '__all__'