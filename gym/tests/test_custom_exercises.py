from model_bakery import baker
from rest_framework import status
import pytest
from core.models import Trainee
from gym.models import CustomExercise


@pytest.fixture
def create_custom_exercise(api_client):
    def do_create_custom_exercise(custom_exercise):
        return api_client.post('/gym/custom_exercises/', custom_exercise)
    return do_create_custom_exercise


@pytest.fixture
def retrieve_custom_exercise(api_client):
    def do_retrieve_custom_exercise(id):
        return api_client.get(f'/gym/custom_exercises/{id}/')
    return do_retrieve_custom_exercise


@pytest.fixture
def list_custom_exercise(api_client):
    def do_list_custom_exercise():
        return api_client.get('/gym/custom_exercises/')
    return do_list_custom_exercise


@pytest.fixture
def delete_custom_exercise(api_client):
    def do_delete_custom_exercise(id):
        return api_client.delete(f'/gym/custom_exercises/{id}/')
    return do_delete_custom_exercise


@pytest.fixture
def update_custom_exercise(api_client):
    def do_update_custom_exercise(id, custom_exercise):
        return api_client.patch(f'/gym/custom_exercises/{id}/', custom_exercise)
    return do_update_custom_exercise


@pytest.mark.django_db
class TestCreateCustomExercise:
    def test_if_user_is_anonymous_returns_401(self, create_custom_exercise):
        response = create_custom_exercise({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_invalid_returns_400(self, authenticate_with_trainee, create_custom_exercise):
        authenticate_with_trainee()

        response = create_custom_exercise({
            "name": "",
            "body_part": 0,
            "calories_burned": 0,
            "is_repetitive": 0
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    def test_if_user_is_authenticated_and_data_is_valid_returns_201(self, authenticate_with_trainee, create_custom_exercise):
        authenticate_with_trainee()

        response = create_custom_exercise({
            "name": "a",
            "body_part": "CR",
            "calories_burned": 0,
            "is_repetitive": False,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCustomExercise:
    def test_if_user_is_anonymous_returns_401(self, retrieve_custom_exercise):
        response = retrieve_custom_exercise(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_custom_exercise_Not_exists_returns_404(self, retrieve_custom_exercise, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_custom_exercise(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_custom_exercise_exists_with_same_trainee_returns_200(self, api_client, retrieve_custom_exercise):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        custom_exercise = baker.make(CustomExercise, trainee=trainee)

        response = retrieve_custom_exercise(custom_exercise.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": custom_exercise.id,
            "name": custom_exercise.name,
            "body_part": custom_exercise.body_part,
            "calories_burned": custom_exercise.calories_burned,
            "is_repetitive": custom_exercise.is_repetitive,
            "image": custom_exercise.image
        }

    def test_if_custom_exercise_exists_with_other_trainee_returns_404(self, api_client, retrieve_custom_exercise):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        custom_exercise = baker.make(CustomExercise, trainee=trainees[1])

        response = retrieve_custom_exercise(custom_exercise.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListCustomExercise:
    def test_if_user_is_anonymous_returns_401(self, list_custom_exercise):
        response = list_custom_exercise()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, authenticate_with_trainee, list_custom_exercise):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        custom_exercise = baker.make(CustomExercise, trainee=trainee)

        response = list_custom_exercise()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0] == {
            "id": custom_exercise.id,
            "name": custom_exercise.name,
            "body_part": custom_exercise.body_part,
            "calories_burned": custom_exercise.calories_burned,
            "is_repetitive": custom_exercise.is_repetitive,
            "image": custom_exercise.image
        }


@pytest.mark.django_db
class TestDeleteCustomExercise:
    def test_if_user_is_anonymous_returns_401(self, delete_custom_exercise):
        response = delete_custom_exercise(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_custom_exercise_Not_exists_returns_404(self, delete_custom_exercise, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_custom_exercise(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_custom_exercise_exists_with_same_trainee_returns_204(self, api_client, delete_custom_exercise):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        custom_exercise = baker.make(CustomExercise, trainee=trainee)

        response = delete_custom_exercise(custom_exercise.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_custom_exercise_exists_with_other_trainee_returns_404(self, api_client, delete_custom_exercise):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        custom_exercise = baker.make(CustomExercise, trainee=trainees[1])

        response = delete_custom_exercise(custom_exercise.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateCustomExercise:
    def test_if_user_is_anonymous_returns_401(self, update_custom_exercise):
        response = update_custom_exercise(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_custom_exercise_Not_exists_returns_404(self, update_custom_exercise, authenticate_with_trainee):
        authenticate_with_trainee()

        response = update_custom_exercise(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_custom_exercise_exists_with_same_trainee_returns_200(self, api_client, update_custom_exercise):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        custom_exercise = baker.make(CustomExercise, trainee=trainee, name='exercise_1')

        response = update_custom_exercise(custom_exercise.id, {'name': 'exercise_2'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'exercise_2'

    def test_if_custom_exercise_exists_with_other_trainee_returns_404(self, api_client, update_custom_exercise):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        custom_exercise = baker.make(CustomExercise, trainee=trainees[1])

        response = update_custom_exercise(custom_exercise.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND
