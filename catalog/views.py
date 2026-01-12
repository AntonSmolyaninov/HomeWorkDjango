from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from catalog.models import Product, ContactInfo


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Вывод в консоль
    print("Последние 5 продуктов:")
    for product in latest_products:
        print(f"{product.name_product} - {product.created_at}")

    return render(request, "home.html", {"latest_products": latest_products})


def contacts(request):
    contacts = ContactInfo.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts})
