from django.shortcuts import render, get_object_or_404
from .models import Recipe

def show_index(request):
    return render(request, 'index.html')


def show_auth(request):
    return render(request, 'auth.html')


def show_card(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'card.html', {'recipe': recipe})


def show_lk(request):
    return render(request, 'lk.html')


def show_order(request):
    return render(request, 'order.html')


def show_registration(request):
    return render(request, 'registration.html')
