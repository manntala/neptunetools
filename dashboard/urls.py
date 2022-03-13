from django.urls import path, include
from .views import dashboard
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', dashboard, name='dashboard'),

]
