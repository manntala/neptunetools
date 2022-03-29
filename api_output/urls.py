from django.urls import path, include
from .views import api_reviews, api_reviews2, submit_review, reviewAPI, buy
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', api_reviews, name='api_reviews'),
    path('api_reviews2', api_reviews2, name='api_reviews2'),
    path('submit_review', submit_review, name='submit_review'),
    path('reviewAPI', reviewAPI, name='reviewAPI'),
    path('buy', buy, name='buy'),
]
