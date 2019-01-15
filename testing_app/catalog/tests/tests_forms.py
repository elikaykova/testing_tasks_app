from django.test import TestCase
from django.utils import timezone
import datetime

# Create your tests here.
from catalog.models import User, Task
from catalog.forms import SubmitForm


# class SubmitFormTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         User.objects.create(username='Bobby', first_name='Big', last_name='Bob', password='123')
#         user = User.objects.get(id=1)
#         Task.objects.create(task_name='new_task', text='task_text', publisher=user)

#     def test_submit_solution_form_task_label(self):
#         form = SubmitForm()
#         self.assertTrue(form.fields['task'].label == None or form.fields['task'].label == 'task')

#     def test_submit_solution_form_date_field(self):
#         form = SubmitForm()
#         self.assertTrue(form.fields['submition_date'].label == 'submition date')

#     def test_submit_solution_form_date_today(self):
#         date = datetime.date.today()
#         form = SubmitForm(data={'submition_date': date})
#         self.assertTrue(form.is_valid())
#         