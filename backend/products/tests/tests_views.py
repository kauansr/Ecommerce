from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from products.models import Produtos
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

class ProdutosAPITests(TestCase):
    """
    Test class for the Produtos API. Contains various tests for CRUD operations 
    on products, authentication with JWT tokens, and image upload handling.
    """
    
    def setUp(self):
        """
        Setup method that runs before every test.
        Creates an admin user, generates a test image, creates a product in the database,
        initializes the API client, and generates a JWT access token for authentication.
        """
        # Create an admin user with email, username, and password
        self.user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpass'
        )
        self.user.is_staff = True
        self.user.save()

        # Create a simple image using PIL (Python Imaging Library)
        image = Image.new('RGB', (100, 100), color=(73, 109, 137))
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        # Create the image file for the test
        self.image_file = ContentFile(img_byte_arr.read(), 'produto_teste.jpg')

        # Create product data for the test
        self.produto_data = {
            'nome': 'Produto Teste',
            'descricao': 'Descrição do produto teste',
            'categoria': 'ROUPAS',
            'quantidade': 10,
            'preco': 100.00,
            'produto_imagem': self.image_file,  # Using the generated image
        }

        # Create the product in the database to ensure the product model is available
        self.produto = Produtos.objects.create(**self.produto_data)

        # Initialize the API client to simulate requests
        self.client = APIClient()

        # Generate the JWT access token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_get_produtos(self):
        """
        Test GET request for listing products with JWT authentication.
        Verifies that the response is successful and returns the expected product count.
        """
        url = reverse('produtosadmall')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 product

    def test_create_produto(self):
        """
        Test POST request to create a new product with JWT authentication.
        Verifies that the product is successfully created and includes the image.
        """
        url = reverse('produtosadmall')

        # Ensure the image file is correctly positioned for reading
        self.image_file.seek(0)

        data = {
            'nome': 'Produto Novo',
            'descricao': 'Descrição do novo produto',
            'categoria': 'ROUPAS',  # Valid category
            'quantidade': 15,
            'preco': 150.0,
            'produto_imagem': self.image_file,  # Sending the image with the product data
        }

        # Add authorization header with the JWT access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Make the POST request
        response = self.client.post(url, data, format='multipart')

        # Verify that the response status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the product was created and the correct name is returned
        self.assertEqual(response.data['nome'], 'Produto Novo')

        # Additional checks to ensure the image was properly saved
        self.assertTrue('produto_imagem' in response.data)
        self.assertIsNotNone(response.data['produto_imagem'])

    def test_get_produto(self):
        """
        Test GET request to retrieve a single product with JWT authentication.
        Verifies that the response is successful and returns the correct product.
        """
        url = reverse('produtoadmone', args=[self.produto.pk])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.produto.nome)

    def test_update_produto(self):
        """
        Test PUT request to update a product with JWT authentication.
        Verifies that the product is updated correctly, including the image.
        """
        url = reverse('produtoadmone', args=[self.produto.pk])

        self.image_file.seek(0)  # Ensure the image file is at the start

        data = {
            'nome': 'Produto Atualizado',
            'descricao': 'Descrição do produto atualizado',
            'categoria': 'APARELHOS',
            'quantidade': 20,
            'preco': 200.00,
            'produto_imagem': self.image_file,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Produto Atualizado')

    def test_delete_produto(self):
        """
        Test DELETE request to delete a product with JWT authentication.
        Verifies that the product is successfully deleted and the response status is correct.
        """
        url = reverse('produtoadmone', args=[self.produto.pk])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_produtos_public(self):
        """
        Test GET request to list products without authentication (public access).
        Verifies that the request returns a successful response.
        """
        self.client.logout()  # Log out to simulate no JWT token
        url = reverse('produtosall')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_produto_public(self):
        """
        Test GET request to retrieve a single product without authentication (public access).
        Verifies that the request returns a successful response.
        """
        self.client.logout()  # Log out to simulate no JWT token
        url = reverse('produtoone', args=[self.produto.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_and_get_jwt_token(self):
        """
        Test obtaining a JWT token after logging in with email and password.
        Verifies that the access and refresh tokens are returned.
        """
        url = reverse('token')  # URL to get the JWT token
        data = {
            'email': 'admin@example.com',  # Using email for login
            'password': 'adminpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Access token should be returned
        self.assertIn('refresh', response.data)  # Refresh token should be returned