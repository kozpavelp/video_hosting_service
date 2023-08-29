from uuid import uuid4

from tests.conftest import create_test_auth_headers


async def test_get_user(client, create_user_in_db, get_user_from_db):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
    }
    await create_user_in_db(**user_data)
    resp = client.get(
        f'/user/?user_id={user_data["user_id"]}',
        headers=create_test_auth_headers(user_data["email"]),
    )
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["user_id"] == str(user_data["user_id"])
    assert resp_json["name"] == user_data["name"]
    assert resp_json["surname"] == user_data["surname"]
    assert resp_json["email"] == user_data["email"]
    assert resp_json["is_active"] == user_data["is_active"]


async def test_get_user_not_found(client, create_user_in_db, get_user_from_db):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
    }
    await create_user_in_db(**user_data)
    id_to_find = uuid4()
    resp = client.get(
        f"/user/?user_id={id_to_find}",
        headers=create_test_auth_headers(user_data["email"]),
    )
    assert resp.status_code == 404
    assert resp.json() == {
        "detail": f"User with id:{id_to_find} not found in database."
    }
