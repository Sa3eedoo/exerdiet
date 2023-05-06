from rest_framework import permissions
from .models import Trainee


class IsAuthenticatedAndNotTrainee(permissions.BasePermission):
    def has_permission(self, request, view):
        is_trainee = Trainee.objects.filter(user=request.user.id).exists()
        print(bool(request.user and request.user.is_authenticated and not is_trainee))
        return bool(request.user and request.user.is_authenticated and not is_trainee)
