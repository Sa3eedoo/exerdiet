from model_bakery import baker
from rest_framework import status
import pytest
from core.models import Trainee
from diet.models import Meal, Food, CustomFood, FoodInstance, Recipe


@pytest.fixture
def create_meal(api_client):
    def do_create_meal(meal):
        return api_client.post('/diet/meals/', meal)
    return do_create_meal


@pytest.fixture
def retrieve_meal(api_client):
    def do_retrieve_meal(id):
        return api_client.get(f'/diet/meals/{id}/')
    return do_retrieve_meal


@pytest.fixture
def list_meal(api_client):
    def do_list_meal():
        return api_client.get('/diet/meals/')
    return do_list_meal


@pytest.fixture
def delete_meal(api_client):
    def do_delete_meal(id):
        return api_client.delete(f'/diet/meals/{id}/')
    return do_delete_meal


@pytest.fixture
def update_meal(api_client):
    def do_update_meal(id, meal):
        return api_client.patch(f'/diet/meals/{id}/', meal)
    return do_update_meal


@pytest.fixture
def create_food_instance(api_client):
    def do_create_food_instance(meal_id, food_instance):
        return api_client.post(f'/diet/meals/{meal_id}/food_instances/', food_instance)
    return do_create_food_instance


@pytest.fixture
def retrieve_food_instance(api_client):
    def do_retrieve_food_instance(meal_id, food_instance_id):
        return api_client.get(f'/diet/meals/{meal_id}/food_instances/{food_instance_id}/')
    return do_retrieve_food_instance


@pytest.fixture
def list_food_instance(api_client):
    def do_list_food_instance(meal_id):
        return api_client.get(f'/diet/meals/{meal_id}/food_instances/')
    return do_list_food_instance


@pytest.fixture
def delete_food_instance(api_client):
    def do_delete_food_instance(meal_id, food_instance_id):
        return api_client.delete(f'/diet/meals/{meal_id}/food_instances/{food_instance_id}/')
    return do_delete_food_instance


@pytest.fixture
def update_food_instance(api_client):
    def do_update_food_instance(meal_id, food_instance_id, food_instance):
        return api_client.patch(f'/diet/meals/{meal_id}/food_instances/{food_instance_id}/', food_instance)
    return do_update_food_instance


@pytest.fixture
def create_recipe(api_client):
    def do_create_recipe(meal_id, recipe):
        return api_client.post(f'/diet/meals/{meal_id}/recipes/', recipe)
    return do_create_recipe


@pytest.fixture
def retrieve_recipe(api_client):
    def do_retrieve_recipe(meal_id, recipe_id):
        return api_client.get(f'/diet/meals/{meal_id}/recipes/{recipe_id}/')
    return do_retrieve_recipe


@pytest.fixture
def list_recipe(api_client):
    def do_list_recipe(meal_id):
        return api_client.get(f'/diet/meals/{meal_id}/recipes/')
    return do_list_recipe


@pytest.fixture
def delete_recipe(api_client):
    def do_delete_recipe(meal_id, recipe_id):
        return api_client.delete(f'/diet/meals/{meal_id}/recipes/{recipe_id}/')
    return do_delete_recipe


