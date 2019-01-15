from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('mytasks/', views.MyTaskListView.as_view(), name='mytasks'),
    # path('task/<int:pk>/submitSolution/', views.submit, name='task-detail'),
    # path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail-no-user'),
    path('task/<int:pk>', views.submit, name='task-detail'),
    path('solutions/', views.SolutionListView.as_view(), name='solutions'),
    path('solution/<int:pk>', views.SolutionDetailView.as_view(), name='solution-detail'),
    path('submitSolution/', views.submitSolution, name='submitSolution'),
    path('submitTask/', views.submitTask, name='submitTask'),
    path('editTask/<int:pk>', views.editTask, name='editTask'),
    path('deleteTask/<int:pk>', views.deleteTask, name='deleteTask'),
    path('editTests/<int:pk>', views.editTests, name='editTests'),

    path('API/users/', views.UserListAPIView.as_view(), name='API_users'),
    path('API/user/<int:pk>', views.UserDetailAPIView.as_view(), name='API_user-detail'),
    path('API/tasks/', views.TaskListAPIView.as_view(), name='API_tasks'),
    path('API/mytasks/', views.MyTaskListAPIView.as_view(), name='API_mytasks'),
    path('API/task/<int:pk>/solutions/', views.CreateSolutionAPIView.as_view(), name='API_submitSolution-detail'),
    path('API/task/<int:pk>', views.TaskDetailAPI.as_view(), name='API_task-detail'),
    path('API/solutions/', views.SolutionListAPIView.as_view(), name='API_solutions'),
    path('API/solution/<int:pk>', views.SolutionDetailAPIView.as_view(), name='API_solution-detail'),
    path('API/submitTask/', views.SubmitTaskAPI.as_view(), name='API_submitTask'),
    path('API/editTask/<int:pk>', views.EditTaskAPI.as_view(), name='API_editTask'),
    path('API/Tests/', views.TestViewAPI.as_view(), name='API_Tests'),
    # path('API/tokens', obtain_auth_token, name='tokens'),
    path('API/rest_auth/', include('rest_auth.urls')),
    path('API/rest_auth_2/', include('rest_auth.registration.urls')),
    # path('API/API_users/', include('users.urls')),
    # path('API/jwt_tokens', refresh_jwt_token, name='jwt_tokens'),
]
