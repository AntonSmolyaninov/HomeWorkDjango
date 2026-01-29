from django.urls import path
from .views import HomePageView, ContactPageView, ProductDetailView

app_name = "catalog"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contacts/', ContactPageView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]