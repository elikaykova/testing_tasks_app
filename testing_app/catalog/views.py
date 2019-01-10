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
from django.utils import timezone
from django.http import HttpResponseRedirect
import pytz
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from catalog.models import Test, Task, SolutionInstance, User
from catalog.forms import SubmitForm, SubmitTaskForm, AddTestForm, AddTestFormSet
from catalog.additions import test_solution
from catalog.rq_test import rq_exec
from catalog.serializers import UserSerializer, SubmitUserSerializer, TaskSerializer, SubmitTaskSerializer, TestSerializer, SolutionInstanceSerializer, SubmitSolutionSerializer


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_users = User.objects.filter(is_staff=False).count()
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
            sol.submition_date = timezone.now()
            sol.save()

            rq_exec(sol.id)
            # sol.score = format(sol.score, '.2f')
            # updating user score
            # request.user.update_score(float(sol.score), sol.task)
            # request.user.save()
            # request.user = sol.user.save()
            return redirect('solutions')
        else:
            print(form.errors)
            return render(request, 'submitSolution.html', {'sol': sol})
    else:
        form = SubmitForm(user=request.user)
    return render(request, 'submitSolution.html', {'form': form, "task":task})

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




#### API_VIEWS


class UserListAPIView(ListCreateAPIView, LoginRequiredMixin):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = "catalog/user_list.html"
    serializer_class = SubmitUserSerializer

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response({'users': serializer.data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'serializer': serializer.data})
        serializer.save()
        # print(serializer)
        return redirect('API_users')


class UserDetailAPIView(RetrieveUpdateAPIView, LoginRequiredMixin):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = "catalog/user_detail.html"
    # authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = SubmitUserSerializer

    def get_object(self):
        user_id = self.kwargs["pk"]
        return get_object_or_404(User, id=user_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class MyTaskListAPIView(LoginRequiredMixin, ListCreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = "catalog/my_task_list.html"
    serializer_class = SubmitTaskSerializer

    def get(self, request, format=None):
        tasks = Task.objects.filter(publisher=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response({'tasks': serializer.data})

    def post(self, request):
        serializer = SubmitTaskSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'serializer': serializer.data})
        serializer.save()
        # print(serializer)
        return redirect('API_mytasks')


class TaskListAPIView(ListCreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = "catalog/task_list.html"
    serializer_class = SubmitTaskSerializer

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({'tasks': serializer.data})

    def post(self, request):
        serializer = SubmitTaskSerializer(data=request.data, context={'user': request.user})
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'serializer': serializer.data})
        serializer.save()
        # print(serializer)
        return redirect('API_tasks')

# class TaskDetailAPIView(generic.DetailView):
#     model = Task

