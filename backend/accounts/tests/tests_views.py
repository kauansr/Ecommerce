from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import User
import json

class UserTestCaseViews(APITestCase):
    """
    Test case for testing user-related API views, including user creation, login,
    fetching user details, updating user data, and deleting a user.

    This test class includes methods to verify:
    - Creation of a new user and response status.
    - Login and token generation.
    - Retrieval of user details with proper authentication.
    - Update user data via PUT request.
    - Delete user and ensure proper responses and behaviors.
    """
    
    def setUp(self):
        """
        Setup method to create a test user before each test method is run.
        
        Creates a test user with predefined email, username, and password, 
        and sets up the data for testing the login process.
        """
        self.client.post(reverse('usercreateapi'), data={'email': 'testeuser@teste.com', 'username': 'testeuser', 'password': '1234567k'})
        self.user_data = {
            'email': 'testeuser@teste.com',
            'password': '1234567k'
        }

    def test_create_account_status_code_201(self):
        """
        Test user creation via POST request to the user creation API endpoint.

        Verifies that the creation of a new user returns status code 201.
        """
        data_json = {
            'email': 'testeuser1@teste.com',
            'username': 'testeuser1',
            'password': '1234567k'
        }
        res = self.client.post(reverse('usercreateapi'), data=data_json)
        self.assertEqual(res.status_code, 201)

    def test_login_status_code_200(self):
        """
        Test login functionality via POST request to obtain a JWT token.

        Verifies that a valid login returns status code 200 and includes the 'access' token.
        """
        res = self.client.post(reverse('token'), data=self.user_data)
        self.assertIn('access', res.data)  # Verifies the 'access' token is present

    def test_get_user_status_code_200(self):
        """
        Test if authenticated user can retrieve their own details.

        Verifies that the user can fetch their details after logging in with a valid JWT token.
        """
        reslog = self.client.post(reverse('token'), data=self.user_data)
        auth = {'Authorization': f'Bearer {reslog.data["access"]}'}

        user = User.objects.get(email=self.user_data['email'])

        res = self.client.get(f'/accountapi/accounts/{user.username}/', content_type='application/json', HTTP_AUTHORIZATION=auth['Authorization'])
        self.assertEqual(res.status_code, 200)

    def test_put_user_status_code_200(self):
        """
        Test the updating of user details via PUT request.

        Verifies that the user can update their details and the changes are reflected correctly.
        """
        reslog = self.client.post(reverse('token'), data=self.user_data)
        auth = {'Authorization': f'Bearer {reslog.data["access"]}'}

        data_att = {
            'email': 'testeuser@teste.com',
            'username': '@testeattuser',
            'password': '1234567k'
        }

        user = User.objects.get(email=self.user_data['email'])

        # Update the user with new data
        res = self.client.put(f'/accountapi/accounts/{user.username}/', data=json.dumps(data_att), content_type='application/json', HTTP_AUTHORIZATION=auth['Authorization'])
        self.assertEqual(res.status_code, 202)

        # Check if the username was updated correctly
        res_get = self.client.get(f'/accountapi/accounts/{data_att.get("username")}/', content_type='application/json', HTTP_AUTHORIZATION=auth['Authorization'])
        self.assertEqual(res_get.data["username"], '@testeattuser')

    def test_delete_status_code_204(self):
        """
        Test user deletion via DELETE request.

        Verifies that the user is deleted successfully and cannot be accessed again.
        """
        reslog = self.client.post(reverse('token'), data=self.user_data)
        auth = {'Authorization': f'Bearer {reslog.data["access"]}'}

        user = User.objects.get(email=self.user_data['email'])

        # Delete the user
        res = self.client.delete(f'/accountapi/accounts/{user.username}/', content_type='application/json', HTTP_AUTHORIZATION=auth['Authorization'])
        self.assertEqual(res.status_code, 204)

        # After deletion, attempt to access the user's data with the same token (should return 401)
        res_get = self.client.get(f'/accountapi/accounts/{user.username}/', content_type='application/json', HTTP_AUTHORIZATION=auth['Authorization'])
        self.assertEqual(res_get.status_code, 401)  # The token will no longer be valid after user deletion

        # Attempt to log in again with the credentials of the deleted user (should return 401)
        res_login = self.client.post(reverse('token'), data=self.user_data)  # Trying to log in with the deleted user's credentials
        self.assertEqual(res_login.status_code, 401)  # The token is now invalid