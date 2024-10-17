from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.http import Http404
from pedidos.models import Pedidos
from pedidos.serializers import PedidosSerializers
from rest_framework import status
import jwt
from project.settings import SECRET_KEY
from products.models import Produtos
from accounts.models import User

class PedidosAPI(APIView):

    permission_classes = [IsAuthenticated]

    def decode_jwttoken(self):

        jwt_encode = self.request.META['HTTP_AUTHORIZATION']

     
        jwt_clean = jwt_encode.split(" ")

        jwt_bearer = jwt_clean[0]
 
        if not jwt_bearer:
            raise ValueError('Token invalido!!')
        
        if jwt_bearer != 'Bearer':
            raise ValueError('Inavlid token !!!')

        
        jwt_decode = jwt.decode(jwt_clean[1], SECRET_KEY, algorithms=['HS256'])
 

        return (jwt_decode, None)

    def get(self, request):

        data_user = self.decode_jwttoken()

        

        if not data_user[0]['email']:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        ped = Pedidos.objects.filter(email=data_user[0]['id'])
     
        serializer = PedidosSerializers(ped, many=True)

        return Response(serializer.data)
        
        

            
    
    def post(self, request):

        data_user = self.decode_jwttoken()

         

        if not data_user[0]['email']:
            return Response(status=status.HTTP_404_NOT_FOUND)
         

        id_prod = request.data['id']
        id_user = User.objects.filter(id=data_user[0]['id']).first()

        if not id_user.email:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        produt = Produtos.objects.filter(id=id_prod).first()

       
        data = {
            'nome_pedido': produt.nome,
            'preco': produt.preco,
            'email': id_user.id
  
        }
        serializer = PedidosSerializers(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidoAPI(APIView):

    permission_classes = [IsAuthenticated]

    

    def get_object(self, pk):

        try:
            return Pedidos.objects.get(pk=pk)
        
        except Pedidos.DoesNotExist:
            raise Http404
    

    def decode_jwttoken(self):

        jwt_encode = self.request.META['HTTP_AUTHORIZATION']

        jwt_clean = jwt_encode.split(" ")

        jwt_bearer = jwt_clean[0]
        if not jwt_bearer:
            raise ValueError('Token invalido!!')
        
        if jwt_bearer != 'Bearer':
            raise ValueError('Inavlid token !!!')

        jwt_decode = jwt.decode(jwt_clean[1], SECRET_KEY, algorithms=['HS256'])

        return (jwt_decode, None)
    
    def get(self, request, pk):

        data_user = self.decode_jwttoken()
        
        if not data_user[0]['email']:
            return Response(status=status.HTTP_404_NOT_FOUND)

        pedido = self.get_object(pk=pk)
        serializer = PedidosSerializers(pedido)

        return Response(serializer.data)
    
    def delete(self, request, pk):

        data_user = self.decode_jwttoken()
        
        if not data_user[0]['email']:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        
        pedido = self.get_object(pk=pk)
        pedido.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PedidosAdmAPI(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        pedidos = Pedidos.objects.all()
        serializer = PedidosSerializers(pedidos, many=True)

        return Response(serializer.data)


class PedidoAdmAPI(APIView):

    permission_classes = [IsAdminUser]


    def get_object(self, pk):

        try:
            return Pedidos.objects.get(pk=pk)
        
        except Pedidos.DoesNotExist:
            raise Http404


    def get(self, request, pk):


        pedido = self.get_object(pk)
        serializer = PedidosSerializers(pedido)


        return Response(serializer.data)


    def put(self, request, pk):

        
        pedido = self.get_object(pk)
        serializer = PedidosSerializers(pedido, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):


        
        pedido = self.get_object(pk=pk)
        pedido.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)