from rest_framework import serializers
from .models import User


class UsersSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)


    def validate_username(self, username):

        username_data: str = username

        

        if "@" in username_data[0]:
            username_validado = username_data

        else:
            username_validado: str =  f'@{username_data}' 

        return username_validado

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
    def update(self, instance, validated_data):

        instance.username = f'@{validated_data.get("username", instance.username)}'
        if "@"  in validated_data.get("username"):
            instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'data_joined']

    