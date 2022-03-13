from django.urls import path, include
from .views import registration_view, login_view, logout_view, account_view, update_view

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('account/', account_view, name='account'),  
    path('update/', update_view, name='update'),  
]
