from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

from catalog.models import Test, Task, SolutionInstance, User
from catalog.forms import SubmitForm, SubmitTaskForm
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
            sol.score = test_solution(sol.solution, sol.task)
            sol.submition_date = date.today()
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
    if request.method == 'POST':
        form = SubmitTaskForm(request.POST)
        if form.is_valid():
            sol = form.save(commit=False)
            sol.release_date = date.today()
            sol = sol.save()
            return redirect('tasks')
        else:
            print(form.errors)
            return render(request, 'submitTask.html', {'sol': sol})

    else:
        form = SubmitTaskForm()
    return render(request, 'submitTask.html',  {'form': form})