import json

import allure
import requests
from jsonschema import validate

from tests.schemas import create_json_schema, update_json_schema, register_json_schema, \
    register_unsuccessful_json_schema

users_url = 'https://reqres.in/api/users'
register_url = 'https://reqres.in/api/register'
login_url = 'https://reqres.in/api/login'


def api_get(url, **kwargs):
    with allure.step('API get request'):
        response = requests.get('https://reqres.in/api' + url, **kwargs)
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True))
        return response


def test_list_users_status_code():
    response = api_get('/users', params={'page': 2})
    assert response.status_code == 200


def test_list_users_number_per_page():
    response = api_get('/users', params={'page': 2})
    body = response.json()
    number_per_page = len(body['data'])
    assert number_per_page == body['per_page']


def test_single_user_status_code():
    response = api_get('/users/2')
    assert response.status_code == 200


def test_single_user_response_id():
    body = api_get('/users/2').json()
    assert body['data']['id'] == 2


def test_user_not_found_status_code():
    response = api_get('/users/23')
    assert response.status_code == 404


def test_user_not_found_empty_response_body():
    response = api_get('/users/23')
    response_body = response.json()
    assert response_body == {}


def test_create_status_code():
    payload = {'name': 'morpheus', 'job': 'leader'}
    response = requests.post(users_url, json=payload)
    assert response.status_code == 201


def test_create_json_schema():
    payload = {'name': 'morpheus', 'job': 'leader'}
    response_body = requests.post(users_url, json=payload).json()
    validate(response_body, create_json_schema)


def test_create_response_data():
    name = 'morpheus'
    job = 'leader'
    payload = {'name': name, 'job': job}
    response_body = requests.post(users_url, json=payload).json()
    assert response_body['name'] == name
    assert response_body['job'] == job


def test_update_status_code():
    update_url = users_url + '/2'
    payload = {'name': 'morpheus', 'job': 'zion resident'}
    response = requests.put(update_url, json=payload)
    assert response.status_code == 200


def test_update_json_schema():
    update_url = users_url + '/2'
    payload = {'name': 'morpheus', 'job': 'zion resident'}
    response_body = requests.put(update_url, json=payload).json()
    validate(response_body, update_json_schema)


def test_update_response_data():
    update_url = users_url + '/2'
    name = 'morpheus'
    job = 'zion resident'
    payload = {'name': name, 'job': job}
    response_body = requests.put(update_url, json=payload).json()
    assert response_body['name'] == name
    assert response_body['job'] == job


def test_delete_status_code():
    delete_url = users_url + '/2'
    response = requests.delete(delete_url)
    assert response.status_code == 204


def test_register_successful_status_code():
    payload = {'email': "eve.holt@reqres.in", 'password': "pistol"}
    response = requests.post(register_url, json=payload)
    assert response.status_code == 200


def test_register_successful_json_schema():
    payload = {'email': "eve.holt@reqres.in", 'password': "pistol"}
    response_body = requests.post(register_url, json=payload).json()
    validate(response_body, register_json_schema)


def test_register_unsuccessful_status_code():
    payload = {'email': "sydney@fife"}
    response = requests.post(register_url, json=payload)
    assert response.status_code == 400


def test_register_unsuccessful_json_schema():
    payload = {'email': "sydney@fife"}
    response_body = requests.post(register_url, json=payload).json()
    validate(response_body, schema=register_unsuccessful_json_schema)


def test_register_unsuccessful_error_message():
    payload = {'email': "sydney@fife"}
    response_body = requests.post(register_url, json=payload).json()
    assert response_body['error'] == "Missing password"












