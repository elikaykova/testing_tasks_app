from django.shortcuts import render
from catalog.models import Test, Task, SolutionInstance, User
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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