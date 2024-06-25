import allure
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def generate_email():
    letters = string.ascii_lowercase
    login = ''.join(random.choice(letters) for i in range(7))
    email = login + '@yandex.ru'
    return email


@allure.title("Создаем пользователя пользователя")
def generate_data_for_new_user():
    name = generate_random_string(7)
    email = name + '@yandex.ru'
    password = generate_random_string(7)

    payload = {
        "name": name,
        "email": email,
        "password": password
    }
    return payload
