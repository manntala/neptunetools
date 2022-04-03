from django.urls import path, include
from .views import removetoken, addtoken, storeview, resetstore, resetaddstore, resetviewstore
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [

    path('removetoken/', removetoken, name='removetoken'),
    path('addtoken/', addtoken, name='addtoken'),
    path('storeview/', storeview, name='storeview'),

    path('resetstore/', resetstore, name='resetstore'),
    path('resetaddstore/', resetaddstore, name='resetaddstore'),
    path('resetviewstore/', resetviewstore, name='resetviewstore'),
]
