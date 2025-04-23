from django.contrib import admin
from .models import (
    Diet,
    TypeOfMenu,
    Allergy,
    Ingredient,
    FoodIntake,
    TypeOfSubscription,
    UserProfile,
    Recipe,
    Order,
)


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(TypeOfMenu)
class TypeOfMenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity_of_ingredients")
    search_fields = ("name",)


@admin.register(FoodIntake)
class FoodIntakeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(TypeOfSubscription)
class TypeOfSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "period", "price")
    list_filter = ("period", "price")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "avatar")
    raw_id_fields = ("user",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "pub_date", "calories")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")
    filter_horizontal = (
        "ingredients",
        "diet",
        "allergy",
        "likes",
        "type_of_menu",
        "food_intake",
    )
    list_filter = ("pub_date", "diet", "type_of_menu", "food_intake")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "profile",
        "type_of_subscription",
        "number_of_people",
        "total_price",
        "status",
    )
    raw_id_fields = ("profile",)
    filter_horizontal = ("food_intake", "allergy", "type_of_menu")
    list_filter = ("status", "type_of_subscription")
