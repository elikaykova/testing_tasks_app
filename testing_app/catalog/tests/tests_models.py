from django.test import TestCase

# Create your tests here.

from catalog.models import User, Task

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='Bobby', first_name='Big', last_name='Bob', password='123')
        user = User.objects.get(id=1)
        Task.objects.create(task_name='new_task', text='task_text', publisher=user)

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'username')

    def test_user_progress_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('user_progress').verbose_name
        self.assertEquals(field_label, 'user progress')

    def test_user_progress_value(self):
        user = User.objects.get(id=1)
        self.assertEquals(user.user_progress, 0)

    def test_get_absolute_url(self):
        user = User.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(user.get_absolute_url(), '/catalog/user/1')

    def test__str__(self):
        user = User.objects.get(id=1)
        expected_object_name = f'{user.id}: {user.username}'
        self.assertEquals(expected_object_name, str(user))
        
    def test_update_score(self):
        user = User.objects.get(id=1)
        task = Task.objects.get(id=1)
        user.update_score(0.65, task)
        self.assertEquals(user.user_progress, 0.65)

    ### TO DO
    # def test_get_tasks(self):
    #     user = User.objects.get(id=1)
    #     tasks = user.get_tasks
