from django.urls import path, include
from .views import catalogupdate, catalogdisplay, viewproductbyid, resetproduct, uploadproductcatalog, catalogadd, uploadaddcatalog, resetproductdisplay, resetaddproduct
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path('catalogupdate', catalogupdate, name='catalogupdate'),
    path('catalogdisplay/', catalogdisplay, name='catalogdisplay'),
    path('catalogadd/', catalogadd, name='catalogadd'),
    path('uploadaddcatalog/', uploadaddcatalog, name='uploadaddcatalog'),

    path('viewproductbyid', viewproductbyid, name='viewproductbyid'),
    path('resetproduct', resetproduct, name='resetproduct'),
    path('resetaddproduct', resetaddproduct, name='resetaddproduct'),
    
    path('resetproductdisplay', resetproductdisplay, name='resetproductdisplay'),
    
    path('uploadproductcatalog', uploadproductcatalog, name='uploadproductcatalog'),
]
