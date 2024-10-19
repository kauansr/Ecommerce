from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from accounts.serializers import UsersSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import jwt
from project.settings import SECRET_KEY


class UsersAPI(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        """
        Rota get todos usuarios

        :return: Json
        """

        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class UserAPI(APIView):

    permission_classes = [IsAuthenticated]

    def decode_jwttoken(self):

        """
        Decodifica o token jwt do usuario

        :return: Json
        """

        jwt_encode = self.request.META['HTTP_AUTHORIZATION']

        jwt_clean = jwt_encode.split(" ")

        if not jwt_clean[0]:
            raise ValueError('Token invalido!!')
        
        
        if jwt_clean[0] != 'Bearer':
            raise ValueError('Inavlid token !!!')

        jwt_decode = jwt.decode(jwt_clean[1], SECRET_KEY, algorithms=['HS256'])

        return (jwt_decode, None)


    def get_object(self, username):

        """
        Pega o usuario no banco de dados
        
        :param str username: dados da rota username
        :return: User
        :raise http404: erro 404
        """

        try:
            return User.objects.get(username=username)
        
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):

        """
        Rota get dos usuarios

        :param str username: dados da rota username
        :return: Json
        """

        data_usertoken = self.decode_jwttoken()


        if data_usertoken[0]['username'] != username:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = self.get_object(username=username)
        serializer = UsersSerializer(user)



        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, username):
        
        """
        Atualiza um dado do usuario

        :param str username: dados da rota username
        :return: Json
        """

        data_usertoken = self.decode_jwttoken()

        if data_usertoken[0]['username'] != username:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = self.get_object(username=username)
        serializer = UsersSerializer(user, data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, username):

        """
        Rota delete do usuario

        :param str username: dados da rota username
        :return: Response(http204)
        """

        data_usertoken = self.decode_jwttoken()

        if data_usertoken[0]['username'] != username:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = self.get_object(username=username)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCreateAPI(APIView):

    permission_classes = []

    def post(self, request):

        """
        Rota post cria um usuario

        :return: Json
        """

        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)