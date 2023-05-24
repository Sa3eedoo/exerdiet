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
    carbs_intake_today = serializers.SerializerMethodField(read_only=True)
    fats_intake_today = serializers.SerializerMethodField(read_only=True)
    protein_intake_today = serializers.SerializerMethodField(read_only=True)
    calories_burned_today = serializers.SerializerMethodField(read_only=True)
    water_intake_today = serializers.SerializerMethodField(read_only=True)
    carbs_needs = serializers.SerializerMethodField(read_only=True)
    fats_needs = serializers.SerializerMethodField(read_only=True)
    protein_needs = serializers.SerializerMethodField(read_only=True)

    def get_calories_intake_today(self, trainee: Trainee):
        total_calories = 0
        today = date.today()
        meals_today = Meal.objects.filter(
            trainee=trainee, time_eaten__date=today)

        if not meals_today:
            return total_calories
        else:
            for meal in meals_today:
                total_calories += meal.get_total_calories()
            return int(total_calories)

    def get_carbs_intake_today(self, trainee: Trainee):
        total_carbs = 0
        today = date.today()
        meals_today = Meal.objects.filter(
            trainee=trainee, time_eaten__date=today)

        if not meals_today:
            return round(total_carbs, 1)
        else:
            for meal in meals_today:
                total_carbs += meal.get_total_carbs()
            return round(total_carbs, 1)

    def get_fats_intake_today(self, trainee: Trainee):
        total_fats = 0
        today = date.today()
        meals_today = Meal.objects.filter(
            trainee=trainee, time_eaten__date=today)

        if not meals_today:
            return round(total_fats, 1)
        else:
            for meal in meals_today:
                total_fats += meal.get_total_fats()
            return round(total_fats, 1)

    def get_protein_intake_today(self, trainee: Trainee):
        total_protein = 0
        today = date.today()
        meals_today = Meal.objects.filter(
            trainee=trainee, time_eaten__date=today)

        if not meals_today:
            return round(total_protein, 1)
        else:
            for meal in meals_today:
                total_protein += meal.get_total_protein()
            return round(total_protein, 1)

    def get_calories_burned_today(self, trainee: Trainee):
        total_calories = 0
        today = date.today()
        performed_workout_today = PerformedWorkout.objects.filter(
            trainee=trainee, time_performed__date=today)

        if not performed_workout_today:
            return total_calories
        else:
            for performed_workout in performed_workout_today:
                total_calories += performed_workout.get_total_calories()
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

    def get_carbs_needs(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.carbs_ratio / 4, 1))

    def get_fats_needs(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.fats_ratio / 9, 1))

    def get_protein_needs(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.protein_ratio / 4, 1))

    class Meta:
        model = Trainee
        fields = ['birthdate', 'gender', 'height', 'weight', 'daily_calories_needs',
                  'calories_intake_today', 'calories_burned_today',
                  'daily_water_needs', 'water_intake_today',
                  'carbs_ratio', 'fats_ratio', 'protein_ratio',
                  'carbs_needs', 'fats_needs', 'protein_needs',
                  'carbs_intake_today', 'fats_intake_today', 'protein_intake_today',
                  'activity_level', 'goal', 'daily_streak', 'image']


class TraineeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = ['birthdate', 'gender', 'height',
                  'weight', 'activity_level', 'goal', 'image']

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

    def validate(self, attrs):
        carbs_ratio = attrs['carbs_ratio']
        fats_ratio = attrs['fats_ratio']
        protein_ratio = attrs['protein_ratio']

        if ((carbs_ratio + fats_ratio + protein_ratio) != 1.0):
            raise serializers.ValidationError(
                'Macronutrients(carbs, fats, protein) ratios are not valid.'
            )

        return super().validate(attrs)
