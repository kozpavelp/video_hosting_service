from uuid import uuid4


async def test_delete_user(client, create_user_in_db, get_user_from_db):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
    }
    await create_user_in_db(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_db(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_delete_user_not_found(client):
    user_uuid = uuid4()
    resp = client.delete(f"/user/?user_id={user_uuid}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id:{user_uuid} not found in database."}
