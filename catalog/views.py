from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from catalog.models import Product, ContactInfo

class HomePageView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "latest_products"

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')

class ContactPageView(ListView):
    model = ContactInfo
    template_name = "contacts.html"
    context_object_name = "contacts"

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
