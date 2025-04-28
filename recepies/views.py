import random

from django.contrib.auth import login


from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Order, TypeOfSubscription, FoodIntake, Allergy, TypeOfMenu

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.generic import UpdateView

from recepies.forms import RegisterUserForm, ProfileUserForm
from recepies.models import Recipe

from django.contrib.auth.decorators import login_required


def show_index(request):
    recipes = list(Recipe.objects.all())
    random_recipes = random.sample(recipes, 3) if len(recipes) >= 3 else recipes
    return render(request, 'index.html', {'random_recipes': random_recipes})


def show_card(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, "card.html", {"recipe": recipe})


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"
    extra_context = {"title": "Авторизация"}

    def get_success_url(self):
        return reverse_lazy("profile")


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user, backend="recepies.EmailAuthBackend.EmailAuthBackend")
            return redirect("profile")
    else:
        form = RegisterUserForm()
    return render(request, "registration/registration.html", {"form": form})


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        user = self.request.user
        self.object = user  # Явно устанавливаем self.object
        return user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        form = self.form_class(initial={
            'email': user.email, 
            'username': user.username, 
            'first_name': user.first_name,
            'avatar': user.avatar
        })
        form2 = PasswordChangeForm(user)
        context = self.get_context_data(**kwargs)
        context.update({
            'orders': Order.objects.filter(profile=user),
            'avatar': user.avatar,
            'user': user,
            'form1': form,
            'form2': form2,
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        form = self.form_class(request.POST, request.FILES, instance=user)

        form2 = PasswordChangeForm(user)

        if 'form1' in request.POST:
            form = self.form_class(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен.')
                return redirect(self.success_url)

        elif 'form2' in request.POST:
            form2 = PasswordChangeForm(user, request.POST)
            if form2.is_valid():
                user = form2.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменен.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки при смене пароля.')

    # Если формы не валидны или ни одна не отправлена
        context = self.get_context_data(**kwargs)
        context.update({
        'orders': Order.objects.filter(profile=user),
        'avatar': user.avatar,
        'user': user,
        'form1': form,
        'form2': form2,
        })
        return self.render_to_response(context)


@login_required
def show_order(request):
    current_user = request.user
    if request.method == "POST":
        try:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Пожалуйста, войдите в систему"}, status=401)
            profile = current_user

            # Маппинги
            MENU_MAPPING = {
                "classic": "Классическое",
                "low": "Низкоуглеводное",
                "veg": "Вегетарианское",
                "keto": "Кето",
            }
            SUBSCRIPTION_MAPPING = {
                "0": ("1 мес.", 1000),
                "1": ("3 мес.", 2700),
                "2": ("6 мес.", 5000),
                "3": ("12 мес.", 9000),
            }
            ALLERGY_MAPPING = {
                "meat": "Мясо",
                "honey": "Продукты пчеловодства",
                "fish": "Рыба и морепродукты",
                "grains": "Зерновые",
                "nuts": "Орехи и бобовые",
                "dairy": "Молочные продукты",
            }

            # Меню
            menu_code = request.POST.get("foodtype")
            menu_name = MENU_MAPPING.get(menu_code)
            if not menu_name:
                return JsonResponse({"error": "Неверный тип меню"}, status=400)
            menu_obj = TypeOfMenu.objects.get(name=menu_name)

            # Подписка
            sub_code = request.POST.get("subscription_duration")
            sub_data = SUBSCRIPTION_MAPPING.get(sub_code)
            if not sub_data:
                return JsonResponse({"error": "Неверная подписка"}, status=400)
            sub_name, base_price = sub_data
            subscription = TypeOfSubscription.objects.get(name=sub_name)

            # Кол-во персон
            persons = int(request.POST.get("select5", 0)) + 1

            # Приёмы пищи
            selected_meals = [
                int(sel[-1])
                for sel in ["select1", "select2", "select3", "select4"]
                if request.POST.get(sel) == "0"
            ]
            meals = FoodIntake.objects.filter(id__in=selected_meals)

            # Аллергии
            allergy_codes = [
                key.split("_")[1] for key in request.POST if key.startswith("allergy_")
            ]
            allergy_names = [
                ALLERGY_MAPPING[c] for c in allergy_codes if c in ALLERGY_MAPPING
            ]
            allergies = Allergy.objects.filter(name__in=allergy_names)

            # Расчёт цены
            total_price = base_price + len(selected_meals) * 300 * persons
            print(
                f"Цена: {total_price}, Персоны: {persons}, Приёмы пищи: {selected_meals}"
            )
            
            # Создание заказа
            order = Order.objects.create(
                profile=profile,
                type_of_subscription=subscription,
                number_of_people=persons,
                total_price=total_price,
                status=False,
            )
            order.food_intake.set(meals)
            order.allergy.set(allergies)
            order.type_of_menu.set([menu_obj])
                
            print("Заказ создан:", order.id)
            return JsonResponse({"message": "Заказ успешно сохранён!"})

        except Exception as e:
            import traceback

            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "order.html")



