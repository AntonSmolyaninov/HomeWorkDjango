from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from catalog.models import Product, ContactInfo
from django.shortcuts import get_object_or_404


def home(request):
    all_products = Product.objects.all().order_by('-created_at')
    return render(request, "home.html", {"latest_products": all_products})


def contacts(request):
    contacts: QuerySet[ContactInfo, ContactInfo] = ContactInfo.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})
