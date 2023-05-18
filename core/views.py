from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from .models import Trainee
from .permissions import IsAuthenticatedAndNotTrainee
from .serializers import TraineeSerializer, TraineeCreateUpdateSerializer, TraineeUpdateCaloriesSerializer, TraineeUpdateWaterSerializer, TraineeUpdateMacronutrientsRatiosSerializer


class TraineeViewSet(CreateModelMixin, GenericViewSet):
    def get_queryset(self):
        return Trainee.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TraineeCreateUpdateSerializer
        elif self.request.method == 'PATCH':
            if self.action == 'me':
                return TraineeCreateUpdateSerializer
            elif self.action == 'set_daily_calories_needs':
                return TraineeUpdateCaloriesSerializer
            elif self.action == 'set_daily_water_needs':
                return TraineeUpdateWaterSerializer
            elif self.action == 'set_macronutrients_ratios':
                return TraineeUpdateMacronutrientsRatiosSerializer

        return TraineeSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticatedAndNotTrainee()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PATCH', 'DELETE'])
    def me(self, request):
        trainee = get_object_or_404(Trainee, user_id=request.user.id)
        if request.method == 'GET':
            serializer = TraineeSerializer(trainee)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = TraineeSerializer(trainee,
                                           data=request.data,
                                           partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            trainee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def reset_daily_calories_needs(self, request):
        trainee = get_object_or_404(Trainee, user_id=request.user.id)
        trainee.is_daily_calories_needs_custom = False
        serializer = TraineeUpdateCaloriesSerializer(trainee)
        trainee.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PATCH'])
    def set_daily_calories_needs(self, request):
        trainee = get_object_or_404(Trainee, user_id=request.user.id)
        if request.method == 'GET':
            serializer = TraineeUpdateCaloriesSerializer(trainee)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = TraineeUpdateCaloriesSerializer(trainee,
                                                         data=request.data,
                                                         partial=True)
            trainee.is_daily_calories_needs_custom = True
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def reset_daily_water_needs(self, request):
        trainee = get_object_or_404(Trainee, user_id=request.user.id)
        trainee.is_daily_water_needs_custom = False
        serializer = TraineeUpdateWaterSerializer(trainee)
        trainee.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PATCH'])
    def set_daily_water_needs(self, request):
        trainee = get_object_or_404(Trainee, user_id=request.user.id)
        if request.method == 'GET':
            serializer = TraineeUpdateWaterSerializer(trainee)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = TraineeUpdateWaterSerializer(trainee,
                                                      data=request.data,
                                                      partial=True)
            trainee.is_daily_water_needs_custom = True
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def reset_macronutrients_ratios(self, request):
        trainee = get_object_or_404(Trainee, user_id=request.user.id)
        trainee.is_macronutrients_ratios_custom = False
        serializer = TraineeUpdateMacronutrientsRatiosSerializer(trainee)
        trainee.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PATCH'])
    def set_macronutrients_ratios(self, request):
        trainee = get_object_or_404(Trainee, user_id=request.user.id)
        if request.method == 'GET':
            serializer = TraineeUpdateMacronutrientsRatiosSerializer(trainee)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = TraineeUpdateMacronutrientsRatiosSerializer(trainee,
                                                                     data=request.data,
                                                                     partial=True)
            trainee.is_macronutrients_ratios_custom = True
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
