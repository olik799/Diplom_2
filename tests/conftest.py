import pytest
import requests
from helpers import generate_data_for_new_user
from data.endpoints import Endpoints


@pytest.fixture
def create_user():
    payload = generate_data_for_new_user()
    response = requests.post(Endpoints.CREATE_USER, data=payload)
    yield payload, response
    auth = response.json()['accessToken']
    requests.delete(Endpoints.DELETE_OR_UPDATE_USER, headers={"Authorization": auth})
