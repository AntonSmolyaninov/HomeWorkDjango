from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse


def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name', 'Гость')
        message = request.POST.get('message', '')
        if not message.strip():
            return render(request, 'contacts.html', {'error': 'Введите сообщение!'})
        return HttpResponse(f"Спасибо. {name}! Сообщение доставленно.")

    success = request.GET.get('success') == '1'
    return render(request, 'contacts.html', {'success': success})
