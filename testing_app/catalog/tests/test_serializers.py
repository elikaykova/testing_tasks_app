import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.test import RequestFactory
from django.test import TestCase
from django.utils import timezone

# Create your tests here.
from catalog import views
from catalog import models
from catalog import serializers


@pytest.mark.django_db
class UserSerializerTest(TestCase):
    def test_user_serializer_no_data(self):
        data = {}
        mm = serializers.UserSerializer(data=data)
        assert mm.is_valid() is False

    def test_user_serializer_with_invalid_data(self):
        data = {'username': 'new_user', 'password': 'abc', 'user_progress': 'a'}
        mm = serializers.UserSerializer(data=data)
        assert mm.is_valid() is False
        assert 'user_progress' in mm.errors

    def test_user_serializer_with_valid_data(self):
        data = {'username': 'new_user', 'password': 'abc', 'user_progress': 1}
        mm = serializers.UserSerializer(data=data)
        assert mm.is_valid() is True

    def test_user_create(self):
        data = {'username': 'new_user', 'password': 'abc'}
        user = serializers.UserSerializer()
        user = user.create(validated_data=data)
        assert user.username == 'new_user' 


@pytest.mark.django_db
class SubmitUserSerializerTest(TestCase):
    def test_user_serializer_no_data(self):
        data = {}
        mm = serializers.SubmitUserSerializer(data=data)
        assert mm.is_valid() is False

    def test_user_serializer_with_invalid_data(self):
        data = {'username': 'new_user', 'password': 'abc', 'email': 2}
        mm = serializers.SubmitUserSerializer(data=data)
        assert mm.is_valid() is False
        assert 'email' in mm.errors

    def test_user_serializer_with_valid_data(self):
        data = {'username': 'new_user', 'password': 'abc'}
        mm = serializers.SubmitUserSerializer(data=data)
        assert mm.is_valid() is True

    def test_user_create(self):
        data = {'username': 'new_user', 'password': 'abc'}
        user = serializers.SubmitUserSerializer()
        user = user.create(validated_data=data)
        assert user.username == 'new_user' 


@pytest.mark.django_db
class TaskSerializerTest(TestCase):
    def test_task_serializer_no_data(self):
        data = {}
        mm = serializers.TaskSerializer(data=data)
        assert mm.is_valid() is False

    def test_task_serializer_with_invalid_data(self):
        user = mixer.blend('catalog.User')
        data = {'task_name': 'new_task', 'text': 'abc', 'publisher': user.id, 'release_date': 'a'}
        mm = serializers.TaskSerializer(data=data)
        assert mm.is_valid() is False
        assert 'release_date' in mm.errors

    def test_task_serializer_with_valid_data(self):
        user = mixer.blend('catalog.User')
        data = {'task_name': 'new_task', 'text': 'abc', 'publisher': user.id}
        mm = serializers.TaskSerializer(data=data)
        assert mm.is_valid() is True

    def test_task_create(self):
        user = mixer.blend('catalog.User')
        data = {'task_name': 'new_task', 'text': 'abc', 'publisher': user}
        task = serializers.TaskSerializer()
        task = task.create(validated_data=data)
        assert task.task_name == 'new_task' 
        assert task.text == 'abc'
        assert task.publisher.id == 1

    def test_task_update(self):
        user = mixer.blend('catalog.User')
        data = {'task_name': 'new_task', 'text': 'abc', 'publisher': user}
        task_s = serializers.TaskSerializer(data=data)
        task = task_s.create(validated_data=data)
        data = {'task_name': 'new_name'}
        task_s = task_s.update(instance=task, validated_data=data)
        assert task.task_name == 'new_name' 
        assert task.text == 'abc'
        assert task.publisher.id == 1


