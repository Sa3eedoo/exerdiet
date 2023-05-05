from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Trainee
from .serializers import TraineeSerializer


class TraineeViewSet(ModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.user.is_authenticated:
            trainee = get_object_or_404(Trainee, user_id=request.user.id)
            if request.method == 'GET':
                serializer = TraineeSerializer(trainee)
                return Response(serializer.data)
            elif request.method == 'PUT' or request.method == 'PATCH':
                partial = True if request.method == 'PATCH' else False
                serializer = TraineeSerializer(
                    trainee, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'detail': 'Authentication credentials were not provided.'})
