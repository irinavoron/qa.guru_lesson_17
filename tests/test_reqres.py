import requests
from jsonschema import validate

from schemas import list_users_schema

url = 'https://reqres.in'


def test_list_users_status_code():
    endpoint = '/api/users'
    response = requests.get(url + endpoint, {'page': 2})

    assert response.status_code == 200


def test_list_users_json_schema():
    endpoint = '/api/users'
    response_body = requests.get(url + endpoint, {'page': 2}).json()

    validate(response_body, list_users_schema)


def test_number_per_page():
    endpoint = '/api/users'
    response_body = requests.get(url + endpoint, {'page': 2}).json()

    assert response_body['per_page'] == len(response_body['data'])


# def test_body():
#     name = 'morpheus'
#     job = 'leader'
#     response = requests.post(url, {'name': name, 'job': job})
#     body = response.json()
#     assert body['name'] == name
#     assert body['job'] == job



