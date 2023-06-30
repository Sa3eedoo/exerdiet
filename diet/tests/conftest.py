from model_bakery import baker
from rest_framework.test import APIClient
import pytest
from core.models import User, Trainee


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate_without_trainee(api_client):
    def do_authenticate_without_trainee(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate_without_trainee


@pytest.fixture
def authenticate_with_trainee(api_client):
    def do_authenticate_with_trainee(is_staff=False):
        trainee = baker.make(Trainee)
        trainee.user.is_staff = is_staff
        return api_client.force_authenticate(user=trainee.user)
    return do_authenticate_with_trainee
