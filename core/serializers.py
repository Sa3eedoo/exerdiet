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
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    daily_streak = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trainee
        fields = ['id', 'user_id', 'birthdate', 'gender', 'height', 'weight', 'daily_calories_needs', 'daily_water_needs',
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
