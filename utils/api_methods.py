import json
import allure
import requests
from allure_commons.types import AttachmentType

url = 'https://reqres.in'


def get_api_request(endpoint, **kwargs):
    with allure.step('API request'):
        response = requests.get(url + endpoint, **kwargs)
        allure.attach(
            body=json.dumps(response.json(), indent=4, ensure_ascii=True),
            name='Response',
            attachment_type=AttachmentType.JSON,
            extension='.json'
        )
        return response
