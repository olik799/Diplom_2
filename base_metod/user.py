import allure
import requests
import random
from data.endpoints import Endpoints


@allure.title("Создаем пользователя")
def create_new_user(payload):
    return requests.post(Endpoints.CREATE_USER, data=payload)


@allure.title("Авторизация пользователя")
def signup_user(payload):
    return requests.post(Endpoints.LOGIN, data=payload)


@allure.title("Изменение данных пользователя")
def update_user(payload, auth):
    return requests.patch(Endpoints.DELETE_OR_UPDATE_USER, data=payload, headers={"Authorization": auth})
