from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from . import models


CALORIE_LEVEL_LOW = 100
CALORIE_LEVEL_HIGH = 250
CARB_LEVEL_LOW = 10
CARB_LEVEL_HIGH = 40
FAT_LEVEL_LOW = 5
FAT_LEVEL_HIGH = 10
PROTEIN_LEVEL_LOW = 5
PROTEIN_LEVEL_HIGH = 15


class CalorieLevelFilter(admin.SimpleListFilter):
    title = 'calorie level'
    parameter_name = 'calorie_level'
    FILTER_ZERO = '0'
    FILTER_LOW = f'<{CALORIE_LEVEL_LOW}'
    FILTER_MED = f'<{CALORIE_LEVEL_HIGH}'
    FILTER_HIGH = f'>{CALORIE_LEVEL_HIGH}'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_ZERO, 'Zero'),
            (self.FILTER_LOW, 'Low'),
            (self.FILTER_MED, 'Medium'),
            (self.FILTER_HIGH, 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_ZERO:
            return queryset.filter(calories=0)
        if self.value() == self.FILTER_LOW:
            return queryset.filter(calories__gt=0).filter(calories__lt=CALORIE_LEVEL_LOW)
        if self.value() == self.FILTER_MED:
            return queryset.filter(calories__gte=CALORIE_LEVEL_LOW).filter(calories__lt=CALORIE_LEVEL_HIGH)
        if self.value() == self.FILTER_HIGH:
            return queryset.filter(calories__gte=CALORIE_LEVEL_HIGH)


class CarbLevelFilter(admin.SimpleListFilter):
    title = 'carb level'
    parameter_name = 'carb_level'
    FILTER_ZERO = '0'
    FILTER_LOW = f'<{CARB_LEVEL_LOW}'
    FILTER_MED = f'<{CARB_LEVEL_HIGH}'
    FILTER_HIGH = f'>{CARB_LEVEL_HIGH}'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_ZERO, 'Zero'),
            (self.FILTER_LOW, 'Low'),
            (self.FILTER_MED, 'Medium'),
            (self.FILTER_HIGH, 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_ZERO:
            return queryset.filter(carbs=0)
        if self.value() == self.FILTER_LOW:
            return queryset.filter(carbs__gt=0).filter(carbs__lt=CARB_LEVEL_LOW)
        if self.value() == self.FILTER_MED:
            return queryset.filter(carbs__gte=CARB_LEVEL_LOW).filter(carbs__lt=CARB_LEVEL_HIGH)
        if self.value() == self.FILTER_HIGH:
            return queryset.filter(carbs__gte=CARB_LEVEL_HIGH)


class FatLevelFilter(admin.SimpleListFilter):
    title = 'fat level'
    parameter_name = 'fat_level'
    FILTER_ZERO = '0'
    FILTER_LOW = f'<{FAT_LEVEL_LOW}'
    FILTER_MED = f'<{FAT_LEVEL_HIGH}'
    FILTER_HIGH = f'>{FAT_LEVEL_HIGH}'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_ZERO, 'Zero'),
            (self.FILTER_LOW, 'Low'),
            (self.FILTER_MED, 'Medium'),
            (self.FILTER_HIGH, 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_ZERO:
            return queryset.filter(fats=0)
        if self.value() == self.FILTER_LOW:
            return queryset.filter(fats__gt=0).filter(fats__lt=FAT_LEVEL_LOW)
        if self.value() == self.FILTER_MED:
            return queryset.filter(fats__gte=FAT_LEVEL_LOW).filter(fats__lt=FAT_LEVEL_HIGH)
        if self.value() == self.FILTER_HIGH:
            return queryset.filter(fats__gte=FAT_LEVEL_HIGH)


class ProteinLevelFilter(admin.SimpleListFilter):
    title = 'protein level'
    parameter_name = 'protein_level'
    FILTER_ZERO = '0'
    FILTER_LOW = f'<{PROTEIN_LEVEL_LOW}'
    FILTER_MED = f'<{PROTEIN_LEVEL_HIGH}'
    FILTER_HIGH = f'>{PROTEIN_LEVEL_HIGH}'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_ZERO, 'Zero'),
            (self.FILTER_LOW, 'Low'),
            (self.FILTER_MED, 'Medium'),
            (self.FILTER_HIGH, 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_ZERO:
            return queryset.filter(protein=0)
        if self.value() == self.FILTER_LOW:
            return queryset.filter(protein__gt=0).filter(protein__lt=PROTEIN_LEVEL_LOW)
        if self.value() == self.FILTER_MED:
            return queryset.filter(protein__gte=PROTEIN_LEVEL_LOW).filter(protein__lt=PROTEIN_LEVEL_HIGH)
        if self.value() == self.FILTER_HIGH:
            return queryset.filter(protein__gte=PROTEIN_LEVEL_HIGH)


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'calorie_level', 'calories',
                    'carbs', 'fats', 'protein', 'category']
    list_editable = ['calories', 'carbs', 'fats', 'protein', 'category']
    list_filter = ['category', CalorieLevelFilter,
                   CarbLevelFilter, FatLevelFilter, ProteinLevelFilter]
    list_per_page = 100
    ordering = ['name']
    search_fields = ['name']

    @admin.display(ordering='calories')
    def calorie_level(self, food):
        if food.calories == 0:
            return 'Zero'
        elif food.calories < CALORIE_LEVEL_LOW:
            return 'Low'
        elif food.calories < CALORIE_LEVEL_HIGH:
            return 'Medium'
        return 'High'

    # def get_queryset(self, request):
    #     return super().get_queryset(request).exclude(customfood__isnull=False)


