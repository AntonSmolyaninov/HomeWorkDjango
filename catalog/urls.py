from django.urls import path
from catalog.views import (
    HomePageView,
    ContactPageView,
    ProductDetailView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("contacts/", ContactPageView.as_view(), name="contacts"),

    path('product/create/', ProductCreateView.as_view(), name='product_create'),

    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('product/', ProductListView.as_view(), name='product_list'),
]
