from model_bakery import baker
from rest_framework import status
import pytest
from core.models import Trainee
from gym.models import PerformedWorkout, Exercise, CustomExercise, ExerciseInstance, Workout


@pytest.fixture
def create_performed_workout(api_client):
    def do_create_performed_workout(performed_workout):
        return api_client.post('/gym/performed_workouts/', performed_workout)
    return do_create_performed_workout


@pytest.fixture
def retrieve_performed_workout(api_client):
    def do_retrieve_performed_workout(id):
        return api_client.get(f'/gym/performed_workouts/{id}/')
    return do_retrieve_performed_workout


@pytest.fixture
def list_performed_workout(api_client):
    def do_list_performed_workout():
        return api_client.get('/gym/performed_workouts/')
    return do_list_performed_workout


@pytest.fixture
def delete_performed_workout(api_client):
    def do_delete_performed_workout(id):
        return api_client.delete(f'/gym/performed_workouts/{id}/')
    return do_delete_performed_workout


@pytest.fixture
def update_performed_workout(api_client):
    def do_update_performed_workout(id, performed_workout):
        return api_client.patch(f'/gym/performed_workouts/{id}/', performed_workout)
    return do_update_performed_workout


@pytest.fixture
def create_exercise_instance(api_client):
    def do_create_exercise_instance(performed_workout_id, exercise_instance):
        return api_client.post(f'/gym/performed_workouts/{performed_workout_id}/exercise_instances/', exercise_instance)
    return do_create_exercise_instance


@pytest.fixture
def retrieve_exercise_instance(api_client):
    def do_retrieve_exercise_instance(performed_workout_id, exercise_instance_id):
        return api_client.get(f'/gym/performed_workouts/{performed_workout_id}/exercise_instances/{exercise_instance_id}/')
    return do_retrieve_exercise_instance


@pytest.fixture
def list_exercise_instance(api_client):
    def do_list_exercise_instance(performed_workout_id):
        return api_client.get(f'/gym/performed_workouts/{performed_workout_id}/exercise_instances/')
    return do_list_exercise_instance


@pytest.fixture
def delete_exercise_instance(api_client):
    def do_delete_exercise_instance(performed_workout_id, exercise_instance_id):
        return api_client.delete(f'/gym/performed_workouts/{performed_workout_id}/exercise_instances/{exercise_instance_id}/')
    return do_delete_exercise_instance


@pytest.fixture
def update_exercise_instance(api_client):
    def do_update_exercise_instance(performed_workout_id, exercise_instance_id, exercise_instance):
        return api_client.patch(f'/gym/performed_workouts/{performed_workout_id}/exercise_instances/{exercise_instance_id}/', exercise_instance)
    return do_update_exercise_instance


@pytest.fixture
def create_workout(api_client):
    def do_create_workout(performed_workout_id, workout):
        return api_client.post(f'/gym/performed_workouts/{performed_workout_id}/workouts/', workout)
    return do_create_workout


@pytest.fixture
def retrieve_workout(api_client):
    def do_retrieve_workout(performed_workout_id, workout_id):
        return api_client.get(f'/gym/performed_workouts/{performed_workout_id}/workouts/{workout_id}/')
    return do_retrieve_workout


@pytest.fixture
def list_workout(api_client):
    def do_list_workout(performed_workout_id):
        return api_client.get(f'/gym/performed_workouts/{performed_workout_id}/workouts/')
    return do_list_workout


@pytest.fixture
def delete_workout(api_client):
    def do_delete_workout(performed_workout_id, workout_id):
        return api_client.delete(f'/gym/performed_workouts/{performed_workout_id}/workouts/{workout_id}/')
    return do_delete_workout


