from model_bakery import baker
from rest_framework import status
import pytest
from core.models import Trainee
from diet.models import CustomFood


@pytest.fixture
def create_custom_food(api_client):
    def do_create_custom_food(custom_food):
        return api_client.post('/diet/custom_foods/', custom_food)
    return do_create_custom_food


@pytest.fixture
def retrieve_custom_food(api_client):
    def do_retrieve_custom_food(id):
        return api_client.get(f'/diet/custom_foods/{id}/')
    return do_retrieve_custom_food


@pytest.fixture
def list_custom_food(api_client):
    def do_list_custom_food():
        return api_client.get('/diet/custom_foods/')
    return do_list_custom_food


@pytest.fixture
def delete_custom_food(api_client):
    def do_delete_custom_food(id):
        return api_client.delete(f'/diet/custom_foods/{id}/')
    return do_delete_custom_food


@pytest.fixture
def update_custom_food(api_client):
    def do_update_custom_food(id, custom_food):
        return api_client.patch(f'/diet/custom_foods/{id}/', custom_food)
    return do_update_custom_food


@pytest.mark.django_db
class TestCreateCustomFood:
    def test_if_user_is_anonymous_returns_401(self, create_custom_food):
        response = create_custom_food({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_invalid_returns_400(self, authenticate_with_trainee, create_custom_food):
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

    def test_if_user_is_authenticated_and_data_is_valid_returns_201(self, authenticate_with_trainee, create_custom_food):
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


@pytest.mark.django_db
class TestRetrieveCustomFood:
    def test_if_user_is_anonymous_returns_401(self, retrieve_custom_food):
        response = retrieve_custom_food(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_custom_food_Not_exists_returns_404(self, retrieve_custom_food, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_custom_food(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_custom_food_exists_with_same_trainee_returns_200(self, api_client, retrieve_custom_food):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        custom_food = baker.make(CustomFood, trainee=trainee)

        response = retrieve_custom_food(custom_food.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": custom_food.id,
            "name": custom_food.name,
            "category": custom_food.category,
            "calories": custom_food.calories,
            "carbs": custom_food.carbs,
            "fats": custom_food.fats,
            "protein": custom_food.protein,
            "image": custom_food.image
        }

    def test_if_custom_food_exists_with_other_trainee_returns_404(self, api_client, retrieve_custom_food):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        custom_food = baker.make(CustomFood, trainee=trainees[1])

        response = retrieve_custom_food(custom_food.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListCustomFood:
    def test_if_user_is_anonymous_returns_401(self, list_custom_food):
        response = list_custom_food()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, list_custom_food):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        custom_food = baker.make(CustomFood, trainee=trainee)

        response = list_custom_food()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0] == {
            "id": custom_food.id,
            "name": custom_food.name,
            "category": custom_food.category,
            "calories": custom_food.calories,
            "carbs": custom_food.carbs,
            "fats": custom_food.fats,
            "protein": custom_food.protein,
            "image": custom_food.image
        }


@pytest.mark.django_db
class TestDeleteCustomFood:
    def test_if_user_is_anonymous_returns_401(self, delete_custom_food):
        response = delete_custom_food(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_custom_food_Not_exists_returns_404(self, delete_custom_food, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_custom_food(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_custom_food_exists_with_same_trainee_returns_204(self, api_client, delete_custom_food):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        custom_food = baker.make(CustomFood, trainee=trainee)

        response = delete_custom_food(custom_food.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_custom_food_exists_with_other_trainee_returns_404(self, api_client, delete_custom_food):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        custom_food = baker.make(CustomFood, trainee=trainees[1])

        response = delete_custom_food(custom_food.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateCustomFood:
    def test_if_user_is_anonymous_returns_401(self, update_custom_food):
        response = update_custom_food(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_custom_food_Not_exists_returns_404(self, update_custom_food, authenticate_with_trainee):
        authenticate_with_trainee()

        response = update_custom_food(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_custom_food_exists_with_same_trainee_returns_200(self, api_client, update_custom_food):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        custom_food = baker.make(CustomFood, trainee=trainee, name='food_1')

        response = update_custom_food(custom_food.id, {'name': 'food_2'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'food_2'

    def test_if_custom_food_exists_with_other_trainee_returns_404(self, api_client, update_custom_food):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        custom_food = baker.make(CustomFood, trainee=trainees[1])

        response = update_custom_food(custom_food.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND
