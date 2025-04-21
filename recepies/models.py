from django.contrib.auth.models import User
from django.db import models


class Diet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()
    ingredients = models.TextField()
    diet = models.ManyToManyField(Diet, related_name='recipes')
    allergy = models.ManyToManyField(Allergy, related_name='recipes')
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()  # для url путей
    likes = models.ManyToManyField(User, related_name='liked_recipes')

    def __str__(self):
        return self.title
