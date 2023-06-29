from rest_framework import status
import pytest
from core.models import User


@pytest.fixture
def create_food(api_client):
    def do_create_food(food):
        return api_client.post('/diet/foods/', food)
    return do_create_food


@ pytest.mark.django_db
class TestCreateFood:
    def test_if_user_is_anonymous_retruns_401(self, create_food):
        response = create_food({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_retruns_405(self, authenticate_with_trainee, create_food):
        authenticate_with_trainee()

        response = create_food({})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
