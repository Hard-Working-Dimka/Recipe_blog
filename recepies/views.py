from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


def show_index(request):
    return render(request, 'index.html')


def show_auth(request):
    return render(request, '')


def show_card(request):
    return render(request, 'card.html')

@login_required
def show_lk(request):
    user_id = request.user.id
    print(user_id)
    #TODO: id юзера есть, кидаем в контекст все его данные
    return render(request, 'registration/profile.html')


def show_order(request):
    return render(request, 'order.html')


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