@pytest.mark.django_db
class TestSerializerTest(TestCase):
    def test_test_serializer_no_data(self):
        data = {}
        mm = serializers.TestSerializer(data=data)
        assert mm.is_valid() is False

    def test_test_serializer_with_invalid_data(self):
        task = mixer.blend('catalog.Task')
        data = {'test_input': 'new_user', 'test_output': 'abc', 'test_num': 'a', 'task': task.id}
        mm = serializers.TestSerializer(data=data)
        assert mm.is_valid() is False
        assert 'test_num' in mm.errors

    def test_test_serializer_with_valid_data(self):
        task = mixer.blend('catalog.Task')
        data = {'test_input': 'new_user', 'test_output': 'abc', 'task': task.id}
        mm = serializers.TestSerializer(data=data)
        assert mm.is_valid() is True

    def test_task_create(self):
        user = mixer.blend('catalog.User')
        data = {'task_name': 'new_task', 'text': 'abc', 'publisher': user}
        task = serializers.SubmitTaskSerializer(context={'user': user})
        task = task.create(validated_data=data)
        assert task.task_name == 'new_task' 
        assert task.text == 'abc'
        assert task.publisher.id == 1

    def test_task_update(self):
        user = mixer.blend('catalog.User')
        data = {'task_name': 'new_task', 'text': 'abc', 'publisher': user}
        task_s = serializers.SubmitTaskSerializer(data=data, context={'user': user})
        task = task_s.create(validated_data=data)
        data = {'task_name': 'new_name'}
        task_s = task_s.update(instance=task, validated_data=data)
        assert task.task_name == 'new_name' 
        assert task.text == 'abc'
        assert task.publisher.id == 1


@pytest.mark.django_db
class SolutionSerializerTest(TestCase):
    def test_solution_serializer_no_data(self):
        data = {}
        mm = serializers.SolutionSerializer(data=data)
        assert mm.is_valid() is False

    def test_solution_serializer_with_invalid_data(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        data = {
            'solution': 'solution', 
            'user': user.id, 
            'task': task.id, 
            'submition_date': 2, 
            'language': 'Pytho'
            }
        mm = serializers.SolutionSerializer(data=data)
        assert mm.is_valid() is False
        assert 'submition_date' in mm.errors

    def test_solution_serializer_with_valid_data(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        data = {'solution': 'solution', 'user': user.id, 'task': task.id}
        mm = serializers.SolutionSerializer(data=data)
        assert mm.is_valid() is True

    def test_solution_create(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        data = {'solution': 'solution', 'user': user, 'task': task, 'submition_date':timezone.now()}
        solution = serializers.SolutionSerializer()
        solution = solution.create(validated_data=data)
        assert solution.solution == 'solution' 
        assert solution.user.id == 1
        assert solution.task.id == 1

    def test_solution_update(self):
        user = mixer.blend('catalog.User')
        user2 = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        data = {'solution': 'solution', 'user': user, 'task': task, 'submition_date':timezone.now()}
        solution_s = serializers.SolutionSerializer(data=data)
        solution = solution_s.create(validated_data=data)
        data = {'solution': 'solution2', 'user': user2}
        solution_s = solution_s.update(instance=solution, validated_data=data)
        assert solution.solution == 'solution2' 
        assert solution.user.id == 2
        assert solution.task.id == 1


@pytest.mark.django_db
class SubmitSolutionSerializerTest(TestCase):
    def test_solution_serializer_no_data(self):
        data = {}
        mm = serializers.SubmitSolutionSerializer(data=data)
        assert mm.is_valid() is False

    def test_solution_serializer_with_invalid_data(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        data = {'solution': 'solution','language': 'Pytho'}
        mm = serializers.SubmitSolutionSerializer(
            data=data, 
            context={'task': task, 'user': user}
            )
        assert mm.is_valid() is False
        assert 'language' in mm.errors

    def test_solution_serializer_with_valid_data(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        data = {'solution': 'solution', 'language': 'Python'}
        mm = serializers.SubmitSolutionSerializer(
            data=data, 
            context={'task': task, 'user': user, 'date': timezone.now()}
            )
        assert mm.is_valid() is True

    def test_solution_create(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        data = {'solution': 'solution', 'user': user, 'task': task, 'submition_date':timezone.now()}
        solution = serializers.SubmitSolutionSerializer(
            context={'task': task, 'user': user, 'date': timezone.now()}
            )
        solution = solution.create(validated_data=data)
        assert solution.solution == 'solution' 
        assert solution.user.id == 1
        assert solution.task.id == 1

    def test_solution_update(self):
        user = mixer.blend('catalog.User')
        user2 = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        data = {'solution': 'solution', 'user': user, 'task': task, 'submition_date':timezone.now()}
        solution_s = serializers.SubmitSolutionSerializer(
            data=data, 
            context={'task': task, 'user': user, 'date': timezone.now()}
            )
        solution = solution_s.create(validated_data=data)
        data = {'solution': 'solution2', 'user': user2}
        solution_s = solution_s.update(instance=solution, validated_data=data)
        assert solution.solution == 'solution2' 
        assert solution.user.id == 2
        assert solution.task.id == 1
