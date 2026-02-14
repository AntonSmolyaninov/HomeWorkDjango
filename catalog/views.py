from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from catalog.forms import ProductForm
from catalog.models import ContactInfo, Product


class HomePageView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "latest_products"

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")


class ContactPageView(ListView):
    model = ContactInfo
    template_name = "contacts.html"
    context_object_name = "contacts"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy('catalog:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy('catalog:product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy('catalog:product_list')