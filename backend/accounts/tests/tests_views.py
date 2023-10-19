from django.urls import reverse
from rest_framework.test import APITestCase
from django.test.client import Client


class UserTestCaseViews(APITestCase):

    def setUp(self):
        self.client.post(reverse('usercreateapi'), data={'email':'testeuser@teste.com','username':'testeuser','password':'1234567k'})

    def test_create_account_status_code_201(self):

        data_json = {
            'email':'testeuser1@teste.com',
            'username':'testeuser1',
            'password':'1234567k'
        }

        res = self.client.post(reverse('usercreateapi'), data=data_json)
        self.assertEquals(res.status_code, 201)
    
    def test_login_status_code_200(self):

        data_json = {
            'email':'testeuser@teste.com',
            'password':'1234567k'
        }

        res = self.client.post(reverse('token'),data=data_json)

        self.assertEquals(res.data['access'], res.data['access'])

    def test_get_users_status_code_200(self):

        res = self.client.get(reverse('usersapi'))

        self.assertEquals(res.status_code, 200)

    def test_get_user_status_code_200(self):

        data_json = {
            'email':'testeuser@teste.com',
            'password':'1234567k'
        }

        reslog = self.client.post(reverse('token'),data=data_json)

        auth = {'Authorization':f'Bearer {reslog.data["access"]}'}


        client = Client()


        res = client.get('/accountapi/accounts/1/',  content_type='application/json', headers=auth)


        self.assertEquals(res.status_code, 200)
    
    def test_put_user_status_code_200(self):

        data_json = {
            'email':'testeuser@teste.com',
            'password':'1234567k'
        }

        reslog = self.client.post(reverse('token'),data=data_json)

        auth = {'Authorization':f'Bearer {reslog.data["access"]}'}


        client = Client()

        data_att = {
            'email':'testeuser@teste.com',
            'username':'@testeattuser',
            'password':'1234567k'
        }


        res = client.put('/accountapi/accounts/1/', data=data_att, content_type='application/json', headers=auth)


        self.assertEquals(res.status_code, 202)
    
    def test_delete_status_code_204(self):

        data_json = {
            'email':'testeuser@teste.com',
            'password':'1234567k'
        }

        reslog = self.client.post(reverse('token'),data=data_json)

        auth = {'Authorization':f'Bearer {reslog.data["access"]}'}


        client = Client()


        res = client.delete('/accountapi/accounts/1/', content_type='application/json', headers=auth)


        self.assertEquals(res.status_code, 204)