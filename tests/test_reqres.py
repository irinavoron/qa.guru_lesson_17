import requests
from jsonschema import validate
from schemas import list_users_schema, single_user_schema, create_schema, update_schema, register_successful_schema, \
    register_unsuccessful_schema

from utils.api_methods import get_api_request

endpoint_users = '/api/users'
endpoint_single_user = '/api/users/2'
endpoint_user_not_found = '/api/users/23'
endpoint_register = '/api/register'


def test_list_users_status_code():
    response = get_api_request(endpoint=endpoint_users, params={'page': 2})

    assert response.status_code == 200


def test_list_users_json_schema():
    response_body = get_api_request(endpoint=endpoint_users, params={'page': 2}).json()

    validate(response_body, list_users_schema)


def test_list_users_number_per_page():
    response_body = get_api_request(endpoint=endpoint_users, params={'page': 2}).json()

    assert response_body['per_page'] == len(response_body['data'])


def test_single_user_status_code():
    response = get_api_request(endpoint=endpoint_single_user)

    assert response.status_code == 200


def test_single_user_json_schema():
    response_body = get_api_request(endpoint=endpoint_single_user).json()

    validate(response_body, single_user_schema)


def test_user_not_found_status_code():
    response = get_api_request(endpoint=endpoint_user_not_found)

    assert response.status_code == 404


def test_user_not_found_empty_response_body():
    response_body = get_api_request(endpoint=endpoint_user_not_found).json()

    assert not response_body


def test_create_status_code():
    response = requests.post(url + endpoint_users, {'name': 'morpheus', 'job': 'leader'})

    assert response.status_code == 201


def test_create_json_schema():
    response_body = requests.post(url + endpoint_users, {'name': 'morpheus', 'job': 'leader'}).json()

    validate(response_body, create_schema)


def test_create_name_and_job_in_response():
    name = 'morpheus'
    job = 'leader'
    response = requests.post(url + endpoint_users, {'name': name, 'job': job})
    body = response.json()
    assert body['name'] == name
    assert body['job'] == job


def test_update_status_code_put():
    response = requests.put(url + endpoint_single_user, {'name': 'morpheus', 'job': 'zion resident'})

    assert response.status_code == 200


def test_update_json_schema():
    response_body = requests.put(url + endpoint_single_user, {'name': 'morpheus', 'job': 'zion resident'}).json()

    validate(response_body, update_schema)


def test_update_no_name_in_response_body():
    response_body = requests.put(url + endpoint_single_user, {'job': 'zion resident'}).json()

    assert 'name' not in response_body


def test_delete_status_code():
    response = requests.delete(url + endpoint_single_user)

    assert response.status_code == 204


def test_register_successful_status_code():
    response = requests.post(
        url=url + endpoint_register,
        json={'email': 'eve.holt@reqres.in', 'password': 'pistol'}
    )

    assert response.status_code == 200


def test_register_successful_json_schema():
    response_body = requests.post(
        url=url + endpoint_register,
        json={'email': 'eve.holt@reqres.in', 'password': 'pistol'}
    ).json()

    validate(response_body, register_successful_schema)


def test_register_unsuccessful_status_code():
    response = requests.post(url + endpoint_register, {'email': 'eve.holt@reqres.in'})

    assert response.status_code == 400


def test_register_unsuccessful_json_schema():
    response_body = requests.post(url + endpoint_register, {'email': 'eve.holt@reqres.in'}).json()

    validate(response_body, register_unsuccessful_schema)


def test_register_unsuccessful_error_message():
    response_body = requests.post(url + endpoint_register, {'email': 'eve.holt@reqres.in'}).json()

    assert response_body['error'] == 'Missing password'
