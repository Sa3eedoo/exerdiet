from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Trainee
from .permissions import IsAuthenticatedAndNotTrainee, IsAuthenticatedAndTrainee
from .serializers import TraineeSerializer


class TraineeViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticatedAndNotTrainee()]
        if self.action == 'me':
            return [IsAuthenticatedAndTrainee()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'])
    def me(self, request):
        trainee = Trainee.objects.get(user_id=request.user.id)
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
