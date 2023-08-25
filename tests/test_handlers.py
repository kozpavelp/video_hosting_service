import json
from uuid import uuid4

async def test_create_user(client, get_user_from_db):
    user_data = {
        'name': 'Pavel',
        'surname': 'Kozl',
        'email': 'kozpavelp@gmail.com'
    }
    resp = client.post('/user/', data=json.dumps(user_data))
    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json['name'] == user_data['name']
    assert resp_json['surname'] == user_data['surname']
    assert resp_json['email'] == user_data['email']
    assert resp_json['is_active'] is True
    users_from_db = await get_user_from_db(resp_json['user_id'])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db['name'] == user_data['name']
    assert user_from_db['surname'] == user_data['surname']
    assert user_from_db['email'] == user_data['email']
    assert user_from_db['is_active'] is True
    assert str(user_from_db['user_id']) == resp_json['user_id']


async def test_delete_user(client, create_user_in_db, get_user_from_db):
    user_data = {
        'user_id': uuid4(),
        'name': 'Pavel',
        'surname': 'Kozl',
        'email': 'kozpavelp@gmail.com',
        'is_active': True
    }
    await create_user_in_db(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data['user_id'])}
    users_from_db = await get_user_from_db(user_data['user_id'])
    user_from_db = dict(users_from_db[0])
    assert user_from_db['name'] == user_data['name']
    assert user_from_db['surname'] == user_data['surname']
    assert user_from_db['email'] == user_data['email']
    assert user_from_db['is_active'] is False
    assert user_from_db['user_id'] == user_data['user_id']


async def test_get_user(client, create_user_in_db, get_user_from_db):
    user_data = {
        'user_id': uuid4(),
        'name': 'Pavel',
        'surname': 'Kozl',
        'email': 'kozpavelp@gmail.com',
        'is_active': True
    }
    await create_user_in_db(**user_data)
    resp = client.get(f'/user/?user_id={user_data["user_id"]}')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json['user_id'] == str(user_data['user_id'])
    assert resp_json['name'] == user_data['name']
    assert resp_json['surname'] == user_data['surname']
    assert resp_json['email'] == user_data['email']
    assert resp_json['is_active'] == user_data['is_active']


async def test_update_users(client, create_user_in_db, get_user_from_db):
    user_data = {
        'user_id': uuid4(),
        'name': 'Pavel',
        'surname': 'Kozl',
        'email': 'kozpavelp@gmail.com',
        'is_active': True
    }
    updated_user_data = {
        'name': 'jopa',
        'surname': 'lavash',
        'email': 'punk@srenk.com'
    }
    await create_user_in_db(**user_data)
    resp = client.patch(f'/user/?user_id={user_data["user_id"]}', data=json.dumps(updated_user_data))
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json['updated_user_id'] == str(user_data['user_id'])
    users_from_db = await get_user_from_db(user_data['user_id'])
    user_from_db = dict(users_from_db[0])
    assert user_from_db['name'] == updated_user_data['name']
    assert user_from_db['surname'] == updated_user_data['surname']
    assert user_from_db['email'] == updated_user_data['email']
    assert user_from_db['user_id'] == user_data['user_id']
    assert user_from_db['is_active'] is user_data['is_active']
