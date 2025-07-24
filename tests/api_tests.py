import requests
from jsonschema import validate
from tests.schemas import post_users

url = 'https://reqres.in'
endpoint = '/api/users'

name = 'morpheus'
job = 'leader'

payload = {
    "name": name,
    "job": job
}

headers = {
    'x-api-key': 'reqres-free-v1'
}

def test_create_user():
    response = requests.post(url + endpoint, data=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()['name'] == 'morpheus'  # Проверка имени
    assert response.json()['job'] == 'leader'
    body = response.json()
    validate(body , post_users)
