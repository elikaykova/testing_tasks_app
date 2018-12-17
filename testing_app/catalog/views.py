from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, datetime
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory

from catalog.models import Test, Task, SolutionInstance, User
from catalog.forms import SubmitForm, SubmitTaskForm, AddTestForm
from catalog.additions import test_solution

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_users = User.objects.all().count()
    num_solutions = SolutionInstance.objects.all().count()

    num_tasks = Task.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_users': num_users,
        'num_tasks': num_tasks,
        'num_solutions': num_solutions,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class UserListView(LoginRequiredMixin, generic.ListView):
    model = User

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User

class TaskListView(generic.ListView):
    model = Task

class TaskDetailView(generic.DetailView):
    model = Task

class SolutionListView(LoginRequiredMixin, generic.ListView):
    model = SolutionInstance

class SolutionDetailView(LoginRequiredMixin, generic.DetailView):
    model = SolutionInstance

@login_required
def submitSolution(request):
    if request.method == 'POST':
        form = SubmitSolutionForm(request.POST, user=request.user)
        if form.is_valid():
            sol = form.save(commit=False)
            sol.solution = form.cleaned_data['solution']
            sol.task = form.cleaned_data['task']
            sol.user = request.user
            # form.user = User.objects.get(user)
            sol = sol.save()
            return redirect('solutions')
        else:
            print(form.errors)
            return render(request, 'submitSolution.html', {'sol': sol})

    else:
        form = SubmitSolutionForm(user=request.user)
    return render(request, 'submitSolution.html',  {'form': form})

@login_required
def submit(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = SubmitForm(request.POST, user=request.user)
        if form.is_valid():
            sol = form.save(commit=False)
            sol.solution = form.cleaned_data['solution']
            sol.task = task
            sol.user = request.user
            sol.score, sol.reports = test_solution(sol.solution, sol.task)
            sol.score = format(sol.score, '.2f')
            sol.submition_date = datetime.now()
            request.user.update_score(float(sol.score))
            request.user.save()
            # request.user = sol.user.save()
            sol = sol.save()
            return redirect('solutions')
        else:
            print(form.errors)
            return render(request, 'submitSolution.html', {'sol': sol})
    else:
        form = SubmitForm(user=request.user)
    return render(request, 'submitSolution.html',  {'form': form, "task":task})

@login_required
def submitTask(request):
    AddTestFormSet = modelformset_factory(Test, extra=1, fields=('test_input', 'test_output',))

    if request.method == 'POST':
        form = SubmitTaskForm(request.POST)
        formset = AddTestFormSet(request.POST, queryset=Test.objects.none())

        if all([form.is_valid(), formset.is_valid()]):
            sol = form.save(commit=False)
            sol.release_date = date.today()
            sol = sol.save()
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.cleaned_data:
                    instance.save()
            return redirect('tasks')

        else:
            print(form.errors)
            return render(request, 'submitTask.html', {'sol': sol, 'instances': instances})

    else:
        form = SubmitTaskForm()
        formset = AddTestFormSet(queryset=Test.objects.none())
    return render(request, 'submitTask.html',  {'form': form, 'formset':formset})

    # AddTestFormSet = formset_factory(AddTestForm, extra=2)

    # if request.method == 'POST':
    #     data={
    #             'form-TOTAL_FORMS': 1,
    #             'form-INITIAL_FORMS': 0,
    #             'form-0-test_input': "",
    #             'form-0-test_output': "",
    #             'form-1-test_input': "",
    #             'form-1-test_output': "",
    #         },
    #     form = SubmitTaskForm(request.POST)
    #     formset = AddTestFormSet(request.POST, data)

    #     # AddTestFormSet = inlineformset_factory(Task, Test, fields=('test_input',))
    #     # form = SubmitTaskForm(request.POST)
    #     # formset = AddTestFormSet(instance=form)

    #     if all([form.is_valid(), formset.is_valid()]):
    #         sol = form.save(commit=False)
    #         sol.release_date = date.today()
    #         sol = sol.save()
    #         for inline_form in formset:
    #             if inline_form.cleaned_data:
    #                 # test = inline_form.save(commit=False)
    #                 # test.save()
    #                 inline_form.save()
    #         return redirect('tasks')

    #     else:
    #         print(form.errors)
    #         return render(request, 'submitTask.html', {'sol': sol})

    # else:
    #     form = SubmitTaskForm()
    #     formset = AddTestFormSet()
    # return render(request, 'submitTask.html',  {'form': form, 'formset':formset})