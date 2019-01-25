import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from django.test import TestCase
from django.utils import timezone
import datetime

# Create your tests here.
from catalog.models import User, Task
from catalog import forms


@pytest.mark.django_db
class SubmitFormTest(TestCase):
    def test_form_no_data(self):
        user = mixer.blend('catalog.User')
        form = forms.SubmitForm(data={}, user=user)
        assert form.is_valid() is False, 'Should be invalid if no data is given'

    def test_form_with_data(self):
        user = mixer.blend('catalog.User')
        data = {'language': 'Python', 'solution': 'Hello World!'}
        form = forms.SubmitForm(data=data, user=user)
        assert form.is_valid() is True, 'Should be valid when data is given'

    def test_form_with_wrong_data(self):
        user = mixer.blend('catalog.User')
        data = {'language': 'Python_no', 'solution': 'Hello World!'}
        form = forms.SubmitForm(data=data, user=user)
        assert form.is_valid() is False, 'Should be invalid when language is not from the list of languages'
        assert 'language' in form.errors, 'Should not accept language which is not from the list of languages'

@pytest.mark.django_db
class SubmitTaskFormTest(TestCase):
    def test_form_no_data(self):
        user = mixer.blend('catalog.User')
        form = forms.SubmitTaskForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is given'

    def test_form_with_data(self):
        user = mixer.blend('catalog.User')
        data = {'task_name': 'new_task', 'text': 'Hello World!'}
        form = forms.SubmitTaskForm(data=data)
        assert form.is_valid() is True, 'Should be valid when data is given'


@pytest.mark.django_db
class AddTestFormTest(TestCase):
    def test_form_no_data(self):
        user = mixer.blend('catalog.User')
        form = forms.AddTestForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is given'

    def test_form_with_data(self):
        user = mixer.blend('catalog.User')
        data = {'test_input': 'test', 'test_output': 'Hello World!'}
        form = forms.AddTestForm(data=data)
        assert form.is_valid() is True, 'Should be valid when data is given'