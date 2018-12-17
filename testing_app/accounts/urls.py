from django.conf.urls import url
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.urls import include

from . import views


app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
]