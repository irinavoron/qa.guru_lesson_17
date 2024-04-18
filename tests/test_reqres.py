import requests
from jsonschema import validate

from schemas import list_users_schema, single_user_schema

url = 'https://reqres.in'
endpoint_list_users = '/api/users'
endpoint_single_user = '/api/users/2'
endpoint_user_not_found = '/api/users/23'


def test_list_users_status_code():
    response = requests.get(url + endpoint_list_users, {'page': 2})

    assert response.status_code == 200


def test_list_users_json_schema():
    response_body = requests.get(url + endpoint_list_users, {'page': 2}).json()

    validate(response_body, list_users_schema)


def test_list_users_number_per_page():
    response_body = requests.get(url + endpoint_list_users, {'page': 2}).json()

    assert response_body['per_page'] == len(response_body['data'])


def test_single_user_status_code():
    response = requests.get(url + endpoint_single_user)

    assert response.status_code == 200


def test_single_user_json_schema():
    response_body = requests.get(url + endpoint_single_user).json()

    validate(response_body, single_user_schema)


def test_user_not_found_status_code():
    response = requests.get(url + endpoint_user_not_found)

    assert response.status_code == 404


def test_user_not_found_empty_response_body():
    response_body = requests.get(url + endpoint_user_not_found).json()

    assert not response_body



# def test_body():
#     name = 'morpheus'
#     job = 'leader'
#     response = requests.post(url, {'name': name, 'job': job})
#     body = response.json()
#     assert body['name'] == name
#     assert body['job'] == job



