from model_bakery import baker
from rest_framework import status
import pytest
from core.models import Trainee
from diet.models import Recipe


@pytest.fixture
def create_recipe(api_client):
    def do_create_recipe(recipe):
        return api_client.post('/diet/recipes/', recipe)
    return do_create_recipe


@pytest.fixture
def retrieve_recipe(api_client):
    def do_retrieve_recipe(id):
        return api_client.get(f'/diet/recipes/{id}/')
    return do_retrieve_recipe


@pytest.fixture
def list_recipe(api_client):
    def do_list_recipe():
        return api_client.get('/diet/recipes/')
    return do_list_recipe


@pytest.fixture
def delete_recipe(api_client):
    def do_delete_recipe(id):
        return api_client.delete(f'/diet/recipes/{id}/')
    return do_delete_recipe


@pytest.fixture
def update_recipe(api_client):
    def do_update_recipe(id, recipe):
        return api_client.patch(f'/diet/recipes/{id}/', recipe)
    return do_update_recipe


@pytest.mark.django_db
class TestCreateRecipe:
    def test_if_user_is_anonymous_returns_401(self, create_recipe):
        response = create_recipe({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_invalid_returns_400(self, authenticate_with_trainee, create_recipe):
        authenticate_with_trainee()

        response = create_recipe({
            "name": "",
            "instructions": "b"
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    def test_if_user_is_authenticated_and_data_is_valid_returns_201(self, authenticate_with_trainee, create_recipe):
        authenticate_with_trainee()

        response = create_recipe({
            "name": "a",
            "instructions": "b"
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveRecipe:
    def test_if_user_is_anonymous_returns_401(self, retrieve_recipe):
        response = retrieve_recipe(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_recipe_Not_exists_returns_404(self, retrieve_recipe, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_recipe(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_recipe_exists_with_same_trainee_returns_200(self, api_client, retrieve_recipe):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        recipe = baker.make(Recipe, trainee=trainee)

        response = retrieve_recipe(recipe.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": recipe.id,
            "name": recipe.name,
            "instructions": recipe.instructions,
            "image": recipe.image,
            "food_instances": [],
            "total_calories": 0,
            "total_carbs": 0,
            "total_fats": 0,
            "total_protein": 0
        }

    def test_if_recipe_exists_with_other_trainee_returns_404(self, api_client, retrieve_recipe):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        recipe = baker.make(Recipe, trainee=trainees[1])

        response = retrieve_recipe(recipe.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListRecipe:
    def test_if_user_is_anonymous_returns_401(self, list_recipe):
        response = list_recipe()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, authenticate_with_trainee, list_recipe):
        authenticate_with_trainee()

        response = list_recipe()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteRecipe:
    def test_if_user_is_anonymous_returns_401(self, delete_recipe):
        response = delete_recipe(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_recipe_Not_exists_returns_404(self, delete_recipe, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_recipe(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_recipe_exists_with_same_trainee_returns_204(self, api_client, delete_recipe):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        recipe = baker.make(Recipe, trainee=trainee)

        response = delete_recipe(recipe.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_recipe_exists_with_other_trainee_returns_404(self, api_client, delete_recipe):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        recipe = baker.make(Recipe, trainee=trainees[1])

        response = delete_recipe(recipe.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateRecipe:
    def test_if_user_is_anonymous_returns_401(self, update_recipe):
        response = update_recipe(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_recipe_Not_exists_returns_404(self, update_recipe, authenticate_with_trainee):
        authenticate_with_trainee()

        response = update_recipe(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_recipe_exists_with_same_trainee_returns_200(self, api_client, update_recipe):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        recipe = baker.make(Recipe, trainee=trainee, name='recipe_1')

        response = update_recipe(recipe.id, {'name': 'recipe_2'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'recipe_2'

    def test_if_recipe_exists_with_other_trainee_returns_404(self, api_client, update_recipe):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        recipe = baker.make(Recipe, trainee=trainees[1])

        response = update_recipe(recipe.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND
