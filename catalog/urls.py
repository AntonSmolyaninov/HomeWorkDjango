from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import (
    HomePageView,
    ContactPageView,
    ProductDetailView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView, CategoryProductsView, unpublish_product, CategoryListView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("contacts/", ContactPageView.as_view(), name="contacts"),

    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),

    path('product/create/', ProductCreateView.as_view(), name='product_create'),

    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('product/<int:pk>/unpublish/', unpublish_product, name='unpublish_product'),

    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),

    path('product/', ProductListView.as_view(), name='product_list'),
]
