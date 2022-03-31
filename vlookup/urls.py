from django.urls import path, include
from .views import uploadcatalog, uploadreviews, vlookup, view_products, autoretrieve, resetform, shopifyscraper, resetscraperform, resetautoretrieve
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('uploadcatalog/', uploadcatalog, name='uploadcatalog'),
    path('uploadreviews/', uploadreviews, name='uploadreviews'),
    path('vlookup/', vlookup, name='vlookup'),
    path('autoretrieve/', autoretrieve, name='autoretrieve'),
    path('resetform/', resetform, name='resetform'),
    path('resetscraperform/', resetscraperform, name='resetscraperform'),
    path('resetautoretrieve/', resetautoretrieve, name='resetautoretrieve'),

    # path('<str:filepath>/', download_file, name='download_file'),
    path('view_products/', view_products, name='view-products'),
    path('shopifyscraper/', shopifyscraper, name='shopifyscraper'),

]
