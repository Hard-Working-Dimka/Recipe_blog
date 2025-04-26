from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)


class Diet(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Диета"
        verbose_name_plural = "Диеты"

    def __str__(self):
        return self.name


class TypeOfMenu(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип меню")

    class Meta:
        verbose_name = "Тип меню"
        verbose_name_plural = "Типы меню"

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(max_length=100, verbose_name="Аллергия")

    class Meta:
        verbose_name = "Аллергия"
        verbose_name_plural = "Аллергии"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ингредиент")
    quantity_of_ingredients = models.IntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class FoodIntake(models.Model):  # завтрак/обед/ужин
    name = models.CharField(max_length=100, verbose_name="Приём пищи")

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"

    def __str__(self):
        return self.name


class TypeOfSubscription(models.Model):
    period = models.IntegerField(verbose_name="Период (дней)")
    price = models.IntegerField(verbose_name="Цена")
    name = models.CharField(max_length=100, verbose_name="Название подписки", blank=True)

    class Meta:
        verbose_name = "Тип подписки"
        verbose_name_plural = "Типы подписок"

    def __str__(self):
        return self.name  # Возвращаем название подписки



class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    avatar = models.ImageField(upload_to="users", verbose_name="Аватар")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        
    def __str__(self):
        return self.user.email


class Recipe(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    image = models.ImageField(verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        Ingredient, related_name="recipes", verbose_name="Ингредиенты"
    )
    diet = models.ManyToManyField(Diet, related_name="recipes", verbose_name="Диеты")
    allergy = models.ManyToManyField(
        Allergy, related_name="recipes", verbose_name="Аллергии"
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    slug = models.SlugField(verbose_name="URL-имя")
    likes = models.ManyToManyField(
        User, related_name="liked_recipes", verbose_name="Лайки"
    )
    calories = models.IntegerField(verbose_name="Калории")
    type_of_menu = models.ManyToManyField(
        TypeOfMenu, related_name="recipes", verbose_name="Типы меню"
    )
    food_intake = models.ManyToManyField(
        FoodIntake, related_name="recipes", verbose_name="Приёмы пищи"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title


class Order(models.Model):
    profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name="Профиль"
    )
    type_of_subscription = models.ForeignKey(
        TypeOfSubscription, on_delete=models.CASCADE, verbose_name="Подписка"
    )
    food_intake = models.ManyToManyField(
        FoodIntake, related_name="orders", verbose_name="Приёмы пищи"
    )
    number_of_people = models.IntegerField(default=1, verbose_name="Количество персон")
    allergy = models.ManyToManyField(
        Allergy, related_name="orders", verbose_name="Аллергии"
    )
    total_price = models.IntegerField(verbose_name="Общая цена")
    status = models.BooleanField(default=False, verbose_name="Статус оплаты")
    type_of_menu = models.ManyToManyField(
        TypeOfMenu, related_name="orders", verbose_name="Типы меню"
    )
    duration = models.IntegerField(default=False, verbose_name="Длительность подписки")  # добавлено
    breakfasts = models.BooleanField(default=False, verbose_name="Завтрак включён")  # добавлено
    lunches = models.BooleanField(default=False, verbose_name="Ужин включён")  # добавлено
    dinners = models.BooleanField(default=False, verbose_name="Ужин включён")  # добавлено
    desserts = models.BooleanField(default=False, verbose_name="Десерт включён")  # добавлено

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ от {self.profile.user.username}"