@pytest.mark.django_db
class TestCreateMeal:
    def test_if_user_is_anonymous_returns_401(self, create_meal):
        response = create_meal({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_valid_returns_201(self, authenticate_with_trainee, create_meal):
        authenticate_with_trainee()

        response = create_meal({
            "name": "a"
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveMeal:
    def test_if_user_is_anonymous_returns_401(self, retrieve_meal):
        response = retrieve_meal(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_meal_Not_exists_returns_404(self, retrieve_meal, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_meal(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_meal_exists_with_same_trainee_returns_200(self, api_client, retrieve_meal):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)

        response = retrieve_meal(meal.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": meal.id,
            "name": meal.name,
            "time_eaten": response.data["time_eaten"],
            "recipes": [],
            "food_instances": [],
            "total_calories": 0,
            "total_carbs": 0,
            "total_fats": 0,
            "total_protein": 0
        }

    def test_if_meal_exists_with_other_trainee_returns_404(self, api_client, retrieve_meal):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        meal = baker.make(Meal, trainee=trainees[1])

        response = retrieve_meal(meal.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListMeal:
    def test_if_user_is_anonymous_returns_401(self, list_meal):
        response = list_meal()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, list_meal):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)

        response = list_meal()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0] == {
            "id": meal.id,
            "name": meal.name,
            "time_eaten": response.data['results'][0]["time_eaten"],
            "recipes": [],
            "food_instances": [],
            "total_calories": meal.get_total_calories(),
            "total_carbs": meal.get_total_carbs(),
            "total_fats": meal.get_total_fats(),
            "total_protein": meal.get_total_protein()
        }


@pytest.mark.django_db
class TestDeleteMeal:
    def test_if_user_is_anonymous_returns_401(self, delete_meal):
        response = delete_meal(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_meal_Not_exists_returns_404(self, delete_meal, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_meal(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_meal_exists_with_same_trainee_returns_204(self, api_client, delete_meal):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)

        response = delete_meal(meal.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_meal_exists_with_other_trainee_returns_404(self, api_client, delete_meal):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        meal = baker.make(Meal, trainee=trainees[1])

        response = delete_meal(meal.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateMeal:
    def test_if_user_is_anonymous_returns_401(self, update_meal):
        response = update_meal(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_meal_Not_exists_returns_404(self, update_meal, authenticate_with_trainee):
        authenticate_with_trainee()

        response = update_meal(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_meal_exists_with_same_trainee_returns_200(self, api_client, update_meal):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee, name='meal_1')

        response = update_meal(meal.id, {'name': 'meal_2'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'meal_2'

    def test_if_meal_exists_with_other_trainee_returns_404(self, api_client, update_meal):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        meal = baker.make(Meal, trainee=trainees[1])

        response = update_meal(meal.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateFoodInstance:
    def test_if_user_is_anonymous_returns_401(self, create_food_instance):
        response = create_food_instance(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_201(self, api_client, create_food_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        food = baker.make(Food)

        response = create_food_instance(meal.id, {
            "food_id": food.id,
            "quantity": 100
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    def test_if_data_is_invalid_returns_400(self, authenticate_with_trainee, create_food_instance):
        authenticate_with_trainee()
        meal = baker.make(Meal)

        response = create_food_instance(meal.id, {
            "food_id": 1,
            "quantity": 1
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['food_id'] is not None

    def test_if_meal_not_exists_returns_404(self, api_client, create_food_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        food = baker.make(Food)

        response = create_food_instance(1, {
            "food_id": food.id,
            "quantity": 100
        })

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_custom_food_of_other_trainee_returns_400(self, api_client, create_food_instance):
        trainee = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainee[0].user)
        meal = baker.make(Meal, trainee=trainee[0])
        custom_food = baker.make(CustomFood, trainee=trainee[1])

        response = create_food_instance(meal.id, {
            "food_id": custom_food.id,
            "quantity": 100
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_meal_of_other_trainee_returns_404(self, api_client, create_food_instance):
        trainee = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainee[0].user)
        meal = baker.make(Meal, trainee=trainee[1])
        food = baker.make(Food)

        response = create_food_instance(meal.id, {
            "food_id": food.id,
            "quantity": 100
        })

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRetrieveFoodInstance:
    def test_if_user_is_anonymous_returns_401(self, retrieve_food_instance):
        response = retrieve_food_instance(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_meal_Not_exists_returns_404(self, retrieve_food_instance, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_food_instance(1, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_Not_exists_returns_404(self, retrieve_food_instance, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)

        response = retrieve_food_instance(meal.id, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_exists_with_same_meal_and_same_trainee_returns_200(self, api_client, retrieve_food_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        food_instance = baker.make(FoodInstance, meal=meal)

        response = retrieve_food_instance(meal.id, food_instance.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == food_instance.id
        assert response.data['food']['id'] == food_instance.food.id
        assert response.data['quantity'] == food_instance.quantity
        assert response.data['total_calories'] == food_instance.get_total_calories(
        )
        assert response.data['total_carbs'] == food_instance.get_total_carbs()
        assert response.data['total_fats'] == food_instance.get_total_fats()
        assert response.data['total_protein'] == food_instance.get_total_protein(
        )

    def test_if_food_instance_exists_with_other_meal_and_trainee_returns_404(self, api_client, retrieve_food_instance):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        meal = baker.make(Meal, trainee=trainees[1])
        food_instance = baker.make(FoodInstance, meal=meal)

        response = retrieve_food_instance(meal.id, food_instance.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_exists_with_other_meal_but_same_trainee_returns_404(self, api_client, retrieve_food_instance):
        trainees = baker.make(Trainee)
        api_client.force_authenticate(user=trainees.user)
        meal = baker.make(Meal, trainee=trainees, _quantity=2)
        food_instance = baker.make(FoodInstance, meal=meal[1])

        response = retrieve_food_instance(meal[0].id, food_instance.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListFoodInstance:
    def test_if_user_is_anonymous_returns_401(self, list_food_instance):
        response = list_food_instance(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, list_food_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        food_instances = baker.make(FoodInstance, meal=meal, _quantity=2)

        response = list_food_instance(meal.id)

        assert response.status_code == status.HTTP_200_OK
        for i in range(2):
            assert response.data[i]['id'] == food_instances[i].id
            assert response.data[i]['food']['id'] == food_instances[i].food.id
            assert response.data[i]['quantity'] == food_instances[i].quantity
            assert response.data[i]['total_calories'] == food_instances[i].get_total_calories(
            )
            assert response.data[i]['total_carbs'] == food_instances[i].get_total_carbs(
            )
            assert response.data[i]['total_fats'] == food_instances[i].get_total_fats(
            )
            assert response.data[i]['total_protein'] == food_instances[i].get_total_protein(
            )

    def test_if_meal_Not_exists_returns_404(self, list_food_instance, authenticate_with_trainee):
        authenticate_with_trainee()

        response = list_food_instance(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteFoodInstance:
    def test_if_user_is_anonymous_returns_401(self, delete_food_instance):
        response = delete_food_instance(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_meal_Not_exists_returns_404(self, delete_food_instance, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_food_instance(1, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_Not_exists_returns_404(self, delete_food_instance, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)

        response = delete_food_instance(meal.id, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_exists_with_same_meal_and_same_trainee_returns_204(self, api_client, delete_food_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        food_instance = baker.make(FoodInstance, meal=meal)

        response = delete_food_instance(meal.id, food_instance.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_food_instance_exists_with_other_meal_and_trainee_returns_404(self, api_client, delete_food_instance):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        meal = baker.make(Meal, trainee=trainees[1])
        food_instance = baker.make(FoodInstance, meal=meal)

        response = delete_food_instance(meal.id, food_instance.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_exists_with_other_meal_but_same_trainee_returns_404(self, api_client, delete_food_instance):
        trainees = baker.make(Trainee)
        api_client.force_authenticate(user=trainees.user)
        meal = baker.make(Meal, trainee=trainees, _quantity=2)
        food_instance = baker.make(FoodInstance, meal=meal[1])

        response = delete_food_instance(meal[0].id, food_instance.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateFoodInstance:
    def test_if_user_is_anonymous_returns_401(self, update_food_instance):
        response = update_food_instance(1, 1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_meal_Not_exists_returns_404(self, update_food_instance, authenticate_with_trainee):
        authenticate_with_trainee()

        response = update_food_instance(1, 1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_Not_exists_returns_404(self, update_food_instance, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)

        response = update_food_instance(meal.id, 1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_exists_with_same_meal_and_same_trainee_returns_200(self, api_client, update_food_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        food_instance = baker.make(FoodInstance, meal=meal, quantity=50.0)

        response = update_food_instance(
            meal.id, food_instance.id, {"quantity": 100.0}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['quantity'] == 100.0

    def test_if_food_instance_exists_with_other_meal_and_trainee_returns_404(self, api_client, update_food_instance):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        meal = baker.make(Meal, trainee=trainees[1])
        food_instance = baker.make(FoodInstance, meal=meal)

        response = update_food_instance(meal.id, food_instance.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_food_instance_exists_with_other_meal_but_same_trainee_returns_404(self, api_client, update_food_instance):
        trainees = baker.make(Trainee)
        api_client.force_authenticate(user=trainees.user)
        meal = baker.make(Meal, trainee=trainees, _quantity=2)
        food_instance = baker.make(FoodInstance, meal=meal[1])

        response = update_food_instance(meal[0].id, food_instance.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateRecipe:
    def test_if_user_is_anonymous_returns_401(self, create_recipe):
        response = create_recipe(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_201(self, api_client, create_recipe):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        recipe = baker.make(Recipe, trainee=trainee)

        response = create_recipe(meal.id, {
            "id": recipe.id,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    def test_if_data_is_invalid_returns_400(self, authenticate_with_trainee, create_recipe):
        authenticate_with_trainee()
        meal = baker.make(Meal)

        response = create_recipe(meal.id, {
            "id": 1
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['id'] is not None

    def test_if_meal_not_exists_returns_404(self, api_client, create_recipe):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        recipe = baker.make(Recipe, trainee=trainee)

        response = create_recipe(1, {
            "id": recipe.id
        })

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_recipe_of_other_trainee_returns_400(self, api_client, create_recipe):
        trainee = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainee[0].user)
        meal = baker.make(Meal, trainee=trainee[0])
        recipe = baker.make(Recipe, trainee=trainee[1])

        response = create_recipe(meal.id, {
            "id": recipe.id
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_meal_of_other_trainee_returns_400(self, api_client, create_food_instance):
        trainee = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainee[0].user)
        meal = baker.make(Meal, trainee=trainee[1])
        recipe = baker.make(Recipe, trainee=trainee[0])

        response = create_food_instance(meal.id, {
            "id": recipe.id
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveRecipe:
    def test_if_user_is_anonymous_returns_401(self, retrieve_recipe):
        response = retrieve_recipe(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_meal_Not_exists_returns_404(self, retrieve_recipe, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_recipe(1, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_recipe_Not_exists_returns_404(self, retrieve_recipe, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)

        response = retrieve_recipe(meal.id, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_recipe_exists_with_same_meal_and_same_trainee_returns_200(self, api_client, retrieve_recipe):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        recipe = baker.make(Recipe, trainee=trainee)
        meal.recipes.add(recipe)

        response = retrieve_recipe(meal.id, recipe.id)

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
        meal = baker.make(Meal, trainee=trainees[1])
        recipe = baker.make(Recipe, trainee=trainees[0])

        response = retrieve_recipe(meal.id, recipe.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListRecipe:
    def test_if_user_is_anonymous_returns_401(self, list_recipe):
        response = list_recipe(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, list_recipe):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        recipe = baker.make(Recipe, trainee=trainee)
        meal.recipes.add(recipe)

        response = list_recipe(meal.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0] == {
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

    def test_if_meal_Not_exists_returns_404(self, list_recipe, authenticate_with_trainee):
        authenticate_with_trainee()

        response = list_recipe(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteRecipe:
    def test_if_user_is_anonymous_returns_401(self, delete_recipe):
        response = delete_recipe(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_meal_Not_exists_returns_404(self, delete_recipe, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_recipe(1, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_recipe_Not_exists_returns_404(self, delete_recipe, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)

        response = delete_recipe(meal.id, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_recipe_exists_with_same_meal_and_same_trainee_returns_204(self, api_client, delete_recipe):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        meal = baker.make(Meal, trainee=trainee)
        recipe = baker.make(Recipe, trainee=trainee)
        meal.recipes.add(recipe)

        response = delete_recipe(meal.id, recipe.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_recipe_exists_with_other_trainee_returns_404(self, api_client, delete_recipe):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        meal = baker.make(Meal, trainee=trainees[1])
        recipe = baker.make(Recipe, trainee=trainees[0])

        response = delete_recipe(meal.id, recipe.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND
