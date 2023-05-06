from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import Trainee


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['username', 'email', 'first_name', 'last_name']


class TraineeSerializer(serializers.ModelSerializer):
    daily_streak = serializers.IntegerField(read_only=True)
    calories_intake_today = serializers.SerializerMethodField(read_only=True)

    def get_calories_intake_today(self, trainee: Trainee):
        return 0

    class Meta:
        model = Trainee
        fields = ['birthdate', 'gender', 'height', 'weight', 'daily_calories_needs', 'calories_intake_today', 'daily_water_needs',
                  'water_intake_today', 'carbs_ratio', 'fats_ratio', 'protein_ratio', 'daily_streak', 'activity_level', 'goal']


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
