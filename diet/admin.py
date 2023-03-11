from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from . import models


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'calorie_level', 'calories',
                    'carbs', 'fats', 'protein', 'category']
    list_editable = ['calories', 'carbs', 'fats', 'protein', 'category']
    list_per_page = 10
    ordering = ['name']
    search_fields = ['name']

    @admin.display(ordering='calories')
    def calorie_level(self, food):
        if food.calories == 0:
            return 'Zero'
        elif food.calories < 100:
            return 'Low'
        elif food.calories < 250:
            return 'Medium'
        return 'High'

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(customfood__isnull=False)


@admin.register(models.CustomFood)
class CustomFoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'trainee_user_name']
    list_select_related = ['trainee__user']

    def trainee_user_name(self, custom_food):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(custom_food.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, custom_food.trainee)
