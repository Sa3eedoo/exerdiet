from datetime import date
from decimal import Decimal
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from diet.models import Meal, Water
from gym.models import PerformedWorkout
from .models import Trainee


class UserCreateSerializer(BaseUserCreateSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['username', 'email', 'first_name', 'last_name']


class TraineeSerializer(serializers.ModelSerializer):
    daily_calories_needs = serializers.IntegerField(read_only=True)
    daily_water_needs = serializers.IntegerField(read_only=True)
    carbs_ratio = serializers.DecimalField(
        read_only=True, max_digits=4, decimal_places=1)
    fats_ratio = serializers.DecimalField(
        read_only=True, max_digits=4, decimal_places=1)
    protein_ratio = serializers.DecimalField(
        read_only=True, max_digits=4, decimal_places=1)
    daily_streak = serializers.IntegerField(read_only=True)
    calories_intake_today = serializers.SerializerMethodField(read_only=True)
    calories_burned_today = serializers.SerializerMethodField(read_only=True)
    water_intake_today = serializers.SerializerMethodField(read_only=True)
    carbs_grams = serializers.SerializerMethodField(read_only=True)
    fats_grams = serializers.SerializerMethodField(read_only=True)
    protein_grams = serializers.SerializerMethodField(read_only=True)

    def get_calories_intake_today(self, trainee: Trainee):
        total_calories = 0
        today = date.today()
        meals_today = Meal.objects.filter(
            trainee=trainee, time_eaten__date=today)

        if not meals_today:
            return total_calories
        else:
            for meal in meals_today:
                for recipe in meal.recipes.all():
                    for food_instance in recipe.food_instances.all():
                        total_calories += food_instance.food.calories * food_instance.quantity / 100
                for food_instance in meal.food_instances.all():
                    total_calories += food_instance.food.calories * food_instance.quantity / 100
            return int(total_calories)

    def get_calories_burned_today(self, trainee: Trainee):
        total_calories = 0
        today = date.today()
        performed_workout_today = PerformedWorkout.objects.filter(
            trainee=trainee, time_performed__date=today)

        if not performed_workout_today:
            return total_calories
        else:
            for performed_workout in performed_workout_today:
                for workout in performed_workout.workouts.all():
                    for exercise_instance in workout.exercise_instances.all():
                        total_calories += exercise_instance.exercise.calories_burned * \
                            exercise_instance.duration * exercise_instance.sets / 60
                for exercise_instance in performed_workout.exercise_instances.all():
                    total_calories += exercise_instance.exercise.calories_burned * \
                        exercise_instance.duration * exercise_instance.sets / 60
            return int(total_calories)

    def get_water_intake_today(self, trainee: Trainee):
        total_water = 0
        today = date.today()
        waters_today = Water.objects.filter(
            trainee=trainee, drinking_date=today)

        if not waters_today:
            return total_water
        else:
            for water in waters_today:
                total_water += water.amount
            return int(total_water)

    def get_carbs_grams(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.carbs_ratio / 4, 1))

    def get_fats_grams(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.fats_ratio / 9, 1))

    def get_protein_grams(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.protein_ratio / 4, 1))

    class Meta:
        model = Trainee
        fields = ['birthdate', 'gender', 'height', 'weight', 'daily_calories_needs',
                  'calories_intake_today', 'calories_burned_today', 'daily_water_needs',
                  'water_intake_today', 'carbs_ratio', 'fats_ratio', 'protein_ratio',
                  'carbs_grams', 'fats_grams', 'protein_grams',
                  'activity_level', 'goal', 'daily_streak']


class TraineeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = ['birthdate', 'gender', 'height',
                  'weight', 'activity_level', 'goal']

    def create(self, validated_data):
        trainee = Trainee(**validated_data)
        trainee.user_id = self.context['user_id']
        trainee.save()
        return trainee


class TraineeUpdateCaloriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = ['daily_calories_needs']


class TraineeUpdateWaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = ['daily_water_needs']


class TraineeUpdateMacronutrientsRatiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = ['carbs_ratio', 'fats_ratio', 'protein_ratio']
