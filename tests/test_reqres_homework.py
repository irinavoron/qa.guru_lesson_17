import json
import allure
import requests
from allure_commons.types import AttachmentType
from jsonschema import validate

from tests.schemas import create_json_schema, update_json_schema, register_json_schema, \
    register_unsuccessful_json_schema

base_url = 'https://reqres.in/api'


def api_get(url, **kwargs):
    with allure.step('API get request'):
        response = requests.get(base_url + url, **kwargs)
        allure.attach(
            body=json.dumps(response.json(), indent=4, ensure_ascii=True),
            name='response',
            attachment_type=AttachmentType.JSON,
            extension='.json')
        return response


def api_post(url, payload, **kwargs):
    with allure.step('API post request'):
        response = requests.post(base_url + url, payload, **kwargs)
        allure.attach(
            body=json.dumps(response.json(), indent=4, ensure_ascii=True),
            name='response',
            attachment_type=AttachmentType.JSON,
            extension='.json'
        )
        return response


def api_put(url, payload, **kwargs):
    with allure.step('API post request'):
        response = requests.put(base_url + url, payload, **kwargs)
        allure.attach(
            body=json.dumps(response.json(), indent=4, ensure_ascii=True),
            name='response',
            attachment_type=AttachmentType.JSON,
            extension='.json'
        )
        return response


def api_delete(url, **kwargs):
    with allure.step('API delete request'):
        response = requests.delete(base_url + url, **kwargs)

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
    response = api_post(url='/users', payload={'name': 'morpheus', 'job': 'leader'})
    assert response.status_code == 201


def test_create_json_schema():
    response_body = api_post(url='/users', payload={'name': 'morpheus', 'job': 'leader'}).json()
    validate(response_body, create_json_schema)


def test_create_response_data():
    name = 'morpheus'
    job = 'leader'
    response_body = api_post(url='/users', payload={'name': name, 'job': job}).json()
    assert response_body['name'] == name
    assert response_body['job'] == job


def test_update_status_code():
    response = api_put(url='/users/2', payload={'name': 'morpheus', 'job': 'zion resident'})
    assert response.status_code == 200


def test_update_json_schema():
    response = api_put(url='/users/2', payload={'name': 'morpheus', 'job': 'zion resident'})
    response_body = response.json()
    validate(response_body, update_json_schema)


def test_update_response_data():
    name = 'morpheus'
    job = 'zion resident'
    response = api_put(url='/users/2', payload={'name': name, 'job': job})
    response_body = response.json()
    assert response_body['name'] == name
    assert response_body['job'] == job


def test_delete_status_code():
    response = api_delete(url='/users/2')
    assert response.status_code == 204


def test_register_successful_status_code():
    response = api_post(url='/register', payload={'email': "eve.holt@reqres.in", 'password': "pistol"})
    assert response.status_code == 200


def test_register_successful_json_schema():
    response = api_post(
        url='/register',
        payload={'email': "eve.holt@reqres.in", 'password': "pistol"}
    )
    response_body = response.json()
    validate(response_body, register_json_schema)


def test_register_unsuccessful_status_code():
    response = api_post(
        url='/register',
        payload={'email': "sydney@fife"}
    )
    assert response.status_code == 400


def test_register_unsuccessful_json_schema():
    response = api_post(
        url='/register',
        payload={'email': "sydney@fife"}
    )
    response_body = response.json()
    validate(response_body, schema=register_unsuccessful_json_schema)


def test_register_unsuccessful_error_message():
    response = api_post(
        url='/register',
        payload={'email': "sydney@fife"}
    )
    response_body = response.json()
    assert response_body['error'] == "Missing password"
