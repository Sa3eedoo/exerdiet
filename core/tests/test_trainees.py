from decimal import Decimal
from model_bakery import baker
from rest_framework import status
import pytest
from core.models import Trainee


@pytest.fixture
def create_trainee(api_client):
    def do_create_trainee(trainee):
        return api_client.post('/core/trainees/', trainee)
    return do_create_trainee


@pytest.fixture
def retrieve_trainee(api_client):
    def do_retrieve_trainee():
        return api_client.get('/core/trainees/me/')
    return do_retrieve_trainee


@pytest.mark.django_db
class TestCreateTrainee:
    def test_if_user_is_anonymous_returns_401(self, create_trainee):
        response = create_trainee({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_has_trainee_returns_403(self, create_trainee, authenticate_with_trainee):
        authenticate_with_trainee()

        response = create_trainee({
            "birthdate": "2000-02-07",
            "gender": "M",
            "height": 170,
            "weight": 65
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_has_no_trainee_returns_201(self, create_trainee, authenticate_without_trainee):
        authenticate_without_trainee()

        response = create_trainee({
            "birthdate": "2000-02-07",
            "gender": "M",
            "height": 170,
            "weight": 65
        })

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveTrainee:
    def test_if_user_is_anonymous_returns_401(self, retrieve_trainee):
        response = retrieve_trainee()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_has_trainee_returns_200(self, retrieve_trainee, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_trainee()

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_authenticated_and_has_no_trainee_returns_200(self, retrieve_trainee, authenticate_without_trainee):
        authenticate_without_trainee()

        response = retrieve_trainee()

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateTrainee:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.patch('/core/trainees/me/', {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_user_if_data_is_valid_returns_200(self, api_client):
        trainee = baker.make(Trainee)
        trainee.gender = 'M'
        api_client.force_authenticate(user=trainee.user)

        response = api_client.patch('/core/trainees/me/', {"gender": "F"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['gender'] == 'F'

    def test_reset_daily_calories_needs_of_user_returns_200(self, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)

        response = api_client.get('/core/trainees/reset_daily_calories_needs/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['daily_calories_needs'] == trainee.calculate_daily_calories_needs(
        )

    def test_reset_daily_water_needs_of_user_returns_200(self, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)

        response = api_client.get('/core/trainees/reset_daily_water_needs/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['daily_water_needs'] == int(trainee.calculate_daily_water_needs(
        ))

    def test_reset_macronutrients_ratios_of_user_returns_200(self, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)

        response = api_client.get(
            '/core/trainees/reset_macronutrients_ratios/')

        assert response.status_code == status.HTTP_200_OK

    def test_set_daily_calories_needs_of_user_returns_200(self, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)

        response = api_client.patch('/core/trainees/set_daily_calories_needs/', {
            "daily_calories_needs": trainee.calculate_daily_calories_needs() + 1

        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['daily_calories_needs'] == trainee.calculate_daily_calories_needs(
        ) + 1

    def test_set_daily_water_needs_of_user_returns_200(self, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)

        response = api_client.patch('/core/trainees/set_daily_water_needs/', {
            "daily_water_needs": int(trainee.calculate_daily_water_needs()) + 1
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['daily_water_needs'] == int(trainee.calculate_daily_water_needs(
        )) + 1

    def test_set_macronutrients_ratios_of_user_returns_200(self, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)

        response = api_client.patch('/core/trainees/set_macronutrients_ratios/', {
            "carbs_ratio": 0.5,
            "fats_ratio": 0.2,
            "protein_ratio": 0.3
        })

        assert response.status_code == status.HTTP_200_OK
