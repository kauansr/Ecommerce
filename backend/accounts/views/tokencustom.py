from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import authentication
from rest_framework import exceptions
import jwt
from project.settings import SECRET_KEY
from accounts.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)

        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['data_joined'] = str(user.data_joined)

        return token
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        jwt_encode = request.META['HTTP_AUTHORIZATION']
        jwt_clean = jwt_encode.split(" ")
        jwt_decode = jwt.decode(jwt_clean[1], SECRET_KEY, algorithms=['HS256'])

        email = jwt_decode[0]['email']

        if not jwt_encode:
            return None
        
        try:
            user = User.objects.get(email=email)
        
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user found')
        
        return (user, None)