from django.shortcuts import render


def show_index(request):
    return render(request, 'index.html')


def show_auth(request):
    return render(request, 'auth.html')


def show_card(request):
    return render(request, 'card.html')


def show_lk(request):
    return render(request, 'lk.html')


def show_order(request):
    return render(request, 'order.html')


def show_registration(request):
    return render(request, 'registration.html')
