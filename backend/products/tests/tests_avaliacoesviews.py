from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Produtos, Avaliacao
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import TestCase

User = get_user_model()

class AvaliacaoTests(TestCase):
    def setUp(self):
        """
        Set up necessary data for the tests:
        - Create a test user with email, username, and password.
        - Create a test product.
        - Generate JWT token for the user.
        - Create an API client to make requests.
        """
        # Create user with email, username, and password
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        
        # Create a test product
        self.produto = Produtos.objects.create(
            nome="Test Product",
            descricao="Test product description",
            categoria="APARELHOS",
            quantidade=10,
            preco=100.0
        )
        
        # Get JWT token for authentication
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Create API client to make requests
        self.client = APIClient()

    def test_create_avaliacao(self):
        """
        Test creating a review (avaliacao) with JWT authentication.
        The request must include a valid JWT token in the Authorization header.
        """
        url = reverse('avaliacoes-list-create', args=[self.produto.id])
        
        # Headers with authentication token
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        data = {
            'nota': 5,
            'comentario': 'Excellent product!'
        }

        # Make POST request to create the review
        response = self.client.post(url, data, format='json', headers=headers)
        
        # Verify that the review was created correctly
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['produto'], self.produto.id)
        self.assertEqual(response.data['usuario'], self.user.id)

    def test_list_reviews(self):
        """
        Test listing reviews for a product.
        Verifies that reviews can be retrieved successfully.
        """
        # Create a review for the product
        Avaliacao.objects.create(
            produto=self.produto,
            usuario=self.user,
            estrelas=5,
            comentario="Great!"
        )

        url = reverse('avaliacoes-list-create', args=[self.produto.id])
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        # Make GET request to list reviews
        response = self.client.get(url, headers=headers)
        
        # Verify that reviews are listed correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['produto'], self.produto.id)
        self.assertEqual(response.data[0]['usuario'], self.user.id)

    def test_update_review(self):
        """
        Test updating an existing review.
        The review should be updated with new data.
        """
        # Create a review
        avaliacao = Avaliacao.objects.create(
            produto=self.produto,
            usuario=self.user,
            estrelas=4,
            comentario="Good, but could be improved"
        )

        url = reverse('avaliacoes-update', args=[avaliacao.id])
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        # Data for updating the review
        data = {
            'estrelas': 5,
            'comentario': 'Excellent! Improved product!'
        }

        # Make PUT request to update the review
        response = self.client.put(url, data, format='json', headers=headers)

        # Verify that the review was updated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estrelas'], 5)
        self.assertEqual(response.data['comentario'], 'Excellent! Improved product!')

    def test_delete_review(self):
        """
        Test deleting an existing review.
        The review should be deleted successfully.
        """
        # Create a review
        avaliacao = Avaliacao.objects.create(
            produto=self.produto,
            usuario=self.user,
            estrelas=3,
            comentario="Initial review"
        )

        url = reverse('avaliacoes-delete', args=[avaliacao.id])
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        # Make DELETE request to remove the review
        response = self.client.delete(url, headers=headers)

        # Verify that the review was deleted correctly
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Avaliacao.objects.filter(id=avaliacao.id).exists())

    def test_create_review_without_authentication(self):
        """
        Test creating a review without authentication.
        The request should return a 401 Unauthorized status code.
        """
        url = reverse('avaliacoes-list-create', args=[self.produto.id])
        data = {
            'estrelas': 4,
            'comentario': 'Review without login'
        }

        # Make POST request without authentication
        response = self.client.post(url, data, format='json')
        
        # Verify that the response is Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)