from rest_framework import status
import pytest
from core.models import User


@pytest.fixture
def create_token(api_client):
    def do_create_token(user):
        return api_client.post('/auth/jwt/create/', user)
    return do_create_token


@pytest.fixture
def create_user(api_client):
    def do_create_user(user):
        return api_client.post('/auth/users/', user)
    return do_create_user


@pytest.fixture
def retrieve_user(api_client):
    def do_retrieve_user():
        return api_client.get('/auth/users/me/')
    return do_retrieve_user


@pytest.fixture
def retrieve_user(api_client):
    def do_retrieve_user():
        return api_client.get('/auth/users/me/')
    return do_retrieve_user


@pytest.fixture
def update_user(api_client):
    def do_update_user(user):
        return api_client.patch('/auth/users/me/', user)
    return do_update_user


@pytest.mark.django_db
class TestCreateToken:
    def test_if_invalid_data_returns_400(self, create_token):
        response = create_token({
            "username": '',
            "password": ''
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_wrong_credentials_returns_401(self, create_token):
        response = create_token({
            "username": 'a',
            "password": 'a'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_valid_data_returns_200(self, create_token):
        user = User()
        user.username = 'a'
        user.email = 'a@a.com'
        user.set_password('12345678a')
        user.save()

        response = create_token({
            "username": 'a',
            "password": '12345678a'
        })

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateUser:
    def test_if_data_is_invalid_returns_400(self, create_user):
        response = create_user({
            "username": "",
            "password": "",
            "email": "",
            "first_name": "",
            "last_name": ""
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, create_user):
        response = create_user({
            "username": "a",
            "password": "12345678a",
            "email": "a@a.com",
            "first_name": "a",
            "last_name": "a"
        })

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveUser:
    def test_if_user_is_anonymous_returns_401(self, retrieve_user):
        response = retrieve_user()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, retrieve_user, authenticate_without_trainee):
        authenticate_without_trainee()

        response = retrieve_user()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUpdateUser:
    def test_if_user_is_anonymous_returns_401(self, update_user):
        response = update_user({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_user_if_data_is_valid_returns_200(self, update_user, authenticate_without_trainee):
        authenticate_without_trainee()

        response = update_user({"first_name": "a"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'a'