@admin.register(models.CustomFood)
class CustomFoodAdmin(admin.ModelAdmin):
    autocomplete_fields = ['trainee']
    list_display = ['name', 'trainee_user_name', 'calorie_level',
                    'calories', 'carbs', 'fats', 'protein', 'category']
    list_filter = ['category', CalorieLevelFilter,
                   CarbLevelFilter, FatLevelFilter, ProteinLevelFilter]
    list_select_related = ['trainee__user']
    list_per_page = 100
    ordering = ['name']
    search_fields = ['name', 'trainee__user__username']

    def trainee_user_name(self, custom_food):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(custom_food.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, custom_food.trainee)

    @admin.display(ordering='calories')
    def calorie_level(self, food):
        if food.calories == 0:
            return 'Zero'
        elif food.calories < CALORIE_LEVEL_LOW:
            return 'Low'
        elif food.calories < CALORIE_LEVEL_HIGH:
            return 'Medium'
        return 'High'


@admin.register(models.FoodInstance)
class FoodInstanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['food', 'recipe', 'meal']
    list_display = ['food_name', 'quantity', 'recipe_name', 'meal_name']
    list_display_links = ['quantity']
    list_per_page = 100
    list_select_related = ['food', 'recipe', 'meal']
    ordering = ['food__name']
    search_fields = ['food__name']

    def food_name(self, food_instacne):
        url = (
            reverse('admin:diet_food_changelist') +
            str(food_instacne.food.id)
        )
        return format_html('<a href="{}">{}</a>', url, food_instacne.food)

    def recipe_name(self, food_instacne):
        url = (
            reverse('admin:diet_recipe_changelist') +
            str(food_instacne.recipe.id)
        )
        return format_html('<a href="{}">{}</a>', url, food_instacne.recipe)

    def meal_name(self, food_instacne):
        if food_instacne.meal:
            url = (
                reverse('admin:diet_meal_changelist') +
                str(food_instacne.meal.id)
            )
            return format_html('<a href="{}">{}</a>', url, food_instacne.meal)
        return food_instacne.meal


@admin.register(models.Recipe)
class RecipeInstanceAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(models.Meal)
class MealInstanceAdmin(admin.ModelAdmin):
    search_fields = ['name']
