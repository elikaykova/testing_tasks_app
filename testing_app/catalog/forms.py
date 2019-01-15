from django import forms
from catalog.models import Test, Task, SolutionInstance, User
from django.forms import modelformset_factory, inlineformset_factory


# class SubmitSolutionForm(forms.ModelForm):
#     task = forms.ModelChoiceField(label='Task', queryset=Task.objects.all())
#     solution = forms.CharField(label='Solution', max_length=1000)

#     class Meta:
#         model = SolutionInstance
#         fields = ('solution',)

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super(SubmitSolutionForm, self).__init__(*args, **kwargs)

class SubmitForm(forms.ModelForm):
    solution = forms.CharField(widget=forms.Textarea)
    # solution.widget.attrs.update({'id' : 'solution_id'})

    # def sub(self):
    #     sol.solution = form.cleaned_data['solution']
    #     sol.user = request.user

    class Meta:
        model = SolutionInstance
        fields = ['solution',]
        labels = {'solution': 'Your solution'}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SubmitForm, self).__init__(*args, **kwargs)
        

class SubmitTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'text',]
        labels = {'task_name': 'Title', 'text': 'Task'}

class AddTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_input', 'test_output',]
        labels = {'test_input': ' Input', 'test_output': 'Output'}

AddTestFormSet = inlineformset_factory(Task, Test, extra=3, fields=('test_input', 'test_output'), can_delete=True)