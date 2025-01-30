from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Produtos
from pedidos.models import Pedidos, ItemPedido
from decimal import Decimal

User = get_user_model()

class PedidoTests(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a test product
        self.produto = Produtos.objects.create(
            nome='Produto Teste', descricao='Product description', categoria='APARELHOS', quantidade=10, preco=50.0
        )
        
    def test_create_order(self):
        """Test the creation of an order"""
        
        url = reverse('pedidosapi')  # URL for creating orders
        data = {
            'itens': [
                {
                    'produto': self.produto.id,
                    'quantidade': 2
                }
            ]
        }
        
        # Sending a POST request to create the order
        response = self.client.post(url, data, format='json')

        # Check if the order was successfully created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pedidos.objects.count(), 1)
        self.assertEqual(response.data['cliente'], self.user.id)
        self.assertEqual(response.data['total'], '100.00')  # 2 * 50.00 = 100.00

    def test_list_orders(self):
        """Test the listing of orders for an authenticated user"""
        
        # Create a test order for the user
        pedido = Pedidos.objects.create(cliente=self.user, email=self.user.email, total=Decimal('100.00'))

        # Create items for the order
        ItemPedido.objects.create(pedido=pedido, produto=self.produto, quantidade=2, preco_unitario=self.produto.preco)
        
        url = reverse('pedidosapi')  # URL to list orders
        response = self.client.get(url, format='json')
        
        # Check if the order appears in the list
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # The user should only have one order
        self.assertEqual(response.data[0]['cliente'], self.user.id)
        self.assertEqual(response.data[0]['total'], '100.00')

    def test_get_order_detail(self):
        """Test retrieving the details of a specific order"""
        
        # Create a test order
        pedido = Pedidos.objects.create(cliente=self.user, email=self.user.email, total=Decimal('100.00'))

        # Create items for the order
        item = ItemPedido.objects.create(pedido=pedido, produto=self.produto, quantidade=2, preco_unitario=self.produto.preco)

        url = reverse('pedidoapi', kwargs={'pk': pedido.id})  # URL to get a specific order
        response = self.client.get(url, format='json')

        # Check if the order was returned correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pedido']['cliente'], self.user.id)
        self.assertEqual(response.data['pedido']['total'], '100.00')
        self.assertEqual(len(response.data['itens']), 1)  # Verify the order has one item
        self.assertEqual(response.data['itens'][0]['produto'], self.produto.id)

    def test_delete_order(self):
        """Test the deletion of an order"""
        
        # Create a test order
        pedido = Pedidos.objects.create(cliente=self.user, email=self.user.email, total=Decimal('100.00'))

        # Create items for the order
        item = ItemPedido.objects.create(pedido=pedido, produto=self.produto, quantidade=2, preco_unitario=self.produto.preco)

        url = reverse('pedidoapi', kwargs={'pk': pedido.id})  # URL to delete a specific order
        response = self.client.delete(url, format='json')

        # Check if the order was successfully deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pedidos.objects.count(), 0)  # No orders should remain in the database after deletion
        self.assertEqual(ItemPedido.objects.count(), 0)  # Items should also be deleted

    def test_create_order_without_items(self):
        """Test creating an order without items, which should return an error"""
        
        url = reverse('pedidosapi')  # URL for creating orders
        data = {}  # No items
        
        # Sending a POST request to create the order
        response = self.client.post(url, data, format='json')

        # Check if the error message is returned correctly
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['msg'], 'You must provide items for the order!')