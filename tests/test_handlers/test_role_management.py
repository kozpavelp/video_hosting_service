from uuid import uuid4

from database.models import RoleList
from tests.conftest import create_test_auth_headers


async def test_add_admin_role(client, create_user_in_db, get_user_from_db):
    user_root = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpave2lp1@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_SUPERADMIN],
    }
    user_to_promote = {
        "user_id": uuid4(),
        "name": "Vasiliy",
        "surname": "Poncho",
        "email": "koasasdzpave2lp1@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER],
    }
    await create_user_in_db(**user_root)
    await create_user_in_db(**user_to_promote)
    resp = client.patch(
        f'/user/admin_role/?user_id={user_to_promote["user_id"]}',
        headers=create_test_auth_headers(user_root["email"]),
    )
    resp_json = resp.json()
    assert resp.status_code == 200
    updated_user = await get_user_from_db(resp_json["updated_user_id"])
    assert len(updated_user) == 1
    updated_user = dict(updated_user[0])
    assert updated_user["user_id"] == user_to_promote["user_id"]
    assert RoleList.PORTAL_ADMIN in updated_user["roles"]


async def test_revoke_admin_role(client, create_user_in_db, get_user_from_db):
    user_root = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Kozl",
        "email": "kozpave2lp1@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_SUPERADMIN],
    }
    user_to_revoke = {
        "user_id": uuid4(),
        "name": "Vasiliy",
        "surname": "Poncho",
        "email": "psina@gmail.com",
        "is_active": True,
        "password": "TestPwd1",
        "roles": [RoleList.PORTAL_USER, RoleList.PORTAL_ADMIN],
    }
    await create_user_in_db(**user_root)
    await create_user_in_db(**user_to_revoke)
    resp = client.delete(
        f'/user/admin_role/?user_id={user_to_revoke["user_id"]}',
        headers=create_test_auth_headers(user_root["email"]),
    )
    resp_json = resp.json()
    assert resp.status_code == 200
    updated_user = await get_user_from_db(resp_json["updated_user_id"])
    assert len(updated_user) == 1
    updated_user = dict(updated_user[0])
    assert updated_user["user_id"] == user_to_revoke["user_id"]
    assert RoleList.PORTAL_ADMIN not in updated_user["roles"]
