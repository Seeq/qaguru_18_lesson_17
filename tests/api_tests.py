import requests
from jsonschema import validate

import schemas
from schemas import post_users

url = 'https://reqres.in'
user_api_endpoint = '/api/users'
register_api_endpoint = '/api/register'

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
    response = requests.post(url + user_api_endpoint, data=payload, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body['name'] == 'morpheus'
    assert body['job'] == 'leader'
    validate(body , post_users)

def test_get_list_of_users():
    params = {"page": 2}
    response = requests.get(url + user_api_endpoint, params=params, headers=headers)
    body = response.json()
    assert response.status_code == 200
    assert body["page"] == 2

def test_get_user_by_id():
    user_id = '2'
    response = requests.get(url + user_api_endpoint + '/' + user_id, headers=headers)
    body = response.json()
    assert response.status_code == 200
    assert body["data"]["email"] == "janet.weaver@reqres.in"
    assert body["data"]["first_name"] == "Janet"
    assert body["data"]["last_name"] == "Weaver"
    validate(body, schemas.get_user)

def test_get_user_by_id_not_found():
    user_id = '0'
    response = requests.get(url + user_api_endpoint + '/' + user_id, headers=headers)
    assert response.status_code == 404

def test_create_user():
    name = 'Sergey'
    job = 'Qa'
    payload = {
        'name': name,
        'job': job
    }
    response = requests.post(url + user_api_endpoint, json=payload, headers=headers)
    assert response.status_code == 201
    validate(response.json(), schema=schemas.create_user)

def test_update_user():
    name = 'Sergey'
    job = 'QA'
    user_id = '2'

    payload = {
        'name': name,
        'job': job
    }
    response = requests.put(url + user_api_endpoint + '/' + user_id, json=payload, headers=headers)
    assert response.status_code == 200
    validate(response.json(), schemas.update_user)

def test_delete_user():
    user_id = '2'
    response = requests.delete(url + user_api_endpoint + '/' + user_id, headers=headers)
    assert response.status_code == 204


def test_register_user_success():
    email = 'eve.holt@reqres.in'
    password = 'pistol'
    payload = {
        'email': email,
        'password': password
    }
    response = requests.post(url + register_api_endpoint, json=payload, headers=headers)
    assert response.status_code == 200
    validate(response.json(), schemas.register_user_success)


def test_register_user_fail():
    email = 'abc'
    password = 'pistol'
    payload = {
        'email': email,
        'password': password
    }
    response = requests.post(url + register_api_endpoint, json=payload, headers=headers)
    assert response.status_code == 400
    validate(response.json(), schema=schemas.register_user_fail)

