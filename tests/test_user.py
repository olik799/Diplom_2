import allure
import pytest

from base_metod import user
import response_text
import helpers


class TestCreateUser:

    @allure.title("Создание пользователя")
    def test_create_user(self):
        payload = helpers.generate_data_for_new_user()
        response = user.create_user(payload)
        assert response.status_code == 200 and (response.json())['success']
        user.delete_user(response.json()["accessToken"])

    @allure.title("Создание пользователя с повторяющимися данными")
    def test_create_user_with_same_params(self):
        payload = helpers.generate_data_for_new_user()
        response = user.create_user(payload)
        response_user2 = user.create_user(payload)
        assert (response_user2.status_code == 403 and (response_user2.json())['message'] == response_text.
                create_user_with_same_params)
        user.delete_user(response.json()["accessToken"])

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
        response = user.create_user(payload)
        assert (response.status_code == 403 and (response.json())['message'] == response_text.
                create_user_without_one_params)


class TestLoginUser:

    @allure.title("Авторизация пользователя")
    def test_login_user(self):
        payload = helpers.generate_data_for_new_user()
        response = user.create_user(payload)
        response_login = user.signup_user(payload)
        assert response_login.status_code == 200 and (response_login.json())['success']
        user.delete_user(response.json()["accessToken"])

    @allure.title("Авторизация пользователя с невалидным email")
    def test_login_user_wrong_email(self):
        payload = helpers.generate_data_for_new_user()
        response = user.create_user(payload)
        response_login = user.signup_user(payload={"name": payload['name'],
                                                   "email": 123456,
                                                   "password": payload['password']})
        assert (response_login.status_code == 401 and (response_login.json())['message'] == response_text.
                login_user_wrong_one_params)
        user.delete_user(response.json()["accessToken"])

    @allure.title("Авторизация пользователя с невалидным паролем")
    def test_login_user_wrong_password(self):
        payload = helpers.generate_data_for_new_user()
        response = user.create_user(payload)
        response_login = user.signup_user(payload={"name": payload['name'],
                                                   "email": payload['email'],
                                                   "password": 12345})
        assert (response_login.status_code == 401 and (response_login.json())['message'] == response_text.
                login_user_wrong_one_params)
        user.delete_user(response.json()["accessToken"])


class TestUpdateUser:

    @allure.title("Изменение email пользователя")
    def test_update_user_email(self):
        payload = helpers.generate_data_for_new_user()
        response = user.create_user(payload)
        auth = response.json()["accessToken"]
        user.signup_user(payload)
        payload['email'] = f'new{payload['email']}'
        response_update = user.update_user(payload, auth)
        assert response_update.status_code == 200 and (response_update.json())['success']
        user.delete_user(response.json()["accessToken"])

    @allure.title("Изменение email пользователя без авторизации")
    def test_update_user_without_auth(self):
        payload = helpers.generate_data_for_new_user()
        response = user.create_user(payload)
        auth = response.json()["accessToken"]
        user.signup_user(payload)
        payload['email'] = f'new{payload['email']}'
        response_update = user.update_user(payload, auth=None)
        assert (response_update.status_code == 401 and (response_update.json())['message'] == response_text.
                update_user_without_auth)
        user.delete_user(response.json()["accessToken"])
