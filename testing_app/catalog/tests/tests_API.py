from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from rest_framework.test import APIRequestFactory
from django.test import TestCase,Client
from django.urls import reverse
from rest_framework import status
import json

from catalog.models import User, Task, SolutionInstance
from catalog.serializers import SubmitUserSerializer

class UserRegistrationAPIViewTestCase(APITestCase):

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password1": "Passxyzord1",
            "password2": "Passxyzord1",
        }

        response = self.client.post('/catalog/API/rest_auth_2/', user_data)
        # print(response.content)
        self.assertEqual(201, response.status_code)

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password1": "Passxyzord1",
            "password2": "Passxyzord1",
        }
        response = self.client.post('/catalog/API/rest_auth_2/', user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "email": "test2@testuser.com",
            "password1": "Passxyzord1",
            "password2": "Passxyzord1",
        }
        response = self.client.post('/catalog/API/rest_auth_2/', user_data_2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):

    def setUp(self):
        self.url = "/catalog/API/rest_auth/login/"
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "snowman"})
        # print('without', response.content)
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "I_know"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        # self.assertTrue("auth_token" in json.loads(response.content))

    def test_login_if_user_exist(self):
        self.client.login(username=self.username, password=self.password)
        user = User.objects.get(username=self.username)
        url = reverse('API_user-detail', kwargs={'pk': user.id}) 
        response = self.client.get(url)
        # print('if_exists', response.content)
        self.assertEqual(200, response.status_code)

    def test_login_if_user_does_not_exist(self):
        self.assertFalse(self.client.login(username="adsad", password="adsda"))

    def test_user_post_1(self):
        url = reverse("API_users")
        data = {
            'password': "you_know_nothing",
            'username': "john",
        }
        data = json.dumps(SubmitUserSerializer(instance=User(data)).data)

        factory = APIRequestFactory()
        request = factory.post(url, data, format='json')

    def test_user_get(self):
        url = reverse("API_users")
        client = APIClient()
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

