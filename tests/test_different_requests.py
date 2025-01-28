import requests
from jsonschema import validate
from json_schemas.schemas import add_user, get_info_about_user, change_data_user, register_new_user, unsuccessful_register_new_user


def test_post():
    response = requests.post("https://reqres.in/api/users", data={"name": "jacki-chan", "job": "actor"})
    response_data = response.json()
    assert response.status_code == 201, f"Возникла ошибка:{response.text}"
    validate(response_data, add_user)
    assert response_data["name"] == "jacki-chan", f"Ожидалось имя 'jacki-chan', но получено {response_data['name']}"
    assert response_data["job"] == "actor", f"Ожидалась работа 'actor', но получена {response_data['job']}"
    assert "id" in response_data, "Ожидалось наличие ключа 'id' в ответе"


def test_get_true_info():
    response = requests.get("https://reqres.in/api/users/2")
    response_data = response.json()
    assert response.status_code == 200, f"Возникла ошибка:{response.text}"
    validate(response_data, get_info_about_user)
    assert response_data["data"]["id"] == 2, f"Ожидался id 2, но получено {response_data['data']['id']}"
    assert response_data["data"][
               "first_name"] == "Janet", f"Ожидалось имя 'Janet', но получено {response_data['data']['first_name']}"


def test_get_false_info():
    response = requests.get("https://reqres.in/api/users/77")
    response_data = response.json()
    assert response.status_code == 404, f"Возникла ошибка:{response.text}"
    assert response_data == {}, F"Возникла ошибка:{response.text}"


def test_update():
    response = requests.put("https://reqres.in/api/users/2", data={"name": "morpheus", "job": "mr.flex"})
    response_data = response.json()
    assert response.status_code == 200, f"Возникла ошибка: {response.text}"
    assert response_data["name"] == "morpheus", f"Ожидалось имя 'morpheus', но получено {response_data['name']}"
    assert response_data["job"] == "mr.flex", f"Ожидалась работа 'mr.flex', но получена {response_data['job']}"
    expected_keys = {"name", "job", "updatedAt"}
    assert expected_keys.issubset(
        response_data.keys()), f"Ожидалось наличие ключей {expected_keys}, но получены: {response_data.keys()}"
    validate(response_data, change_data_user)


def test_successful_register():
    response = requests.post("https://reqres.in/api/register",
                             data={"email": "eve.holt@reqres.in", "password": "pistol"})
    response_data = response.json()
    assert response.status_code == 200, f"Возникла ошибка:{response.text}"
    assert "id" in response_data, "Ожидалось наличие ключа 'id' в ответе"
    assert "token" in response_data, "Ожидалось наличие ключа 'token' в ответе"
    validate(response_data, register_new_user)


def test_unsuccessful_register():
    response = requests.post("https://reqres.in/api/register")
    response_data = response.json()
    assert response.status_code == 400, f"Возникла ошибка:{response.text}"
    assert "error" in response_data, "Ожидалось наличие ключа 'error' в ответе"
    validate(response.json(), unsuccessful_register_new_user)


def test_delete():
    response = requests.delete("https://reqres.in/api/users/2")
    assert response.status_code == 204, f"Возникла ошибка:{response.text}"
