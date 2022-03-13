from django.urls import path, include
from .views import storeupdate, storeview
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [

    path('storeupdate/', storeupdate, name='storeupdate'),
    path('storeview/', storeview, name='storeview'),
    

]
