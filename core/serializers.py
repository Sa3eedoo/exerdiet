from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import Trainee


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TraineeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    daily_streak = serializers.IntegerField(read_only=True)
    activity_level = serializers.CharField(source='get_activity_level_display')
    goal = serializers.CharField(source='get_goal_display')

    class Meta:
        model = Trainee
        fields = ['id', 'user_id', 'birthdate', 'height', 'weight', 'daily_calories_needs', 'daily_water_needs',
                  'daily_water_intake', 'carbs_ratio', 'fats_ratio', 'protein_ratio', 'daily_streak', 'activity_level', 'goal']
