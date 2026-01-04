from catalog import views
from catalog.apps import CatalogConfig
from django.urls import path


app_name = CatalogConfig.name

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]
