from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from ..models import User

class UserTestCase(TestCase):
    """
    Test case for testing user creation, retrieval, and deletion in the database.

    This test case provides methods to verify the user functionality, including:
    - Creating a user.
    - Retrieving the user and checking its string representation.
    - Deleting a user and confirming that the user is no longer in the database.
    """

    def setUp(self):
        """
        Setup method to create a test user before each test method is run.

        Creates a user with predefined email, username, and password.
        """
        self.user = User.objects.create(
            email="teste@teste.com",
            username="teste",
            password="1234567k"
        )
    

    def test_get_user(self):
        """
        Test the retrieval of a user by email and validate its string representation.

        - Retrieves the user created in the setup method using their email.
        - Checks that the string representation of the user is correct (i.e., the username).
        """
        u1 = User.objects.get(email='teste@teste.com')

        # Assert that the string representation of the user matches the expected username
        self.assertEqual(u1.__str__(), 'teste')
    
    def test_delete_user(self):
        """
        Test the deletion of a user and confirm that the user no longer exists in the database.

        - Retrieves the user by email.
        - Deletes the user.
        - Ensures that attempting to fetch the user after deletion raises an `ObjectDoesNotExist` exception.
        """
        u1 = User.objects.get(email='teste@teste.com')
        
        # Delete the user
        u1.delete()

        # Assert that the user does not exist anymore by attempting to retrieve them
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(email='teste@teste.com')