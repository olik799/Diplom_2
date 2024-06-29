import allure
import pytest
import requests

import helpers
from data.status_code import StatusCode
from data.response_text import TextResponse
from base_metod import user


class TestCreateUser:

    @allure.title("Создание пользователя")
    def test_create_new_user(self, create_user):
        response = create_user
        assert response[1].status_code == StatusCode.OK and response[1].json().get('success') is True

    @allure.title("Создание пользователя с повторяющимися данными")
    def test_create_user_with_same_params(self, create_user):
        response = create_user
        payload = response[0]
        response_user2 = user.create_new_user(payload)
        assert (response_user2.status_code == StatusCode.FORBIDDEN and response_user2.json().get('message') ==
                TextResponse.CREATE_USER_WITH_SAME_PARAMS)

    @allure.title("Создание пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("name, email, password",
                             [[None, helpers.generate_email(), helpers.generate_random_string(7)],
                              [helpers.generate_random_string(7), None, helpers.generate_random_string(7)],
                              [helpers.generate_random_string(7), helpers.generate_email(), None]])
    def test_create_user_without_name(self, name, email, password):
        payload = {
            "name": name,
            "email": email,
            "password": password
        }
        response = user.create_new_user(payload)
        assert (response.status_code == StatusCode.FORBIDDEN and (response.json())['message'] == TextResponse.
                CREATE_USER_WITHOUT_ONE_PARAMS)


class TestLoginUser:

    @allure.title("Авторизация пользователя")
    def test_login_user(self, create_user):
        response = create_user
        response_login = user.signup_user(response[0])
        assert response_login.status_code == StatusCode.OK and response_login.json().get("success") is True

    @allure.title("Авторизация пользователя с невалидным email")
    def test_login_user_wrong_email(self, create_user):
        response = create_user
        payload = response[0]
        payload = {"name": payload['name'], "email": 123456, "password": payload['password']}
        response_login = user.signup_user(payload)
        assert (response_login.status_code == StatusCode.UNAUTHORIZED and response_login.json().get('message') ==
                TextResponse.LOGIN_USER_WRONG_ONE_PARAMS)

    @allure.title("Авторизация пользователя с невалидным паролем")
    def test_login_user_wrong_password(self, create_user):
        response = create_user
        payload = response[0]
        payload = {"name": payload['name'], "email": payload['email'], "password": 12345}
        response_login = user.signup_user(payload)
        assert (response_login.status_code == StatusCode.UNAUTHORIZED and response_login.json().get('message') ==
                TextResponse.LOGIN_USER_WRONG_ONE_PARAMS)


class TestUpdateUser:

    @allure.title("Изменение email пользователя")
    def test_update_user_email(self, create_user):
        response = create_user
        payload = response[0]
        auth = response[1].json()["accessToken"]
        user.signup_user(payload)
        payload['email'] = f'new{payload["email"]}'
        response_update = user.update_user(payload, auth)
        assert response_update.status_code == StatusCode.OK and response_update.json().get("success") is True

    @allure.title("Изменение email пользователя без авторизации")
    def test_update_user_without_auth(self, create_user):
        response = create_user
        payload = response[0]
        user.signup_user(payload)
        payload['email'] = f'new{payload["email"]}'
        response_update = user.update_user(payload, auth=None)
        assert (response_update.status_code == StatusCode.UNAUTHORIZED and response_update.json().get('message') ==
                TextResponse.UPDATE_USER_WITHOUT_AUTH)
