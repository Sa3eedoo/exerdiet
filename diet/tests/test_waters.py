from model_bakery import baker
from rest_framework import status
import pytest
from core.models import Trainee
from diet.models import Water


@pytest.fixture
def create_water(api_client):
    def do_create_water(water):
        return api_client.post('/diet/waters/', water)
    return do_create_water


@pytest.fixture
def retrieve_water(api_client):
    def do_retrieve_water(id):
        return api_client.get(f'/diet/waters/{id}/')
    return do_retrieve_water


@pytest.fixture
def list_water(api_client):
    def do_list_water():
        return api_client.get('/diet/waters/')
    return do_list_water


@pytest.fixture
def delete_water(api_client):
    def do_delete_water(id):
        return api_client.delete(f'/diet/waters/{id}/')
    return do_delete_water


@pytest.fixture
def update_water(api_client):
    def do_update_water(id, water):
        return api_client.patch(f'/diet/waters/{id}/', water)
    return do_update_water


@pytest.mark.django_db
class TestCreateWater:
    def test_if_user_is_anonymous_returns_401(self, create_water):
        response = create_water({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_invalid_returns_400(self, authenticate_with_trainee, create_water):
        authenticate_with_trainee()

        response = create_water({'amount': -1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['amount'] is not None

    def test_if_user_is_authenticated_and_data_is_valid_returns_201(self, authenticate_with_trainee, create_water):
        authenticate_with_trainee()

        response = create_water({'amount': 100})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveWater:
    def test_if_user_is_anonymous_returns_401(self, retrieve_water):
        response = retrieve_water(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_water_Not_exists_returns_404(self, retrieve_water, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_water(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_water_exists_with_same_trainee_returns_200(self, api_client, retrieve_water):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        water = baker.make(Water, trainee=trainee)

        response = retrieve_water(water.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": water.id,
            "amount": water.amount,
            "drinking_date": response.data['drinking_date']
        }

    def test_if_water_exists_with_other_trainee_returns_404(self, api_client, retrieve_water):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        water = baker.make(Water, trainee=trainees[1])

        response = retrieve_water(water.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListWater:
    def test_if_user_is_anonymous_returns_401(self, list_water):
        response = list_water()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, list_water):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        water = baker.make(Water, trainee=trainee)

        response = list_water()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0] == {
            "id": water.id,
            "amount": water.amount,
            "drinking_date": response.data['results'][0]['drinking_date']
        }


@pytest.mark.django_db
class TestDeleteWater:
    def test_if_user_is_anonymous_returns_401(self, delete_water):
        response = delete_water(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_water_Not_exists_returns_404(self, delete_water, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_water(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_water_exists_with_same_trainee_returns_204(self, api_client, delete_water):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        water = baker.make(Water, trainee=trainee)

        response = delete_water(water.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_water_exists_with_other_trainee_returns_404(self, api_client, delete_water):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        water = baker.make(Water, trainee=trainees[1])

        response = delete_water(water.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateWater:
    def test_if_user_is_anonymous_returns_401(self, update_water):
        response = update_water(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_water_Not_exists_returns_404(self, update_water, authenticate_with_trainee):
        authenticate_with_trainee()

        response = update_water(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_water_exists_with_same_trainee_returns_200(self, api_client, update_water):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        water = baker.make(Water, trainee=trainee, amount=100)

        response = update_water(water.id, {'amount': 200})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['amount'] == 200

    def test_if_water_exists_with_other_trainee_returns_404(self, api_client, update_water):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        water = baker.make(Water, trainee=trainees[1])

        response = update_water(water.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND
