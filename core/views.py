from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import Trainee
from .serializers import TraineeSerializer


class TraineeViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
