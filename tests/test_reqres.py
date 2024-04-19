from jsonschema import validate
from schemas import list_users_schema, single_user_schema, create_schema, update_schema, register_successful_schema, \
    register_unsuccessful_schema

from utils.api_methods import get_api_request, post_api_request, put_api_request, delete_api_request

users = '/api/users'
single_user = '/api/users/2'
user_not_found = '/api/users/23'
register = '/api/register'


def test_list_users_status_code():
    response = get_api_request(
        endpoint=users,
        params={'page': 2}
    )

    assert response.status_code == 200


def test_list_users_json_schema():
    response_body = get_api_request(
        endpoint=users,
        params={'page': 2}
    ).json()

    validate(response_body, list_users_schema)


def test_list_users_number_per_page():
    response_body = get_api_request(
        endpoint=users,
        params={'page': 2}
    ).json()

    assert response_body['per_page'] == len(response_body['data'])


def test_single_user_status_code():
    response = get_api_request(endpoint=single_user)

    assert response.status_code == 200


def test_single_user_json_schema():
    response_body = get_api_request(endpoint=single_user).json()

    validate(response_body, single_user_schema)


def test_user_not_found_status_code():
    response = get_api_request(endpoint=user_not_found)

    assert response.status_code == 404


def test_user_not_found_empty_response_body():
    response_body = get_api_request(endpoint=user_not_found).json()

    assert not response_body


def test_create_status_code():
    response = post_api_request(
        endpoint=users,
        payload={'name': 'morpheus', 'job': 'leader'}
    )

    assert response.status_code == 201


def test_create_json_schema():
    response_body = post_api_request(
        endpoint=users,
        payload={'name': 'morpheus', 'job': 'leader'}
    ).json()

    validate(response_body, create_schema)


def test_create_name_and_job_in_response():
    name = 'morpheus'
    job = 'leader'
    response_body = post_api_request(
        endpoint=users,
        payload={'name': name, 'job': job}
    ).json()

    assert response_body['name'] == name
    assert response_body['job'] == job


def test_update_status_code_put():
    response = put_api_request(
        endpoint=single_user,
        payload={'name': 'morpheus', 'job': 'zion resident'}
    )

    assert response.status_code == 200


def test_update_json_schema():
    response_body = put_api_request(
        endpoint=single_user,
        payload={'name': 'morpheus', 'job': 'zion resident'}
    ).json()

    validate(response_body, update_schema)


def test_update_no_name_in_response_body():
    response_body = put_api_request(
        endpoint=single_user,
        payload={'job': 'zion resident'}
    ).json()

    assert 'name' not in response_body


def test_delete_status_code():
    response = delete_api_request(endpoint=single_user)

    assert response.status_code == 204


def test_register_successful_status_code():
    response = post_api_request(
        endpoint=register,
        payload={'email': 'eve.holt@reqres.in', 'password': 'pistol'}
    )

    assert response.status_code == 200


def test_register_successful_json_schema():
    response_body = post_api_request(
        endpoint=register,
        payload={'email': 'eve.holt@reqres.in', 'password': 'pistol'}
    ).json()

    validate(response_body, register_successful_schema)


def test_register_unsuccessful_status_code():
    response = post_api_request(
        endpoint=register,
        payload={'email': 'eve.holt@reqres.in'}
    )

    assert response.status_code == 400


def test_register_unsuccessful_json_schema():
    response_body = post_api_request(
        endpoint=register,
        payload={'email': 'eve.holt@reqres.in'}
    ).json()

    validate(response_body, register_unsuccessful_schema)


def test_register_unsuccessful_error_message():
    response_body = post_api_request(
        endpoint=register,
        payload={'email': 'eve.holt@reqres.in'}
    ).json()

    assert response_body['error'] == 'Missing password'
