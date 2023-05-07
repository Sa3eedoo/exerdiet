from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from .models import Trainee
from .permissions import IsAuthenticatedAndNotTrainee, IsAuthenticatedAndTrainee
from .serializers import TraineeSerializer, TraineeCreateSerializer


class TraineeViewSet(CreateModelMixin, GenericViewSet):
    queryset = Trainee.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TraineeCreateSerializer
        return TraineeSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticatedAndNotTrainee()]
        if self.action in ['me', 'reset_daily_calories_needs', 'reset_daily_water_needs', 'reset_macronutrients_ratios']:
            return [IsAuthenticatedAndTrainee()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PATCH', 'DELETE'])
    def me(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = TraineeSerializer(trainee)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            partial = True if request.method == 'PATCH' else False
            serializer = TraineeSerializer(
                trainee, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            trainee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def reset_daily_calories_needs(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
        trainee.daily_calories_needs = trainee.calculate_daily_calories_needs()
        serializer = TraineeSerializer(trainee)
        trainee.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def reset_daily_water_needs(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
        trainee.daily_water_needs = trainee.calculate_daily_water_needs()
        serializer = TraineeSerializer(trainee)
        trainee.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def reset_macronutrients_ratios(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
        trainee.carbs_ratio, trainee.fats_ratio, trainee.protein_ratio = trainee.get_default_macronutrients_ratios()
        serializer = TraineeSerializer(trainee)
        trainee.save()
        return Response(serializer.data)
