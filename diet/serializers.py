from rest_framework import serializers
from core.models import Trainee
from .models import Food, CustomFood, Recipe, Meal, FoodInstance


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'category', 'calories',
                  'carbs', 'fats', 'protein', 'image']


class CustomFoodCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomFood
        fields = ['id', 'name', 'category', 'calories',
                  'carbs', 'fats', 'protein', 'image']

    def create(self, validated_data):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)
        custom_food = CustomFood(**validated_data)
        custom_food.trainee = trainee
        custom_food.save()
        return custom_food


class CustomFoodUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFood
        fields = ['name', 'category', 'calories',
                  'carbs', 'fats', 'protein', 'image']


class SimpleFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'calories', 'carbs', 'fats', 'protein']


class FoodInstanceSerializer(serializers.ModelSerializer):
    food = SimpleFoodSerializer(read_only=True)
    total_calories = serializers.SerializerMethodField(read_only=True)
    total_carbs = serializers.SerializerMethodField(read_only=True)
    total_fats = serializers.SerializerMethodField(read_only=True)
    total_protein = serializers.SerializerMethodField(read_only=True)

    def get_total_calories(self, food_instance: FoodInstance):
        return food_instance.get_total_calories()

    def get_total_carbs(self, food_instance: FoodInstance):
        return food_instance.get_total_carbs()

    def get_total_fats(self, food_instance: FoodInstance):
        return food_instance.get_total_fats()

    def get_total_protein(self, food_instance: FoodInstance):
        return food_instance.get_total_protein()

    class Meta:
        model = FoodInstance
        fields = ['id', 'food', 'quantity', 'total_calories',
                  'total_carbs', 'total_fats', 'total_protein']


class FoodInstanceCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    food_id = serializers.IntegerField()

    def validate_food_id(self, value):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)

        if not Food.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                'No food with the given id was found.'
            )
        if Food.objects.filter(id=value, customfood__isnull=False).exists():
            if not CustomFood.objects.filter(food_ptr_id=value, trainee=trainee).exists():
                raise serializers.ValidationError(
                    'No food with the given id was found.'
                )
        return value

    class Meta:
        model = FoodInstance
        fields = ['id', 'food_id', 'quantity']

    def create(self, validated_data):
        recipe_id = self.context.get('recipe_id')
        meal_id = self.context.get('meal_id')
        if recipe_id:
            food_instance = FoodInstance(recipe_id=recipe_id,
                                         **validated_data)
        if meal_id:
            food_instance = FoodInstance(meal_id=meal_id,
                                         **validated_data)
        food_instance.save()
        return food_instance


class FoodInstanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodInstance
        fields = ['quantity']


class RecipeSerializer(serializers.ModelSerializer):
    food_instances = FoodInstanceSerializer(many=True, read_only=True)
    total_calories = serializers.SerializerMethodField(read_only=True)
    total_carbs = serializers.SerializerMethodField(read_only=True)
    total_fats = serializers.SerializerMethodField(read_only=True)
    total_protein = serializers.SerializerMethodField(read_only=True)

    def get_total_calories(self, recipe: Recipe):
        return recipe.get_total_calories()

    def get_total_carbs(self, recipe: Recipe):
        return recipe.get_total_carbs()

    def get_total_fats(self, recipe: Recipe):
        return recipe.get_total_fats()

    def get_total_protein(self, recipe: Recipe):
        return recipe.get_total_protein()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'image', 'food_instances',
                  'total_calories', 'total_carbs', 'total_fats', 'total_protein']

    def create(self, validated_data):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)
        recipe = Recipe(**validated_data)
        recipe.trainee = trainee
        recipe.save()
        return recipe


class RecipeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['name', 'instructions', 'image']


class SimpleRecipeSerializer(serializers.ModelSerializer):
    food_instances = FoodInstanceSerializer(many=True, read_only=True)
    total_calories = serializers.SerializerMethodField(read_only=True)
    total_carbs = serializers.SerializerMethodField(read_only=True)
    total_fats = serializers.SerializerMethodField(read_only=True)
    total_protein = serializers.SerializerMethodField(read_only=True)

    def get_total_calories(self, recipe: Recipe):
        return recipe.get_total_calories()

    def get_total_carbs(self, recipe: Recipe):
        return recipe.get_total_carbs()

    def get_total_fats(self, recipe: Recipe):
        return recipe.get_total_fats()

    def get_total_protein(self, recipe: Recipe):
        return recipe.get_total_protein()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'food_instances', 'total_calories',
                  'total_carbs', 'total_fats', 'total_protein']


class MealSerializer(serializers.ModelSerializer):
    recipes = SimpleRecipeSerializer(many=True, read_only=True)
    food_instances = FoodInstanceSerializer(many=True, read_only=True)
    total_calories = serializers.SerializerMethodField(read_only=True)
    total_carbs = serializers.SerializerMethodField(read_only=True)
    total_fats = serializers.SerializerMethodField(read_only=True)
    total_protein = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(max_length=150, required=False)

    def get_total_calories(self, meal: Meal):
        return meal.get_total_calories()

    def get_total_carbs(self, meal: Meal):
        return meal.get_total_carbs()

    def get_total_fats(self, meal: Meal):
        return meal.get_total_fats()

    def get_total_protein(self, meal: Meal):
        return meal.get_total_protein()

    class Meta:
        model = Meal
        fields = ['id', 'name', 'time_eaten', 'recipes', 'food_instances',
                  'total_calories', 'total_carbs', 'total_fats', 'total_protein']

    def create(self, validated_data):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)
        meal = Meal(**validated_data)
        meal.trainee = trainee
        meal.save()
        return meal


class MealUpdateSerializer(serializers.ModelSerializer):
    time_eaten = serializers.DateTimeField()

    class Meta:
        model = Meal
        fields = ['name', 'time_eaten']


class MealAddRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate_id(self, recipe_id):
        user_id = self.context['user_id']
        trainee = Trainee.objects.get(user_id=user_id)

        if not Recipe.objects.filter(id=recipe_id, trainee=trainee).exists():
            raise serializers.ValidationError(
                'No recipe with the given id was found.'
            )
        return recipe_id

    class Meta:
        model = Recipe
        fields = ['id']

    def create(self, validated_data):
        recipe_id = validated_data['id']
        meal_id = self.context['meal_id']
        recipe = Recipe.objects.get(id=recipe_id)
        meal = Meal.objects.get(id=meal_id)
        meal.recipes.add(recipe)
        return recipe
