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
import json
from django.http import Http404
from django.contrib.sessions.middleware import SessionMiddleware

from catalog import views
from accounts.views import signup
from catalog.models import User, Task, Solution
from catalog import models
from catalog.serializers import SubmitUserSerializer, UserSerializer, TaskSerializer
from catalog.additions import solution_testing


@pytest.mark.django_db
class SignUpViewTest(TestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = signup(req)
        assert resp.status_code == 200, 'Should be callable by any user'

    def test_authenticated_user(self):
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = signup(req)
        assert resp.status_code == 200, 'Should be callable by authenticated user'

    def test_post(self):
        data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password1": "Passxyzord1",
            "password2": "Passxyzord1",
        }

        req = RequestFactory().post('/', data=data)
        req.user = AnonymousUser()
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        resp = signup(req)
        assert resp.status_code == 302, 'Should redirect to success view'


@pytest.mark.django_db
class IndexViewTest(TestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.index(req)
        assert resp.status_code == 200, 'Should be callable by any user'

    def test_authenticated_user(self):
        solution = mixer.blend('catalog.Solution')
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.index(req)
        assert resp.status_code == 200, 'Should be callable by authenticated user'


@pytest.mark.django_db
class UserListViewTest(TestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.UserListView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        user = mixer.blend('catalog.User', is_superuser=True)
        req = RequestFactory().get('/')
        req.user = user
        resp = views.UserListView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by authenticated user'


@pytest.mark.django_db
class UserDetailViewTest(TestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.UserDetailView.as_view()(req, pk=1)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.UserDetailView.as_view()(req, pk=1)
        assert resp.status_code == 200, 'Should be callable by authenticated user'


@pytest.mark.django_db
class MyTaskListViewTest(TestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.MyTaskListView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.MyTaskListView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by authenticated user'


@pytest.mark.django_db
class TaskListViewTest(TestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.TaskListView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by any user'

    def test_authenticated_user(self):
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.TaskListView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by authenticated user'


@pytest.mark.django_db
class TaskDetailViewTest(TestCase):
    def test_anonymous(self):
        task = mixer.blend('catalog.Task')
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.TaskDetailView.as_view()(req, pk=1)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.TaskDetailView.as_view()(req, pk=1)
        assert resp.status_code == 200, 'Should be callable by authenticated user'



@pytest.mark.django_db
class SolutionListViewTest(TestCase):
    def test_anonymous(self):
        task = mixer.blend('catalog.Task')
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.SolutionListView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.SolutionListView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by authenticated user'



@pytest.mark.django_db
class SolutionDetailViewTest(TestCase):
    def test_anonymous(self):
        solution = mixer.blend('catalog.Solution')
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.SolutionDetailView.as_view()(req, pk=1)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        solution = mixer.blend('catalog.Solution')
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.SolutionDetailView.as_view()(req, pk=1)
        assert resp.status_code == 200, 'Should be callable by authenticated user'



@pytest.mark.django_db
class EditTaskViewTest(TestCase):
    def test_get_anonymous(self):
        task = mixer.blend('catalog.Task')
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.editTask(req, pk=1)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_get_authenticated_user(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.editTask(req, pk=1)
        assert resp.status_code == 200, 'Should be callable by authenticated user'

    def test_edit_task_get_object_if_does_not_exists(self):
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        with pytest.raises(Http404):
            views.editTask(req, pk=1), 'Should be return 404 if does not exist'
        
    def test_post(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        data = {'task_name': 'new_name', 'text':task.text}
        req = RequestFactory().post('/', data=data)
        req.user = user
        resp = views.editTask(req, pk=1)
        assert resp.status_code == 302, 'Should redirect to success view'


@pytest.mark.django_db
class DeleteTaskViewTest(TestCase):
    def test_anonymous(self):
        task = mixer.blend('catalog.Task')
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.deleteTask(req, pk=1)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.deleteTask(req, pk=1)
        assert resp.status_code == 200, 'Should be callable by authenticated user'

    def test_post(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        data = {}
        req = RequestFactory().post('/', data=data)
        req.user = user
        resp = views.deleteTask(req, pk=1)
        assert resp.status_code == 302, 'Should redirect to success view'


@pytest.mark.django_db
class EditTestsViewTest(TestCase):
    def test_anonymous(self):
        task = mixer.blend('catalog.Task')
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.editTests(req, pk=1)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.editTests(req, pk=1)
        assert resp.status_code == 200, 'Should be callable by authenticated user'

    # def test_post(self):
    #     task = mixer.blend('catalog.Task')
    #     user = mixer.blend('catalog.User')
    #     test = mixer.blend('catalog.Test')
    #     data = {'test_input': test.test_input, 'test_output':test.test_output}
    #     req = RequestFactory().post('/', data=data)
    #     req.user = user
    #     resp = views.editTests(req, pk=1)
    #     assert resp.status_code == 302, 'Should redirect to success view'


@pytest.mark.django_db
class SubmitSolutionViewTest(TestCase):
    def test_anonymous(self):
        task = mixer.blend('catalog.Task')
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.submit(req, pk=1)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.submit(req, pk=1)
        assert resp.status_code == 200, 'Should be callable by authenticated user'

    def test_post(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        data = {'task': task, 'user': user, 'solution': 'new_solution', 'language': 'Python'}
        req = RequestFactory().post('/', data=data)
        req.user = user
        resp = views.submit(req, pk=1)
        assert resp.status_code == 302, 'Should redirect to success view'

    def test_post_with_invalid_data(self):
        task = mixer.blend('catalog.Task')
        user = mixer.blend('catalog.User')
        data = {'task': task, 'user': user, 'solution': 'new_solution', 'language': 'Pytho'}
        req = RequestFactory().post('/', data=data)
        req.user = user
        resp = views.submit(req, pk=1)
        assert resp.status_code == 200, 'Should not accept invalid data'


@pytest.mark.django_db
class SubmitTaskViewTest(TestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.submitTask(req)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_authenticated_user(self):
        user = mixer.blend('catalog.User')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.submitTask(req)
        assert resp.status_code == 200, 'Should be callable by authenticated user'


    # def test_post(self):
    #     task = mixer.blend('catalog.Task')
    #     user = mixer.blend('catalog.User')
    #     data = {'task_name': task, 'publisher': user, 'text': 'new_solution'}
    #     req = RequestFactory().post('/', data=data)
    #     req.user = user
    #     resp = views.submitTask(req)
    #     assert resp.status_code == 302, 'Should redirect to success view'
### Not working
    # def test_post(self):
    #     user = mixer.blend('catalog.User')
    #     data = {'task_name': 'new_task', 'publisher': user, 'text': 'new_task'}
    #     req = RequestFactory().post('/', data=data)
    #     req.user = user
    #     resp = views.submitTask(req)
    #     assert resp.status_code == 302, 'Should redirect to success view'
