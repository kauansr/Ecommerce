from rest_framework import serializers
from .models import User


class UsersSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False, allow_blank=True)


    def validate_username(self, username):

        if username and username[0] != "@":
            return f'@{username}'
        return username
    
    def validate(self, data):
        if not data.get('username') or data.get('username') == '':
            raise serializers.ValidationError({'username': 'Este campo não pode ser em branco.'})
        if not data.get('email') or data.get('email') == '':
            raise serializers.ValidationError({'email': 'Este campo não pode ser em branco.'})
        if not data.get('password') or data.get('password') == '':
            raise serializers.ValidationError({'password': 'Este campo não pode ser em branco.'})
    
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
       
        new_username = validated_data.get("username")
        if new_username is not None and new_username.strip():
            if "@" not in new_username:
                new_username = f'@{new_username}'
            instance.username = new_username

        
        new_email = validated_data.get('email')
        if new_email is not None and new_email.strip():
            instance.email = new_email

        new_password = validated_data.get('password')
        if new_password is not None and new_password.strip():
            instance.set_password(new_password)

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'data_joined']

    