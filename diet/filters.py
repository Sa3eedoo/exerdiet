from django_filters import rest_framework as filters
from .models import Food, Meal


class FoodFilter(filters.FilterSet):
    class Meta:
        model = Food
        fields = {
            'category': ['exact'],
            'calories': ['gte', 'lte'],
            'carbs': ['gte', 'lte'],
            'fats': ['gte', 'lte'],
            'protein': ['gte', 'lte'],
        }


class MealFilter(filters.FilterSet):
    class Meta:
        model = Meal
        fields = {
            'time_eaten': ['gte', 'lte'],
        }
