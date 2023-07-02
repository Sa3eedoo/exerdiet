from model_bakery import baker
from rest_framework import status
import pytest
from diet.models import Food


@pytest.fixture
def create_food(api_client):
    def do_create_food(food):
        return api_client.post('/diet/foods/', food)
    return do_create_food


@pytest.fixture
def retrieve_food(api_client):
    def do_retrieve_food(id):
        return api_client.get(f'/diet/foods/{id}/')
    return do_retrieve_food


@pytest.fixture
def list_food(api_client):
    def do_list_food():
        return api_client.get('/diet/foods/')
    return do_list_food


@pytest.mark.django_db
class TestCreateFood:
    def test_if_user_is_anonymous_returns_401(self, create_food):
        response = create_food({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_405(self, authenticate_with_trainee, create_food):
        authenticate_with_trainee()

        response = create_food({})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestRetrieveFood:
    def test_if_user_is_anonymous_returns_401(self, retrieve_food):
        response = retrieve_food(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_food_Not_exists_returns_404(self, retrieve_food, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_food(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_exists_returns_200(self, retrieve_food, authenticate_with_trainee):
        authenticate_with_trainee()
        food = baker.make(Food)

        response = retrieve_food(food.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": food.id,
            "name": food.name,
            "category": food.category,
            "calories": food.calories,
            "carbs": food.carbs,
            "fats": food.fats,
            "protein": food.protein,
            "image": food.image
        }


@pytest.mark.django_db
class TestListFood:
    def test_if_user_is_anonymous_returns_401(self, list_food):
        response = list_food()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, authenticate_with_trainee, list_food):
        authenticate_with_trainee()
        food = baker.make(Food)

        response = list_food()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0] == {
            "id": food.id,
            "name": food.name,
            "category": food.category,
            "calories": food.calories,
            "carbs": food.carbs,
            "fats": food.fats,
            "protein": food.protein,
            "image": food.image
        }
