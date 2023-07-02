from model_bakery import baker
from rest_framework import status
import pytest
from gym.models import Exercise


@pytest.fixture
def create_exercise(api_client):
    def do_create_exercise(exercise):
        return api_client.post('/gym/exercises/', exercise)
    return do_create_exercise


@pytest.fixture
def retrieve_exercise(api_client):
    def do_retrieve_exercise(id):
        return api_client.get(f'/gym/exercises/{id}/')
    return do_retrieve_exercise


@pytest.fixture
def list_exercise(api_client):
    def do_list_exercise():
        return api_client.get('/gym/exercises/')
    return do_list_exercise


@pytest.mark.django_db
class TestCreateExercise:
    def test_if_user_is_anonymous_returns_401(self, create_exercise):
        response = create_exercise({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_405(self, authenticate_with_trainee, create_exercise):
        authenticate_with_trainee()

        response = create_exercise({})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestRetrieveExercise:
    def test_if_user_is_anonymous_returns_401(self, retrieve_exercise):
        response = retrieve_exercise(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_exercise_Not_exists_returns_404(self, retrieve_exercise, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_exercise(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_exists_returns_200(self, retrieve_exercise, authenticate_with_trainee):
        authenticate_with_trainee()
        exercise = baker.make(Exercise)

        response = retrieve_exercise(exercise.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": exercise.id,
            "name": exercise.name,
            "body_part": exercise.body_part,
            "calories_burned": exercise.calories_burned,
            "is_repetitive": exercise.is_repetitive,
            "image": exercise.image
        }


@pytest.mark.django_db
class TestListExercise:
    def test_if_user_is_anonymous_returns_401(self, list_exercise):
        response = list_exercise()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, authenticate_with_trainee, list_exercise):
        authenticate_with_trainee()
        exercise = baker.make(Exercise)

        response = list_exercise()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0] == {
            "id": exercise.id,
            "name": exercise.name,
            "body_part": exercise.body_part,
            "calories_burned": exercise.calories_burned,
            "is_repetitive": exercise.is_repetitive,
            "image": exercise.image
        }
