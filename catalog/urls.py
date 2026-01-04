from catalog.apps import CatalogConfig
from django.urls import path
from catalog.views import home

app_name = CatalogConfig.name

urlpatterns = [
    path("", home)
]
