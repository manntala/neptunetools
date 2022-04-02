from django.urls import path, include
from .views import PostView, home, uploadcsv, gettoken, send, display, displayid, activate, deactivate, resetorder, cancelorder
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', home, name='home'),
    path('api-auth/', include('rest_framework.urls')),
    path('postview', PostView.as_view(), name='PostView'),
    path('api/token/', obtain_auth_token, name='obtain-token'),    

    path('uploadcsv/', uploadcsv, name='uploadcsv'),
    path('resetorder/', resetorder, name='resetorder'),
    path('cancelorder/', cancelorder, name='cancelorder'),
    path('gettoken/', gettoken, name='gettoken'),
    path('activate/<str:id>', activate, name='activate'),
    path('deactivate/<str:id>', deactivate, name='deactivate'),

    # orders
    path('send/', send, name='send'),
    path('display/', display, name='display'),
    path('displayid/<str:id>', displayid, name='displayid'),

]