class SolutionListAPIView(LoginRequiredMixin, ListAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = "catalog/solutioninstance_list.html"

    def get(self, request, format=None):
        solutions = SolutionInstance.objects.filter(user=request.user)
        serializer = SolutionInstanceSerializer(solutions, many=True)
        return Response({'solutions': serializer.data})


class SolutionDetailAPIView(LoginRequiredMixin, RetrieveAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = "catalog/solutioninstance_detail.html"
    # authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, pk, format=None):
        solution = SolutionInstance.objects.get(pk = pk)
        serializer = SolutionInstanceSerializer(solution)
        return Response({'solutioninstance': serializer.data})


class CreateSolutionAPIView(LoginRequiredMixin, ListCreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = "catalog/submitFormAPI.html"
    serializer_class = SubmitSolutionSerializer

    def get(self, request, pk):
        print('get')
        task = Task.objects.get(id=pk)
        solutions = SolutionInstance.objects.filter(task=task)
        task = TaskSerializer(task)
        serializer = SolutionInstanceSerializer(solutions, many=True)
        return Response({ 'task': task.data, 'solutions': serializer.data})

    def post(self, request, pk):
        print('post')
        task = Task.objects.get(id=pk)
        serializer = SubmitSolutionSerializer(data=request.data, 
            context={'task': task, 'user': request.user, 'date': timezone.now()})
        if not serializer.is_valid():
            return Response({'serializer': serializer.data, 'task': task})
        # request.user.update_score(float(sol.score), sol.task)
        # request.user.save()
        serializer.save()
        task = TaskSerializer(task)
        # print(serializer)
        return HttpResponseRedirect("")



# class CreateSolutionAPIView(LoginRequiredMixin, CreateAPIView):
#     # renderer_classes = [TemplateHTMLRenderer]
#     # template_name = "catalog/submitFormAPI.html"
#     serializer_class = SubmitSolutionSerializer

#     def get(self, request, pk):
#         print('get')
#         task = Task.objects.get(id=pk)
#         task = TaskSerializer(task)
#         return Response({ 'task': task.data})

#     def post(self, request, pk):
#         print('post')
#         task = Task.objects.get(id=pk)
#         serializer = SubmitSolutionSerializer(data=request.data, 
#             context={'task': task, 'user': request.user, 'date': timezone.now()})
#         if not serializer.is_valid():
#             return Response({'serializer': serializer.data, 'task': task})
#         # request.user.update_score(float(sol.score), sol.task)
#         # request.user.save()
#         serializer.save()
#         return redirect('API_solutions')

### CreateSolutionAPIView as Form
# class CreateSolutionAPIView(LoginRequiredMixin, CreateAPIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = "catalog/submitFormAPI.html"
#     # authentication_classes = (authentication.TokenAuthentication,)
#     def get(self, request, pk):
#         print('get')
#         task = Task.objects.get(id=pk)
#         solution = SolutionInstanceSerializer()
#         return Response({'serializer': solution, 'task': task})

#     def post(self, request, pk):
#         print('post')
#         task = Task.objects.get(id=pk)
#         serializer = SolutionInstanceSerializer(data=request.data)
#         serializer.task = task
#         print(':(')
#         if not serializer.is_valid():
#             # print(serializer.errors)
#             return Response({'serializer': serializer, 'task': task})
#         print(':(:(')
#         serializer.save()
#         return redirect('API_solutions')

### TaskDetailAPI without PUT
# class TaskDetailAPI(LoginRequiredMixin, APIView):
#     # renderer_classes = [TemplateHTMLRenderer]
#     # template_name = 'catalog/updateTaskFormAPI.html'

#     def get(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         serializer = TaskSerializer(task)
#         return Response({'serializer': serializer.data})


class SubmitTaskAPI(LoginRequiredMixin, CreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'catalog/submitTaskFormAPI.html'
    serializer_class = TaskSerializer

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'serializer': serializer.data})
        serializer.save()
        # print(serializer)
        return redirect('API_tasks')


class TaskDetailAPI(LoginRequiredMixin, RetrieveUpdateAPIView):
    serializer_class = TaskSerializer

    def get_object(self):
        task_id = self.kwargs["pk"]
        return get_object_or_404(Task, id=task_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class EditTaskAPI(LoginRequiredMixin, RetrieveUpdateAPIView):
    serializer_class = TaskSerializer

    def get_object(self):
        task_id = self.kwargs["pk"]
        return get_object_or_404(Task, id=task_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



### EditTaskAPI as Form
# class EditTaskAPI(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'catalog/updateTaskFormAPI.html'

#     def get(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         serializer = TaskSerializer(task)
#         return Response({'serializer': serializer})

#     def post(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if not serializer.is_valid():
#             print(serializer.errors)
#             return Response({'serializer': serializer})
#         serializer.save()
#         print(serializer)
#         return redirect('API_tasks')


class TestViewAPI(LoginRequiredMixin, APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'catalog/updateTestsFormAPI.html'
    serializer_class = TestSerializer

    def get(self, request, format=None):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response({'tests': serializer.data})

    def post(self, request):
        tests = Test.objects.all()
        serializer = TestSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'serializer': serializer})
        serializer.save()
        print(serializer)
        return redirect('API_Tests')