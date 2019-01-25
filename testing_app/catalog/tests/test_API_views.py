import pytest
from django.test import TestCase
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from rest_framework.test import APIRequestFactory
from django.test import TestCase,Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate
import json

from catalog import views
from accounts.views import signup
from catalog.models import User, Task, Solution
from catalog import models
from catalog.serializers import SubmitUserSerializer, UserSerializer, TaskSerializer
from catalog.additions import solution_testing


"""
API Tests
"""
@pytest.mark.django_db
class UserRegistrationAPIViewTest(APITestCase):

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


@pytest.mark.django_db
class UserLoginAPIViewTestCase(APITestCase):

    def setUp(self):
        self.url = "/catalog/API/rest_auth/login/"
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "snowman"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "I_know"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)

    def test_login_if_user_exist(self):
        self.client.login(username=self.username, password=self.password)
        user = User.objects.get(username=self.username)
        url = reverse('API_user-detail', kwargs={'pk': user.id}) 
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_login_if_user_does_not_exist(self):
        self.assertFalse(self.client.login(username="adsad", password="adsda"))

    def test_user_get_API_users_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("API_users")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_get_API_tasks_without_auth(self):
        url = reverse("API_tasks")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_get_API_tasks_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("API_tasks")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_get_API_users_without_auth(self):
        url = reverse("API_users")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)

    def test_user_get_API_mytasks_without_auth(self):
        url = reverse("API_mytasks")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 302)

    def test_user_get_API_mytasks_with_auth(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("API_mytasks")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_update_without_authentication(self):
        url = reverse('API_user-detail', kwargs={'pk': 1}) 
        user_data = {
            "username": "john_2",
        }

        response = self.client.put(url, user_data)
        self.assertEqual(403, response.status_code)

    def test_user_update_with_authentication(self):
        self.client.login(username=self.username, password=self.password)
        user = User.objects.get(username=self.username)
        url = reverse('API_user-detail', kwargs={'pk': user.id})

        user_data = {
            "username": "john_2",
            'password': self.password
        }

        response = self.client.put(url, user_data)
        self.assertEqual(200, response.status_code)


@pytest.mark.django_db
class TaskDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.task_name = 'task'
        self.text = 'new task'

    def test_create_task(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_task-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        data = {'text': self.text, 'task_name': self.task_name, 'publisher': self.user}
        self.task = Task.objects.create(task_name=self.task_name, text=self.text, publisher=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class EditTaskAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.task_name = 'task'
        self.text = 'new task'

    def test_create_task(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_editTask', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        data = {'text': self.text, 'task_name': self.task_name, 'publisher': self.user}
        self.task = Task.objects.create(task_name=self.task_name, text=self.text, publisher=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TaskListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.task_name = 'task'
        self.text = 'new task'

    def test_post_task(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_tasks')
        data = {'text': self.text, 'task_name': self.task_name}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_task_invalid_information(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_tasks')
        data = {'task_name': self.task_name}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class SubmitTaskAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.task_name = 'task'
        self.text = 'new task'

    # def test_post_task(self):
    #     self.client.login(username=self.username, password=self.password)
    #     url = reverse('API_submitTask')
    #     data = {'text': self.text, 'task_name': self.task_name, "publisher": UserSerializer(self.user).data}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, 302)

    def test_post_task_invalid_information(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_submitTask')
        data = {'task_name': self.task_name}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class MyTaskListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.task_name = 'task'
        self.text = 'new task'

    def test_post_mytask(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_mytasks')
        user = UserSerializer(self.user)
        data = {'text': self.text, 'task_name': self.task_name}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_mytask_invalid_information(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_mytasks')
        data = {'task_name': self.task_name}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class SolutionAPIViewTestCase(APITestCase):

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.task_name = 'task'
        self.text = 'new task'
        self.task = Task.objects.create(
            task_name=self.task_name, 
            text=self.text, 
            publisher=self.user
            )

        self.solution = 'a = input()\nprint(a)'
        self.language = 'Python'

        self.test_input = 'hahaha'
        self.test_output = 'hahaha'

    # def test_create_solution(self):
    #     self.client.login(username=self.username, password=self.password)
    #     url = reverse('API_solution-detail', kwargs={'pk': 1})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 404)

    #     self.solution = Solution.objects.create(
    #         solution=self.solution, 
    #         task=self.task, 
    #         user=self.user, 
    #         language=self.language
    #         )

    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class SolutionListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = "/catalog/API/rest_auth/login/"
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_get_solution(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_solutions')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


@pytest.mark.django_db
class CreateSolutionAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = "/catalog/API/rest_auth/login/"
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.solution = 'a = input()\nprint(a)'
        self.language = 'Python'

    def test_get_solution(self):
        task = mixer.blend('catalog.Task')
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_submitSolution-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    # def test_post_solution(self):
    #     task = mixer.blend('catalog.Task')
    #     self.client.login(username=self.username, password=self.password)
    #     url = reverse('API_submitSolution-detail', kwargs={'pk': 1})
    #     data = {
    #         'solution': self.solution, 
    #         'task': TaskSerializer(task).data, 
    #         'user': UserSerializer(self.user).data, 
    #         'language': self.language
    #     }
    #     response = self.client.post(url, data=data, format='json')
    #     self.assertEqual(response.status_code, 302)

    def test_post_solution_invalid_input(self):
        task = mixer.blend('catalog.Task')
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_submitSolution-detail', kwargs={'pk': 1})
        data = {
            'solution': self.solution, 
            'task': TaskSerializer(task).data, 
            'user': UserSerializer(self.user).data,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestAPIViewTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.task_name = 'TTask'
        self.text = 'new task'
        self.task = Task.objects.create(task_name=self.task_name, text=self.text, publisher=self.user)

        self.test_input = 'hahaha'
        self.test_output = 'hahaha'

    def test_create_test(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_test-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.test = models.Test.objects.create(test_input=self.test_input, test_output=self.test_output, task=self.task)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_test(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_tests')
        task = TaskSerializer(self.task)
        data = {'test_input': self.test_input, 'test_output': self.test_output, 'task': self.task.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_test_invalid_data(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_tests')
        task = TaskSerializer(self.task)
        data = {'test_input': self.test_input, 'test_output': self.test_output}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_get_test(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('API_tests')
        task = TaskSerializer(self.task)
        # data = {'test_input': self.test_input, 'test_output': self.test_output, 'task': self.task.id}
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