@pytest.mark.django_db
class TestCreatePerformedWorkout:
    def test_if_user_is_anonymous_returns_401(self, create_performed_workout):
        response = create_performed_workout({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_and_data_is_valid_returns_201(self, authenticate_with_trainee, create_performed_workout):
        authenticate_with_trainee()

        response = create_performed_workout({
            "name": "a"
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrievePerformedWorkout:
    def test_if_user_is_anonymous_returns_401(self, retrieve_performed_workout):
        response = retrieve_performed_workout(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_performed_workout_Not_exists_returns_404(self, retrieve_performed_workout, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_performed_workout(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_performed_workout_exists_with_same_trainee_returns_200(self, api_client, retrieve_performed_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)

        response = retrieve_performed_workout(performed_workout.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": performed_workout.id,
            "name": performed_workout.name,
            "time_performed": response.data["time_performed"],
            "workouts": [],
            "exercise_instances": [],
            "total_calories": 0
        }

    def test_if_performed_workout_exists_with_other_trainee_returns_404(self, api_client, retrieve_performed_workout):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainees[1])

        response = retrieve_performed_workout(performed_workout.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListPerformedWorkout:
    def test_if_user_is_anonymous_returns_401(self, list_performed_workout):
        response = list_performed_workout()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, list_performed_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)

        response = list_performed_workout()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0] == {
            "id": performed_workout.id,
            "name": performed_workout.name,
            "time_performed": response.data['results'][0]["time_performed"],
            "workouts": [],
            "exercise_instances": [],
            "total_calories": 0
        }


@pytest.mark.django_db
class TestDeletePerformedWorkout:
    def test_if_user_is_anonymous_returns_401(self, delete_performed_workout):
        response = delete_performed_workout(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_performed_workout_Not_exists_returns_404(self, delete_performed_workout, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_performed_workout(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_performed_workout_exists_with_same_trainee_returns_204(self, api_client, delete_performed_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)

        response = delete_performed_workout(performed_workout.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_performed_workout_exists_with_other_trainee_returns_404(self, api_client, delete_performed_workout):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainees[1])

        response = delete_performed_workout(performed_workout.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdatePerformedWorkout:
    def test_if_user_is_anonymous_returns_401(self, update_performed_workout):
        response = update_performed_workout(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_performed_workout_Not_exists_returns_404(self, update_performed_workout, authenticate_with_trainee):
        authenticate_with_trainee()

        response = update_performed_workout(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_performed_workout_exists_with_same_trainee_returns_200(self, api_client, update_performed_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(
            PerformedWorkout, trainee=trainee, name='performed_workout_1')

        response = update_performed_workout(
            performed_workout.id, {'name': 'performed_workout_2'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'performed_workout_2'

    def test_if_performed_workout_exists_with_other_trainee_returns_404(self, api_client, update_performed_workout):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainees[1])

        response = update_performed_workout(performed_workout.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateExerciseInstance:
    def test_if_user_is_anonymous_returns_401(self, create_exercise_instance):
        response = create_exercise_instance(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_201(self, api_client, create_exercise_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        exercise = baker.make(Exercise)

        response = create_exercise_instance(performed_workout.id, {
            "exercise_id": exercise.id,
            "duration": 10,
            "sets": 4
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    def test_if_data_is_invalid_returns_400(self, authenticate_with_trainee, create_exercise_instance):
        authenticate_with_trainee()
        performed_workout = baker.make(PerformedWorkout)

        response = create_exercise_instance(performed_workout.id, {
            "exercise_id": 1,
            "quantity": 1
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['exercise_id'] is not None

    def test_if_performed_workout_not_exists_returns_404(self, api_client, create_exercise_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        exercise = baker.make(Exercise)

        response = create_exercise_instance(1, {
            "exercise_id": exercise.id,
            "duration": 10,
            "sets": 4
        })

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_custom_exercise_of_other_trainee_returns_400(self, api_client, create_exercise_instance):
        trainee = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainee[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee[0])
        custom_exercise = baker.make(CustomExercise, trainee=trainee[1])

        response = create_exercise_instance(performed_workout.id, {
            "exercise_id": custom_exercise.id,
            "quantity": 100
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_performed_workout_of_other_trainee_returns_404(self, api_client, create_exercise_instance):
        trainee = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainee[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee[1])
        exercise = baker.make(Exercise)

        response = create_exercise_instance(performed_workout.id, {
            "exercise_id": exercise.id,
            "duration": 10,
            "sets": 4
        })

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRetrieveExerciseInstance:
    def test_if_user_is_anonymous_returns_401(self, retrieve_exercise_instance):
        response = retrieve_exercise_instance(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_performed_workout_Not_exists_returns_404(self, retrieve_exercise_instance, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_exercise_instance(1, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_Not_exists_returns_404(self, retrieve_exercise_instance, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)

        response = retrieve_exercise_instance(performed_workout.id, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_exists_with_same_performed_workout_and_same_trainee_returns_200(self, api_client, retrieve_exercise_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout)

        response = retrieve_exercise_instance(
            performed_workout.id, exercise_instance.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == exercise_instance.id
        assert response.data['exercise']['id'] == exercise_instance.exercise.id
        assert response.data['duration'] == exercise_instance.duration
        assert response.data['sets'] == exercise_instance.sets
        assert response.data['total_calories'] == exercise_instance.get_total_calories(
        )

    def test_if_exercise_instance_exists_with_other_performed_workout_and_trainee_returns_404(self, api_client, retrieve_exercise_instance):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainees[1])
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout)

        response = retrieve_exercise_instance(
            performed_workout.id, exercise_instance.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_exists_with_other_performed_workout_but_same_trainee_returns_404(self, api_client, retrieve_exercise_instance):
        trainees = baker.make(Trainee)
        api_client.force_authenticate(user=trainees.user)
        performed_workout = baker.make(
            PerformedWorkout, trainee=trainees, _quantity=2)
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout[1])

        response = retrieve_exercise_instance(
            performed_workout[0].id, exercise_instance.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListExerciseInstance:
    def test_if_user_is_anonymous_returns_401(self, list_exercise_instance):
        response = list_exercise_instance(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, list_exercise_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        exercise_instances = baker.make(
            ExerciseInstance, performed_workout=performed_workout, _quantity=2)

        response = list_exercise_instance(performed_workout.id)

        assert response.status_code == status.HTTP_200_OK
        for i in range(2):
            assert response.data[i]['id'] == exercise_instances[i].id
            assert response.data[i]['exercise']['id'] == exercise_instances[i].exercise.id
            assert response.data[i]['duration'] == exercise_instances[i].duration
            assert response.data[i]['sets'] == exercise_instances[i].sets
            assert response.data[i]['total_calories'] == exercise_instances[i].get_total_calories(
            )

    def test_if_performed_workout_Not_exists_returns_404(self, list_exercise_instance, authenticate_with_trainee):
        authenticate_with_trainee()

        response = list_exercise_instance(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteExerciseInstance:
    def test_if_user_is_anonymous_returns_401(self, delete_exercise_instance):
        response = delete_exercise_instance(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_performed_workout_Not_exists_returns_404(self, delete_exercise_instance, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_exercise_instance(1, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_Not_exists_returns_404(self, delete_exercise_instance, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)

        response = delete_exercise_instance(performed_workout.id, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_exists_with_same_performed_workout_and_same_trainee_returns_204(self, api_client, delete_exercise_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout)

        response = delete_exercise_instance(
            performed_workout.id, exercise_instance.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_exercise_instance_exists_with_other_performed_workout_and_trainee_returns_404(self, api_client, delete_exercise_instance):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainees[1])
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout)

        response = delete_exercise_instance(
            performed_workout.id, exercise_instance.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_exists_with_other_performed_workout_but_same_trainee_returns_404(self, api_client, delete_exercise_instance):
        trainees = baker.make(Trainee)
        api_client.force_authenticate(user=trainees.user)
        performed_workout = baker.make(
            PerformedWorkout, trainee=trainees, _quantity=2)
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout[1])

        response = delete_exercise_instance(
            performed_workout[0].id, exercise_instance.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateExerciseInstance:
    def test_if_user_is_anonymous_returns_401(self, update_exercise_instance):
        response = update_exercise_instance(1, 1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_performed_workout_Not_exists_returns_404(self, update_exercise_instance, authenticate_with_trainee):
        authenticate_with_trainee()

        response = update_exercise_instance(1, 1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_Not_exists_returns_404(self, update_exercise_instance, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)

        response = update_exercise_instance(performed_workout.id, 1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_exists_with_same_performed_workout_and_same_trainee_returns_200(self, api_client, update_exercise_instance):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout, duration=5)

        response = update_exercise_instance(
            performed_workout.id, exercise_instance.id, {"duration": 10}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['duration'] == 10

    def test_if_exercise_instance_exists_with_other_performed_workout_and_trainee_returns_404(self, api_client, update_exercise_instance):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainees[1])
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout)

        response = update_exercise_instance(
            performed_workout.id, exercise_instance.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_exercise_instance_exists_with_other_performed_workout_but_same_trainee_returns_404(self, api_client, update_exercise_instance):
        trainees = baker.make(Trainee)
        api_client.force_authenticate(user=trainees.user)
        performed_workout = baker.make(
            PerformedWorkout, trainee=trainees, _quantity=2)
        exercise_instance = baker.make(
            ExerciseInstance, performed_workout=performed_workout[1])

        response = update_exercise_instance(
            performed_workout[0].id, exercise_instance.id, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateWorkout:
    def test_if_user_is_anonymous_returns_401(self, create_workout):
        response = create_workout(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_201(self, api_client, create_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        workout = baker.make(Workout, trainee=trainee)

        response = create_workout(performed_workout.id, {
            "id": workout.id,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    def test_if_data_is_invalid_returns_400(self, authenticate_with_trainee, create_workout):
        authenticate_with_trainee()
        performed_workout = baker.make(PerformedWorkout)

        response = create_workout(performed_workout.id, {
            "id": 1
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['id'] is not None

    def test_if_performed_workout_not_exists_returns_404(self, api_client, create_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        workout = baker.make(Workout, trainee=trainee)

        response = create_workout(1, {
            "id": workout.id
        })

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_workout_of_other_trainee_returns_400(self, api_client, create_workout):
        trainee = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainee[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee[0])
        workout = baker.make(Workout, trainee=trainee[1])

        response = create_workout(performed_workout.id, {
            "id": workout.id
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_performed_workout_of_other_trainee_returns_400(self, api_client, create_exercise_instance):
        trainee = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainee[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee[1])
        workout = baker.make(Workout, trainee=trainee[0])

        response = create_exercise_instance(performed_workout.id, {
            "id": workout.id
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveWorkout:
    def test_if_user_is_anonymous_returns_401(self, retrieve_workout):
        response = retrieve_workout(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_performed_workout_Not_exists_returns_404(self, retrieve_workout, authenticate_with_trainee):
        authenticate_with_trainee()

        response = retrieve_workout(1, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_workout_Not_exists_returns_404(self, retrieve_workout, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)

        response = retrieve_workout(performed_workout.id, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_workout_exists_with_same_performed_workout_and_same_trainee_returns_200(self, api_client, retrieve_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        workout = baker.make(Workout, trainee=trainee)
        performed_workout.workouts.add(workout)

        response = retrieve_workout(performed_workout.id, workout.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": workout.id,
            "name": workout.name,
            "instructions": workout.instructions,
            "image": workout.image,
            "exercise_instances": [],
            "total_calories": 0
        }

    def test_if_workout_exists_with_other_trainee_returns_404(self, api_client, retrieve_workout):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainees[1])
        workout = baker.make(Workout, trainee=trainees[0])

        response = retrieve_workout(performed_workout.id, workout.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListWorkout:
    def test_if_user_is_anonymous_returns_401(self, list_workout):
        response = list_workout(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, list_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        workout = baker.make(Workout, trainee=trainee)
        performed_workout.workouts.add(workout)

        response = list_workout(performed_workout.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0] == {
            "id": workout.id,
            "name": workout.name,
            "instructions": workout.instructions,
            "image": workout.image,
            "exercise_instances": [],
            "total_calories": 0
        }

    def test_if_performed_workout_Not_exists_returns_404(self, list_workout, authenticate_with_trainee):
        authenticate_with_trainee()

        response = list_workout(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteWorkout:
    def test_if_user_is_anonymous_returns_401(self, delete_workout):
        response = delete_workout(1, 1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_performed_workout_Not_exists_returns_404(self, delete_workout, authenticate_with_trainee):
        authenticate_with_trainee()

        response = delete_workout(1, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_workout_Not_exists_returns_404(self, delete_workout, api_client):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)

        response = delete_workout(performed_workout.id, 1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_workout_exists_with_same_performed_workout_and_same_trainee_returns_204(self, api_client, delete_workout):
        trainee = baker.make(Trainee)
        api_client.force_authenticate(user=trainee.user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainee)
        workout = baker.make(Workout, trainee=trainee)
        performed_workout.workouts.add(workout)

        response = delete_workout(performed_workout.id, workout.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_workout_exists_with_other_trainee_returns_404(self, api_client, delete_workout):
        trainees = baker.make(Trainee, _quantity=2)
        api_client.force_authenticate(user=trainees[0].user)
        performed_workout = baker.make(PerformedWorkout, trainee=trainees[1])
        workout = baker.make(Workout, trainee=trainees[0])

        response = delete_workout(performed_workout.id, workout.id)

        assert response.status_code == status.HTTP_404_NOT_FOUND
