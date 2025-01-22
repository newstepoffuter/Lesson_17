import requests
from jsonschema import validate
from schemas import post_method, get_method, put_method, register, bad_register


def test_post():
    response = requests.post("https://reqres.in/api/users", data={"name": "jacki-chan", "job": "actor"})
    assert response.status_code == 201, f"Возникла ошибка:{response.text}"
    validate(response.json(), post_method)


def test_get_true_info():
    response = requests.get("https://reqres.in/api/users/2")
    assert response.status_code == 200, f"Возникла ошибка:{response.text}"
    validate(response.json(), get_method)


def test_get_false_info():
    response = requests.get("https://reqres.in/api/users/77")
    assert response.status_code == 404, f"Возникла ошибка:{response.text}"
    assert response.json() == {}, F"Возникла ошибка:{response.text}"


def test_update():
    response = requests.put("https://reqres.in/api/users/2", data={"name": "morpheus", "job": "mr.flex"})
    assert response.status_code == 200, f"Возникла ошибка:{response.text}"
    validate(response.json(), put_method)


def test_successful_register():
    response = requests.post("https://reqres.in/api/register",
                             data={"email": "eve.holt@reqres.in", "password": "pistol"})
    assert response.status_code == 200, f"Возникла ошибка:{response.text}"
    validate(response.json(), register)


def test_unsuccessful_register():
    response = requests.post("https://reqres.in/api/register")
    assert response.status_code == 400, f"Возникла ошибка:{response.text}"
    validate(response.json(), bad_register)


def test_delete():
    response = requests.delete("https://reqres.in/api/users/2")
    assert response.status_code == 204, f"Возникла ошибка:{response.text}"
