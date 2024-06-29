import pytest
import allure
from base_metod import order
from data.status_code import StatusCode
from data.response_text import TextResponse


class TestOrder:

    @allure.title("Созание заказа с авторизацией")
    def test_create_order(self, create_user):
        ingredients = order.random_list_of_ingredients()
        response = create_user
        auth = response[1].json()["accessToken"]
        response = order.create_order(ingredients, {"Authorization": auth})
        assert response.status_code == StatusCode.OK and response.json().get('success') is True

    @allure.title("Созание заказа без авторизации")
    def test_create_order_without_auth(self, create_user):
        ingredients = order.random_list_of_ingredients()
        response = order.create_order(ingredients)
        assert response.status_code == StatusCode.OK and response.json().get('success') is True

    @allure.title("Созание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_user):
        response = create_user
        ingredients = []
        auth = response[1].json()["accessToken"]
        headers = {'Authorization': auth}
        response = order.create_order(ingredients, headers)
        assert (response.status_code == StatusCode.BAD_REQUEST and response.json().get('message') == TextResponse.
                CREATE_ORDER_WITHOUT_INGREDIENTS)

    @allure.title("Созание заказа с неверным хэшем ингредиентов")
    def test_create_order_wrong_hash(self, create_user):
        response = create_user
        ingredients = ["1", "2"]
        auth = response[1].json()["accessToken"]
        headers = {'Authorization': auth}
        response = order.create_order(ingredients, headers)
        assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_auth_user(self, create_user):
        response = create_user
        auth = response[1].json()["accessToken"]
        headers = {'Authorization': auth}
        ingredients = order.random_list_of_ingredients()
        order.create_order(ingredients, headers)
        response_get_order = order.get_user_order(headers)
        assert response_get_order.status_code == StatusCode.OK and response_get_order.json().get('success') is True

    @allure.title("Получение заказов без авторизации")
    def test_get_orders_without_auth(self, create_user):
        ingredients = order.random_list_of_ingredients()
        order.create_order(ingredients)
        response = order.get_user_order()
        assert (response.status_code == StatusCode.UNAUTHORIZED and response.json().get('message') == TextResponse.
                GET_ORDER_WITHOUT_AUTH)
