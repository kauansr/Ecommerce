from rest_framework import serializers
from .models import User

class UsersSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Fields:
    - id: Unique identifier for the user (auto-generated).
    - email: The user's email address.
    - username: The user's username, with validation to ensure it starts with "@".
    - password: The user's password, write-only field.
    - data_joined: The date and time when the user was created.

    Methods:
    - validate_username: Ensures the username starts with "@".
    - validate: Ensures the username, email, and password are not empty.
    - create: Creates a new user with the validated data.
    - update: Updates an existing user's details (username, email, password).

    Meta:
    - model: The model this serializer is based on (User model).
    - fields: The fields to include in the serialized representation.
    """
    
    # The password field is write-only, meaning it won't be returned in responses
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def validate_username(self, username):
        """
        Validates the username to ensure it starts with '@'.
        
        If the username doesn't start with '@', it prepends '@' to the username.
        
        Args:
        - username: The username to validate.
        
        Returns:
        - The modified username if it doesn't start with '@', or the original username.
        """
        if username and username[0] != "@":
            return f'@{username}'
        return username

    def validate(self, data):
        """
        Validates the data to ensure that the username, email, and password are not empty.
        
        Args:
        - data: The data dictionary containing the user attributes to validate.
        
        Raises:
        - ValidationError: If any of the required fields are missing or empty.
        
        Returns:
        - The validated data.
        """
        if not data.get('username') or data.get('username') == '':
            raise serializers.ValidationError({'username': 'This field cannot be blank.'})
        if not data.get('email') or data.get('email') == '':
            raise serializers.ValidationError({'email': 'This field cannot be blank.'})
        if not data.get('password') or data.get('password') == '':
            raise serializers.ValidationError({'password': 'This field cannot be blank.'})
        
        return data

    def create(self, validated_data):
        """
        Creates a new user using the validated data.
        
        Args:
        - validated_data: The validated user data (username, email, password).
        
        Returns:
        - The created User instance.
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing user's details (username, email, and password).
        
        Args:
        - instance: The existing User instance to update.
        - validated_data: The validated data to update the user with.
        
        Returns:
        - The updated User instance.
        """
        # Update username if provided and ensure it starts with '@'
        new_username = validated_data.get("username")
        if new_username is not None and new_username.strip():
            if "@" not in new_username:
                new_username = f'@{new_username}'
            instance.username = new_username

        # Update email if provided
        new_email = validated_data.get('email')
        if new_email is not None and new_email.strip():
            instance.email = new_email

        # Update password if provided
        new_password = validated_data.get('password')
        if new_password is not None and new_password.strip():
            instance.set_password(new_password)

        # Save the updated instance
        instance.save()
        return instance

    class Meta:
        model = User  # The model this serializer corresponds to
        fields = ['id', 'email', 'username', 'password', 'data_joined']  # The fields to include in the serialized data