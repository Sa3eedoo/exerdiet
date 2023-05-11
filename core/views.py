from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from .models import Trainee
from .permissions import IsAuthenticatedAndNotTrainee, IsAuthenticatedAndTrainee
from .serializers import TraineeSerializer, TraineeCreateSerializer, TraineeUpdateSerializer, TraineeUpdateCaloriesSerializer, TraineeUpdateWaterSerializer, TraineeUpdateMacronutrientsRatiosSerializer


class TraineeViewSet(CreateModelMixin, GenericViewSet):
    queryset = Trainee.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TraineeCreateSerializer
        elif self.request.method == 'PATCH':
            if self.action == 'me':
                return TraineeUpdateSerializer
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
        if self.action in ['me', 'reset_daily_calories_needs',
                           'reset_daily_water_needs', 'reset_macronutrients_ratios',
                           'set_daily_calories_needs', 'set_daily_water_needs', 'set_macronutrients_ratios']:
            return [IsAuthenticatedAndTrainee()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PATCH', 'DELETE'])
    def me(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
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
        trainee = Trainee.objects.get(user_id=request.user.id)
        trainee.is_daily_calories_needs_custom = False
        serializer = TraineeUpdateCaloriesSerializer(trainee)
        trainee.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PATCH'])
    def set_daily_calories_needs(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
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
        trainee = Trainee.objects.get(user_id=request.user.id)
        trainee.is_daily_water_needs_custom = False
        serializer = TraineeUpdateWaterSerializer(trainee)
        trainee.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PATCH'])
    def set_daily_water_needs(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
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
        trainee = Trainee.objects.get(user_id=request.user.id)
        trainee.is_macronutrients_ratios_custom = False
        serializer = TraineeUpdateMacronutrientsRatiosSerializer(trainee)
        trainee.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PATCH'])
    def set_macronutrients_ratios(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
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
