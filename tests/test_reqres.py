import json
from allure_commons.types import AttachmentType
from jsonschema import validate
import schemas
import requests
import allure
from requests import Response

base_url = 'https://reqres.in'
users = '/api/users'
single_user = '/api/users/2'
user_not_found = '/api/users/23'
register = '/api/register'


def response_attaching(response: Response):
    if response.request.body:
        allure.attach(
            body=json.dumps(response.json(), indent=4, ensure_ascii=True),
            name='Response',
            attachment_type=AttachmentType.JSON,
            extension='.json'
        )


def api_request(endpoint, method, data=None, params=None):
    url = base_url + endpoint
    with allure.step("API request"):
        response = requests.request(method, url, data=data, params=params)
        response_attaching(response)
        return response


def test_list_users_status_code_and_schema():
    response = api_request(
        endpoint=users,
        method='GET',
        params={'page': 2}
    )
    response_body = response.json()

    assert response.status_code == 200
    validate(response_body, schemas.list_users_schema)


def test_list_users_number_per_page():
    response_body = api_request(
        endpoint=users,
        method='GET',
        params={'page': 2}
    ).json()

    assert response_body['per_page'] == len(response_body['data'])


def test_single_user_status_code_and_schema():
    response = api_request(
        endpoint=single_user,
        method='GET'
    )
    response_body = response.json()

    assert response.status_code == 200
    validate(response_body, schemas.single_user_schema)


def test_user_not_found_status_code():
    response = api_request(
        endpoint=user_not_found,
        method='GET'
    )

    assert response.status_code == 404


def test_user_not_found_empty_response_body():
    response_body = api_request(
        endpoint=user_not_found,
        method='GET'
    ).json()

    assert not response_body


def test_create_status_code_and_schema():
    response = api_request(
        endpoint=users,
        method='POST',
        data={'name': 'morpheus', 'job': 'leader'}
    )
    response_body = response.json()

    assert response.status_code == 201
    validate(response_body, schemas.create_schema)


def test_create_name_and_job_in_response():
    name = 'morpheus'
    job = 'leader'
    response_body = api_request(
        endpoint=users,
        method='POST',
        data={'name': name, 'job': job}
    ).json()

    assert response_body['name'] == name
    assert response_body['job'] == job


def test_update_status_code_and_schema():
    response = api_request(
        endpoint=single_user,
        method='PUT',
        data={'name': 'morpheus', 'job': 'zion resident'}
    )
    response_body = response.json()

    assert response.status_code == 200
    validate(response_body, schemas.update_schema)


def test_update_no_name_in_response_body():
    response_body = api_request(
        endpoint=single_user,
        method='PUT',
        data={'job': 'zion resident'}
    ).json()

    assert 'name' not in response_body


def test_delete_status_code():
    response = api_request(
        endpoint=single_user,
        method='DELETE')

    assert response.status_code == 204


def test_register_successful_status_code_and_schema():
    response = api_request(
        endpoint=register,
        method='POST',
        data={'email': 'eve.holt@reqres.in', 'password': 'pistol'}
    )
    response_body = response.json()

    assert response.status_code == 200
    validate(response_body, schemas.register_successful_schema)


def test_register_unsuccessful_status_code_and_schema():
    response = api_request(
        endpoint=register,
        method='POST',
        data={'email': 'eve.holt@reqres.in'}
    )
    response_body = response.json()

    assert response.status_code == 400
    validate(response_body, schemas.register_unsuccessful_schema)


def test_register_unsuccessful_error_message():
    response_body = api_request(
        endpoint=register,
        method='POST',
        data={'email': 'eve.holt@reqres.in'}
    ).json()

    assert response_body['error'] == 'Missing password'
