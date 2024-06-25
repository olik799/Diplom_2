import allure
import requests

from endpoints import EP_CREATE_USER, EP_DELETE_OR_UPDATE_USER, EP_LOGIN


@allure.title("Создаем пользователя")
def create_user(payload):
    return requests.post(EP_CREATE_USER, data=payload)


@allure.title("Удаляем пользователя")
def delete_user(auth):
    requests.delete(EP_DELETE_OR_UPDATE_USER, headers={"Authorization": auth})


@allure.title("Авторизация пользователя")
def signup_user(payload):
    return requests.post(EP_LOGIN, data=payload)


@allure.title("Изменение данных пользователя")
def update_user(payload, auth):
    return requests.patch(EP_DELETE_OR_UPDATE_USER, data=payload, headers={"Authorization": auth})
