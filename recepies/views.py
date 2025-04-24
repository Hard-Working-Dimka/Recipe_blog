from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from recepies.forms import RegisterUserForm


#
def show_index(request):
    return render(request, 'index.html')
#
#
# def show_auth(request):
#     return render(request, '')
#
#
# def show_card(request):
#     return render(request, 'card.html')

@login_required
def show_lk(request):
    user_id = request.user.id
    print(user_id)
    #TODO: id юзера есть, кидаем в контекст все его данные
    return render(request, 'registration/profile.html')


#
# def show_order(request):
#     return render(request, 'order.html')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return reverse_lazy('profile')


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/profile.html')
    else:
        form = RegisterUserForm()
    return render(request, 'registration/registration.html', {'form': form})

