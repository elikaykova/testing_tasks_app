from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>/submitSolution/', views.submit, name='task-detail'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail-no-user'),
    path('solutions/', views.SolutionListView.as_view(), name='solutions'),
    path('solution/<int:pk>', views.SolutionDetailView.as_view(), name='solution-detail'),
    path('submitSolution/', views.submitSolution, name='submitSolution'),
    path('submitTask/', views.submitTask, name='submitTask'),
]
