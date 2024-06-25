import allure
from helpers import generate_data_for_new_user as gen_user
from base_metod import order
from base_metod import user
import response_text


class TestOrder:

    @allure.title("Созание заказа с авторизацией")
    def test_create_order(self):
        ingredients = order.random_list_of_ingredients()
        payload = gen_user()
        response_user = user.create_user(payload)
        auth = response_user.json()["accessToken"]
        response = order.create_order(ingredients, {"Authorization": auth})
        assert response.status_code == 200 and (response.json())['success']
        user.delete_user(auth)

    @allure.title("Созание заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredients = order.random_list_of_ingredients()
        response = order.create_order(ingredients)
        assert response.status_code == 200 and (response.json())['success']

    @allure.title("Созание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        payload = gen_user()
        response_user = user.create_user(payload)
        auth = response_user.json()["accessToken"]
        response = order.create_order(ingredients=[])
        assert (response.status_code == 400 and (response.json())['message'] == response_text.
                create_order_without_ingredients)
        user.delete_user(auth)

    @allure.title("Созание заказа с неверным хэшем ингредиентов")
    def test_create_order_wrong_hash(self):
        payload = gen_user()
        response_user = user.create_user(payload)
        auth = response_user.json()["accessToken"]
        response = order.create_order(ingredients=["1", "2"])
        assert response.status_code == 500
        user.delete_user(auth)

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_auth_user(self):
        payload = gen_user()
        response = user.create_user(payload)
        auth = response.json()["accessToken"]
        header_auth = {"Authorization": auth}
        ingredients = order.random_list_of_ingredients()
        order.create_order(ingredients, header_auth)
        response = order.get_user_order(header_auth)
        assert response.status_code == 200 and (response.json())['success']
        user.delete_user(auth)

    @allure.title("Получение заказов без авторизации")
    def test_get_orders_without_auth(self):
        ingredients = order.random_list_of_ingredients()
        order.create_order(ingredients)
        response = order.get_user_order()
        assert response.status_code == 401 and (response.json())['message'] == response_text.get_order_without_auth
