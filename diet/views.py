from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from core.models import Trainee
from core.pagination import DefaultPagination
from .filters import FoodFilter, MealFilter, WaterFilter
from .models import Food, CustomFood, FoodInstance, Recipe, Meal, Water
from . import serializers


class FoodViewSet(ReadOnlyModelViewSet):
    queryset = Food.objects.\
        filter(customfood__isnull=True).order_by('name')
    serializer_class = serializers.FoodSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FoodFilter
    pagination_class = DefaultPagination
    search_fields = ['name']
    ordering_fields = ['calories', 'carbs', 'fats', 'protein']


class CustomFoodViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FoodFilter
    pagination_class = DefaultPagination
    search_fields = ['name']
    ordering_fields = ['calories', 'carbs', 'fats', 'protein']

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = get_object_or_404(Trainee, user_id=user_id)
        return CustomFood.objects.filter(trainee=trainee).order_by('name')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CustomFoodCreateSerializer
        if self.request.method == 'PATCH':
            return serializers.CustomFoodUpdateSerializer
        return serializers.FoodSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def destroy(self, request, *args, **kwargs):
        custom_food = self.get_object()
        if custom_food.food_instances.exists():
            return Response({'error': 'Food cannot be deleted because it is associated with a recipe or a meal.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(custom_food)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [SearchFilter]
    pagination_class = DefaultPagination
    search_fields = ['name', 'instructions']

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = get_object_or_404(Trainee, user_id=user_id)
        return Recipe.objects.\
            filter(trainee=trainee).\
            prefetch_related('food_instances__food').\
            order_by('name')

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.RecipeUpdateSerializer
        return serializers.RecipeSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        if recipe.meals.exists():
            return Response({'error': 'Recipe cannot be deleted because it is associated with a meal.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeFoodInstanceViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = get_object_or_404(Trainee, user_id=user_id)
        recipe_id = self.kwargs['recipe_pk']
        recipe = get_object_or_404(Recipe, id=recipe_id, trainee=trainee)
        return recipe.food_instances\
            .select_related('food')\
            .order_by('id')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.FoodInstanceCreateSerializer
        if self.request.method == 'PATCH':
            return serializers.FoodInstanceUpdateSerializer
        return serializers.FoodInstanceSerializer

    def get_serializer_context(self):
        return {'recipe_id': self.kwargs['recipe_pk'],
                'user_id': self.request.user.id}


class MealViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MealFilter
    pagination_class = DefaultPagination
    search_fields = ['name']
    ordering_fields = ['time_eaten']

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = get_object_or_404(Trainee, user_id=user_id)
        return Meal.objects.\
            filter(trainee=trainee).\
            prefetch_related('recipes__food_instances__food').\
            prefetch_related('food_instances__food').\
            order_by('-time_eaten')

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.MealUpdateSerializer
        return serializers.MealSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class MealRecipeViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = get_object_or_404(Trainee, user_id=user_id)
        meal_id = self.kwargs['meal_pk']
        meal = get_object_or_404(Meal, id=meal_id, trainee=trainee)
        return meal.recipes\
            .prefetch_related('food_instances__food')\
            .order_by('name')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.MealAddRecipeSerializer
        return serializers.SimpleRecipeSerializer

    def get_serializer_context(self):
        return {'meal_id': self.kwargs['meal_pk'],
                'user_id': self.request.user.id}

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        meal_id = self.kwargs['meal_pk']
        meal = Meal.objects.get(id=meal_id)
        meal.recipes.remove(recipe)

        return Response(status=status.HTTP_204_NO_CONTENT)


class MealFoodInstanceViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = get_object_or_404(Trainee, user_id=user_id)
        meal_id = self.kwargs['meal_pk']
        meal = get_object_or_404(Meal, id=meal_id, trainee=trainee)
        return meal.food_instances\
            .select_related('food')\
            .order_by('id')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.FoodInstanceCreateSerializer
        if self.request.method == 'PATCH':
            return serializers.FoodInstanceUpdateSerializer
        return serializers.FoodInstanceSerializer

    def get_serializer_context(self):
        return {'meal_id': self.kwargs['meal_pk'],
                'user_id': self.request.user.id}


class WaterViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [DjangoFilterBackend]
    filterset_class = WaterFilter
    pagination_class = DefaultPagination

    def get_queryset(self):
        user_id = self.request.user.id
        trainee = get_object_or_404(Trainee, user_id=user_id)
        return Water.objects.filter(trainee=trainee).order_by('-drinking_date')

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.WaterUpdateSerializer
        return serializers.WaterSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
