from decimal import Decimal
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
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
    daily_streak = serializers.IntegerField(read_only=True)
    calories_intake_today = serializers.SerializerMethodField(read_only=True)
    calories_burned_today = serializers.SerializerMethodField(read_only=True)
    carbs_calories = serializers.SerializerMethodField(read_only=True)
    fats_calories = serializers.SerializerMethodField(read_only=True)
    protein_calories = serializers.SerializerMethodField(read_only=True)
    carbs_grams = serializers.SerializerMethodField(read_only=True)
    fats_grams = serializers.SerializerMethodField(read_only=True)
    protein_grams = serializers.SerializerMethodField(read_only=True)

    def get_calories_intake_today(self, trainee: Trainee):
        return 0

    def get_calories_burned_today(self, trainee: Trainee):
        return 0

    def get_carbs_calories(self, trainee: Trainee):
        return int(trainee.daily_calories_needs * trainee.carbs_ratio)

    def get_fats_calories(self, trainee: Trainee):
        return int(trainee.daily_calories_needs * trainee.fats_ratio)

    def get_protein_calories(self, trainee: Trainee):
        return int(trainee.daily_calories_needs * trainee.protein_ratio)

    def get_carbs_grams(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.carbs_ratio / 4, 1))

    def get_fats_grams(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.fats_ratio / 9, 1))

    def get_protein_grams(self, trainee: Trainee):
        return Decimal(round(trainee.daily_calories_needs * trainee.protein_ratio / 4, 1))

    class Meta:
        model = Trainee
        fields = ['birthdate', 'gender', 'height', 'weight', 'daily_calories_needs',
                  'is_daily_calories_needs_custom', 'calories_intake_today', 'calories_burned_today',
                  'daily_water_needs', 'is_daily_water_needs_custom', 'water_intake_today', 'carbs_ratio',
                  'fats_ratio', 'protein_ratio', 'is_macronutrients_ratios_custom', 'carbs_calories',
                  'fats_calories', 'protein_calories', 'carbs_grams', 'fats_grams', 'protein_grams',
                  'daily_streak', 'activity_level', 'goal']


class TraineeCreateSerializer(serializers.ModelSerializer):
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
