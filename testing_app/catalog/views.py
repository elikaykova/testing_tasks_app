from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, datetime
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView


from catalog.models import Test, Task, SolutionInstance, User
from catalog.forms import SubmitForm, SubmitTaskForm, AddTestForm, AddTestFormSet
from catalog.additions import test_solution
from catalog.rq_test import rq_exec

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

    ordering = ['-user_progress']

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User

class MyTaskListView(LoginRequiredMixin, generic.ListView):
    template_name = "catalog/my_task_list.html"
    model = Task

class TaskListView(generic.ListView):
    model = Task

class TaskDetailView(generic.DetailView):
    model = Task

class SolutionListView(LoginRequiredMixin, generic.ListView):
    model = SolutionInstance

    ordering = ['-submition_date']

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
            sol.done = False
            sol.submition_date = datetime.now()
            sol.save()

            rq_exec(sol.id)
            # sol.score = format(sol.score, '.2f')
            # updating user score
            request.user.update_score(float(sol.score), sol.task)
            request.user.save()
            # request.user = sol.user.save()
            sol.save()
            return redirect('solutions')
        else:
            print(form.errors)
            return render(request, 'submitSolution.html', {'sol': sol})
    else:
        form = SubmitForm(user=request.user)
    return render(request, 'submitSolution.html',  {'form': form, "task":task})


@login_required
def submitTask(request):

    form = SubmitTaskForm()
    formset = AddTestFormSet(queryset=Test.objects.none(), instance=Task())

    if request.method == 'POST':
        form = SubmitTaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.release_date = date.today()
            task.publisher = request.user
            task = form.save()
            formset = AddTestFormSet(request.POST, request.FILES, instance=task)

            if formset.is_valid():
                formset.save()
                # for instance in instances:
                #     instance.save()
                return redirect('tasks')

        else:
            print(form.errors)
            print(formset.errors)
            return render(request, 'submitTask.html', {'form': form, 'formset':formset})

    else:
        form = SubmitTaskForm()
        formset = AddTestFormSet(queryset=Test.objects.none(), instance=Task())
    return render(request, 'submitTask.html',  {'form': form, 'formset':formset})



# class editTask(UpdateView):
#     model = Task
#     fields = ['task_name', 'text']

@login_required
def editTask(request, pk=None):
    task = get_object_or_404(Task, pk=pk)

    form = SubmitTaskForm(request.POST or None, instance=task)
    if form.is_valid():
        task = form.save()
        return redirect('tasks')

    return render(request, 'editTask.html',  {'form': form, 'task': task, })

@login_required
def deleteTask(request, pk=None):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'deleteTask.html',  {'task': task, })


@login_required
def editTests(request, pk=None):
    task = get_object_or_404(Task, pk=pk)

    formset = AddTestFormSet(request.POST or None, instance=task)
    if formset.is_valid():
        task = formset.save()
        return redirect('tasks')

    return render(request, 'editTests.html',  {'formset': formset, 'task': task, })
