from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('solutions/', views.SolutionListView.as_view(), name='solutions'),
    path('solution/<int:pk>', views.SolutionDetailView.as_view(), name='solution-detail'),
]
