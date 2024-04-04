import json
import requests
from jsonschema import validate

from tests.schemas import post_users


# users_url = "https://reqres.in/api/users"
#
# payload = {'name': 'morpheus', 'job': 'leader'}
#
# response = requests.request("POST", users_url, data=payload)
#
# print(response.text)


def test_schema_from_file():
    url = "https://reqres.in/api/users"
    payload = {'name': 'morpheus', 'job': 'leader'}
    response = requests.post(url, data=payload)
    body = response.json()
    assert response.status_code == 201
    with open('post_users.json') as file:
        validate(body, json.loads(file.read()))


def test_schema_from_var():
    url = "https://reqres.in/api/users"
    payload = {'name': 'morpheus', 'job': 'leader'}
    response = requests.post(url, data=payload)
    body = response.json()

    validate(body, schema=post_users)


def test_data_in_response():
    url = "https://reqres.in/api/users"
    name = 'morpheus'
    job = 'leader'
    response = requests.post(url, data={'name': name, 'job': job})
    body = response.json()

    assert body['name'] == name
    assert body['job'] == job


def test_get():
    response = requests.get('https://reqres.in/api/users', params={'page': 2})
    ids = [element['id'] for element in response.json()['data']]
    assert len(ids) == len(set(ids))
