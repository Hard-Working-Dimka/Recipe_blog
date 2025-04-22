from django.contrib.auth.models import User
from django.db import models


class Diet(models.Model):  # TODO: на сайте нет, в ТЗ есть!
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TypeOfMenu(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity_of_ingredients = models.IntegerField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users')


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    diet = models.ManyToManyField(Diet, related_name='recipes')
    allergy = models.ManyToManyField(Allergy, related_name='recipes')
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()  # для url путей
    likes = models.ManyToManyField(User, related_name='liked_recipes')
    calories = models.IntegerField()
    type_of_menu = models.ManyToManyField(TypeOfMenu, related_name='recipes')

    def __str__(self):
        return self.title


class TypeOfSubscription(models.Model):
    period = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.period


class FoodIntake(models.Model):  # завтрак/обед/ужин
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    type_of_subscription = models.ForeignKey(TypeOfSubscription, on_delete=models.CASCADE)
    food_intake = models.ManyToManyField(FoodIntake)
    number_of_people = models.IntegerField()
    allergy = models.ManyToManyField(Allergy, related_name='orders')
    total_price = models.IntegerField()
    status = models.BooleanField(default=False)  # TODO:ДЛЯ ОПЛАТЫ,возможно , лишнее, подумать как сделать оплату
    type_of_menu = models.ManyToManyField(TypeOfMenu, related_name='orders')

    def __str__(self):
        return self.profile.user
