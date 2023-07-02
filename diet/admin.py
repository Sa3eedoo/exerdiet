from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.http.request import HttpRequest
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


class CustomFoodFilter(admin.SimpleListFilter):
    title = 'is custom food'
    parameter_name = 'is_custom_food'
    FILTER_CUSTOM = '1'
    FILTER_NOT_CUSTOM = '0'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_CUSTOM, 'Custom Food'),
            (self.FILTER_NOT_CUSTOM, 'Not Custom Food')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_CUSTOM:
            return queryset.filter(customfood__isnull=False)
        if self.value() == self.FILTER_NOT_CUSTOM:
            return queryset.exclude(customfood__isnull=False)


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'calorie_level', 'calories',
                    'carbs', 'fats', 'protein', 'category']
    list_editable = ['calories', 'carbs', 'fats', 'protein', 'category']
    list_filter = [CustomFoodFilter, 'category', CalorieLevelFilter,
                   CarbLevelFilter, FatLevelFilter, ProteinLevelFilter]
    list_per_page = 100
    ordering = ['name']
    readonly_fields = ['thumbnail']
    search_fields = ['name']

    class Media:
        css = {
            'all': ['core/styles.css']
        }

    def thumbnail(self, food: models.Food):
        if food.image.name != '':
            return format_html(f'<img src="{food.image.url}" class="thumbnail"/>')
        return ''

    @admin.display(ordering='calories')
    def calorie_level(self, food):
        if food.calories == 0:
            return 'Zero'
        elif food.calories < CALORIE_LEVEL_LOW:
            return 'Low'
        elif food.calories < CALORIE_LEVEL_HIGH:
            return 'Medium'
        return 'High'

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['calories'].widget.attrs['placeholder'] = 'cal/(100gm,ml)(1tsp)'
        form.base_fields['carbs'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'
        form.base_fields['fats'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'
        form.base_fields['protein'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'

        return form


@admin.register(models.CustomFood)
class CustomFoodAdmin(admin.ModelAdmin):
    autocomplete_fields = ['trainee']
    list_display = ['name', 'trainee_username', 'calorie_level',
                    'calories', 'carbs', 'fats', 'protein', 'category']
    list_filter = ['category', CalorieLevelFilter,
                   CarbLevelFilter, FatLevelFilter, ProteinLevelFilter]
    list_select_related = ['trainee__user']
    list_per_page = 100
    ordering = ['name']
    readonly_fields = ['thumbnail']
    search_fields = ['name', 'trainee__user__username__istartswith']

    class Media:
        css = {
            'all': ['core/styles.css']
        }

    def thumbnail(self, custom_food: models.CustomFood):
        if custom_food.image.name != '':
            return format_html(f'<img src="{custom_food.image.url}" class="thumbnail"/>')
        return ''

    @admin.display(ordering='trainee__user__username')
    def trainee_username(self, custom_food):
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

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['calories'].widget.attrs['placeholder'] = 'cal/(100gm,ml)(1tsp)'
        form.base_fields['carbs'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'
        form.base_fields['fats'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'
        form.base_fields['protein'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'

        return form

    @admin.display(ordering='food__name')
    def food_name(self, food_instance):
        url = (
            reverse('admin:diet_food_changelist') +
            str(food_instance.food.id)
        )
        return format_html('<a href="{}">{}</a>', url, food_instance.food)

    @admin.display(ordering='recipe__name')
    def recipe_name(self, food_instance):
        if food_instance.recipe:
            url = (
                reverse('admin:diet_recipe_changelist') +
                str(food_instance.recipe.id)
            )
            return format_html('<a href="{}">{}</a>', url, food_instance.recipe)
        return food_instance.recipe

    @admin.display(ordering='meal__name')
    def meal_name(self, food_instance):
        if food_instance.meal:
            url = (
                reverse('admin:diet_meal_changelist') +
                str(food_instance.meal.id)
            )
            return format_html('<a href="{}">{}</a>', url, food_instance.meal)
        return food_instance.meal

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['calories'].widget.attrs['placeholder'] = 'cal/(100gm,ml)(1tsp)'
        form.base_fields['carbs'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'
        form.base_fields['fats'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'
        form.base_fields['protein'].widget.attrs['placeholder'] = 'gram/(100gm,ml)(1tsp)'

        return form


class FoodInstanceRecipeInline(admin.TabularInline):
    model = models.FoodInstance
    autocomplete_fields = ['food']
    exclude = ['meal']
    extra = 1
    fields = ['food', 'quantity']

    def formfield_for_dbfield(self, db_field, request: HttpRequest | None, **kwargs: Any):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'quantity':
            field.widget.attrs['placeholder'] = 'gm|mL|tsp'
        return field


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['trainee']
    list_display = ['name', 'trainee_username', 'eaten_count', 'instructions']
    list_select_related = ['trainee__user']
    list_per_page = 100
    ordering = ['name']
    readonly_fields = ['thumbnail']
    search_fields = ['name', 'trainee__user__username__istartswith']
    inlines = [FoodInstanceRecipeInline]

    class Media:
        css = {
            'all': ['core/styles.css']
        }

    def thumbnail(self, recipe: models.Recipe):
        if recipe.image.name != '':
            return format_html(f'<img src="{recipe.image.url}" class="thumbnail"/>')
        return ''

    @admin.display(ordering='trainee__user__username')
    def trainee_username(self, recipe):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(recipe.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, recipe.trainee)

    @admin.display(ordering='eaten_count')
    def eaten_count(self, recipe):
        return recipe.eaten_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(eaten_count=Count('meals'))


class FoodInstanceMealInline(admin.TabularInline):
    model = models.FoodInstance
    autocomplete_fields = ['food']
    exclude = ['recipe']
    extra = 1
    fields = ['food', 'quantity']

    def formfield_for_dbfield(self, db_field, request: HttpRequest | None, **kwargs: Any):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'quantity':
            field.widget.attrs['placeholder'] = 'gm|mL|tsp'
        return field


class RecipeMealInline(admin.TabularInline):
    model = models.Recipe.meals.through
    autocomplete_fields = ['recipe']
    extra = 1
    verbose_name = "Recipe"
    verbose_name_plural = "Recipes"


@admin.register(models.Meal)
class MealAdmin(admin.ModelAdmin):
    autocomplete_fields = ['trainee']
    exclude = ['recipes']
    list_display = ['name', 'trainee_username', 'time_eaten']
    list_filter = ['time_eaten']
    list_per_page = 100
    list_select_related = ['trainee__user']
    inlines = [RecipeMealInline, FoodInstanceMealInline]
    ordering = ['time_eaten']
    search_fields = ['name', 'trainee__user__username__istartswith']

    @admin.display(ordering='trainee__user__username')
    def trainee_username(self, recipe):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(recipe.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, recipe.trainee)


@admin.register(models.Water)
class WaterAdmin(admin.ModelAdmin):
    autocomplete_fields = ['trainee']
    list_display = ['amount', 'trainee_username', 'drinking_date']
    list_per_page = 100
    list_select_related = ['trainee__user']
    ordering = ['trainee__user__username']
    search_fields = ['trainee__user__username__istartswith']

    @admin.display(ordering='trainee__user__username')
    def trainee_username(self, custom_food):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(custom_food.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, custom_food.trainee)

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['amount'].widget.attrs['placeholder'] = 'mL'

        return form
