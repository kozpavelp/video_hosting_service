from uuid import uuid4

from database.dals import RoleList
from tests.conftest import create_test_auth_headers


async def test_delete_user(client, create_user_in_db, get_user_from_db):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozlassd",
        "email": "kozpavel1p@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    await create_user_in_db(**user_data)
    resp = client.delete(
        f"/user/?user_id={user_data['user_id']}",
        headers=create_test_auth_headers(user_data["email"]),
    )
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_db(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_delete_user_not_found(client, create_user_in_db):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    await create_user_in_db(**user_data)
    user_uuid = uuid4()
    resp = client.delete(
        f"/user/?user_id={user_uuid}",
        headers=create_test_auth_headers(user_data["email"]),
    )
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id:{user_uuid} not found in database."}


async def test_delete_user_bad_cred(client, create_user_in_db):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl22",
        "email": "kozpavel1p@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    await create_user_in_db(**user_data)
    resp = client.delete(
        f"/user/?user_id={user_data['user_id']}",
        headers=create_test_auth_headers(user_data["email"] + "wrong"),
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}


async def test_delete_user_wrong_token(client, create_user_in_db):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    await create_user_in_db(**user_data)
    wrong_headers = create_test_auth_headers(user_data["email"])
    wrong_headers["Authorization"] += "wrong"
    resp = client.delete(
        f"/user/?user_id={user_data['user_id']}", headers=wrong_headers
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}


async def test_delete_user_no_token(client, create_user_in_db):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    await create_user_in_db(**user_data)
    user_uuid = uuid4()
    resp = client.delete(f"/user/?user_id={user_uuid}")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}


async def test_delete_user_with_privilege(client, create_user_in_db, get_user_from_db):
    user_to_delete = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp1@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    mega_user = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp2@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_ADMIN],
    }
    await create_user_in_db(**user_to_delete)
    await create_user_in_db(**mega_user)
    resp = client.delete(
        f'/user/?user_id={user_to_delete["user_id"]}',
        headers=create_test_auth_headers(mega_user["email"]),
    )
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_to_delete["user_id"])}
    users_from_db = await (get_user_from_db(user_to_delete["user_id"]))
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_to_delete["name"]
    assert user_from_db["surname"] == user_to_delete["surname"]
    assert user_from_db["email"] == user_to_delete["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_to_delete["user_id"]


async def test_user_delete_user(client, create_user_in_db, get_user_from_db):
    user1 = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp1@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    user2 = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpavelp2@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    await create_user_in_db(**user1)
    await create_user_in_db(**user2)
    resp = client.delete(
        f'/user/?user_id={user1["user_id"]}',
        headers=create_test_auth_headers(user2["email"]),
    )
    assert resp.status_code == 403
