from model_bakery import baker
from rest_framework import status
import pytest
from core.models import User, Trainee


@pytest.fixture
def create_custom_food(api_client):
    def do_create_custom_food(custom_food):
        return api_client.post('/diet/custom_foods/', custom_food)
    return do_create_custom_food


@pytest.mark.django_db
class TestCreateCustomFood:
    def test_if_user_is_anonymous_retruns_401(self, create_custom_food):
        response = create_custom_food({
            "name": "a",
            "calories": 0,
            "carbs": 0,
            "fats": 0,
            "protein": 0
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_invalid_retruns_400(self, authenticate_with_trainee, create_custom_food):
        authenticate_with_trainee()

        response = create_custom_food({
            "name": "",
            "calories": 0,
            "carbs": 0,
            "fats": 0,
            "protein": 0
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    def test_if_user_is_authenticated_and_data_is_valid_retruns_201(self, authenticate_with_trainee, create_custom_food):
        authenticate_with_trainee()

        response = create_custom_food({
            "name": "a",
            "calories": 0,
            "carbs": 0,
            "fats": 0,
            "protein": 0
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
