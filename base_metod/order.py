import allure
import requests
import random

from data.endpoints import Endpoints


@allure.title("Получаем список ингредиентов")
def get_ingredients():
    return requests.get(Endpoints.INGREDIENTS)


@allure.title("Создаем заказ")
def create_order(ingredients: list[str], headers=None):
    data = {"ingredients": ingredients}
    return requests.post(Endpoints.CREATE_ORDER, data=data, headers=headers)


@allure.title("Получаем заказы пользователя")
def get_user_order(headers=None):
    return requests.get(Endpoints.CREATE_ORDER, headers=headers)


@allure.title("Получаем 3 случайных ингредиента")
def random_list_of_ingredients():
    response = get_ingredients().json()["data"]
    ing_list = list(map(lambda d: d['_id'], response))
    result = []
    for i in range(3):
        result.append(random.choice(ing_list))
        return result
