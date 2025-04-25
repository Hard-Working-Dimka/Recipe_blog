from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.forms import AuthenticationForm

from recepies.forms import RegisterUserForm
from recepies.models import Recipe


#
def show_index(request):
    return render(request, 'index.html')


def show_card(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'card.html', {'recipe': recipe})


@login_required
def show_lk(request):
    user_id = request.user.id
    print(user_id)
    # TODO: id юзера есть, кидаем в контекст все его данные
    return render(request, 'registration/profile.html')


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
