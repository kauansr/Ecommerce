from django.test import TestCase

from ..models import User


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            email="teste@teste.com",
            username="teste",
            password="1234567k"
        )
    

    def test_get_user(self):
        u1 = User.objects.get(email='teste@teste.com')

        self.assertEquals(u1.__str__(), 'teste')
    
    def test_delete_user(self):
        u1 = User.objects.get(email='teste@teste.com')
        u1.delete()

        self.assertEquals(u1.__str__(), 'teste')