from django.test import TestCase
import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
# Create your tests here.

from catalog.models import User, Task


@pytest.mark.django_db
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='Bobby', first_name='Big', last_name='Bob', password='123')
        user = User.objects.get(id=1)
        Task.objects.create(task_name='new_task', text='task_text', publisher=user)

    def test_init(self):
        user = mixer.blend('catalog.User')
        assert obj.pk == 2, 'Should save a User instance'

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        assert field_label == 'first name', 'Correct field saving'

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        assert field_label == 'username', 'Correct field saving'

    def test_user_progress_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('user_progress').verbose_name
        assert field_label == 'user progress', 'Correct field saving'

    def test_user_progress_value(self):
        user = User.objects.get(id=1)
        assert user.user_progress == 0, 'New user should be with progress == 0'

    def test_get_absolute_url(self):
        user = User.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        assert user.get_absolute_url() == '/catalog/user/1', 'Should return correct url to the instance'

    def test__str__(self):
        user = User.objects.get(id=1)
        expected_object_name = f'1: Bobby'
        assert expected_object_name == str(user), 'Should return string representation of a user'
        
    def test_update_score(self):
        user = User.objects.get(id=1)
        task = Task.objects.get(id=1)
        user.update_score(0.65, task)
        assert user.user_progress == 0.65, 'Should update user score with 0.65'

    def test_get_all_solutions(self):
        user = User.objects.get(id=1)
        user2 = mixer.blend('catalog.User')
        solution1 = mixer.blend('catalog.Solution', user=user)
        solution2 = mixer.blend('catalog.Solution', user=user)
        solution3 = mixer.blend('catalog.Solution', user=user)
        solution4 = mixer.blend('catalog.Solution', user=user2)
        solutions = user.get_all_solutions()
        assert len(solutions) == 3, 'Should return all solutions of the user'

    def test_get_all_tasks(self):
        user = User.objects.get(id=1)
        user2 = mixer.blend('catalog.User')
        task_1 = mixer.blend('catalog.Task')
        task_2 = mixer.blend('catalog.Task')
        task_3 = mixer.blend('catalog.Task')
        task_4 = mixer.blend('catalog.Task')
        solution1 = mixer.blend('catalog.Solution', user=user, task=task_2)
        solution2 = mixer.blend('catalog.Solution', user=user, task=task_4)
        solution3 = mixer.blend('catalog.Solution', user=user, task=task_4)
        tasks = user.get_all_tasks()
        assert len(tasks) == 2, 'Should return all tasks that user have solution for'

    def test_get_max_score_for_task(self):
        user = User.objects.get(id=1)
        task = Task.objects.get(id=1)
        solution1 = mixer.blend('catalog.Solution', user=user, task=task, score=0.98)
        solution2 = mixer.blend('catalog.Solution', user=user, task=task, score=0.00)
        solution3 = mixer.blend('catalog.Solution', user=user, task=task, score=0.52)
        max_score = user.get_max_score_for_task(task)
        assert max_score == 0.98, 'Should return the maximum score for this task'

    def tearDown(self):
        pass


@pytest.mark.django_db
class TaskModelTest(TestCase):
    def test_init(self):
        task = mixer.blend('catalog.Task')
        assert task.pk == 1, 'Should save a Task instance'

    def test__str__(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task', task_name='new_task', publisher=user)
        expected_object_name = '1: new_task'
        assert expected_object_name == str(task), 'Should return string representation of a task'

    def test_get_absolute_url(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        assert task.get_absolute_url() == '/catalog/task/1', 'Should return correct url to the instance'


@pytest.mark.django_db
class TestModelTest(TestCase):
    def test_init(self):
        test = mixer.blend('catalog.Test')
        assert test.pk == 1, 'Should save a Test instance'

    def test__str__(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task', task_name='new_task', publisher=user)
        test = mixer.blend('catalog.Test', task=task)
        expected_object_name = 'Test for new_task'
        assert expected_object_name == str(test), 'Should return string representation of a test'


@pytest.mark.django_db
class SolutionModelTest(TestCase):
    def test_init(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task', publisher=user)
        solution = mixer.blend('catalog.Solution', user=user, task=task)
        assert solution.pk == 1, 'Should save a Solution instance'

    def test__str__(self):
        user = mixer.blend('catalog.User', username='new_user')
        task = mixer.blend('catalog.Task', publisher=user, task_name='new_task')
        solution = mixer.blend('catalog.Solution', user=user, task=task, language='Python')
        expected_object_name = 'Solution for task: "new_task", by new_user, written on Python, with score: 0'
        assert expected_object_name == str(solution), 'Should return string representation of a solution'

    def test_get_absolute_url(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        solution = mixer.blend('catalog.Solution', user=user, task=task)
        assert solution.get_absolute_url() == '/catalog/solution/1', 'Should return correct url to the instance'
