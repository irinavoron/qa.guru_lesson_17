import json
import allure
import requests
from allure_commons.types import AttachmentType

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
