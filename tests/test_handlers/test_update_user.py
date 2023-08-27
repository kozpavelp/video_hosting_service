import json
from uuid import uuid4


async def test_update_users(client, create_user_in_db, get_user_from_db):
    user_data = {
        'user_id': uuid4(),
        'name': 'Pavel',
        'surname': 'Kozl',
        'email': 'kozpavelp@gmail.com',
        'is_active': True
    }
    updated_user_data = {
        'name': 'Jora',
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


async def test_update_one(client, create_user_in_db, get_user_from_db):
    users_to_add = [
        {
            'user_id': uuid4(),
            'name': 'Pavel',
            'surname': 'Kozl',
            'email': 'kozpavelp@gmail.com',
            'is_active': True
        },
        {
            'user_id': uuid4(),
            'name': 'Ivan',
            'surname': 'Assas',
            'email': 'Isas@gmail.kz',
            'is_active': True
        },
        {
            'user_id': uuid4(),
            'name': 'Poncho',
            'surname': 'Kofta',
            'email': 'ponko@ya.com',
            'is_active': True
        }
    ]
    data_to_update = {
        'name': 'NePavel',
        'surname': 'NeKozl',
        'email': 'new_life@pochta.pe'
    }
    for user_data in users_to_add:
        await create_user_in_db(**user_data)
    resp = client.patch(f'/user/?user_id={users_to_add[0]["user_id"]}', data=json.dumps(data_to_update))
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json['updated_user_id'] == str(users_to_add[0]['user_id'])
    users_from_db = await get_user_from_db(users_to_add[0]['user_id'])
    user_from_db = dict(users_from_db[0])
    assert user_from_db['name'] == data_to_update['name']
    assert user_from_db['surname'] == data_to_update['surname']
    assert user_from_db['email'] == data_to_update['email']
    #Checking other for no changes
    users_from_db = await get_user_from_db(users_to_add[1]['user_id'])
    user_from_db = dict(users_from_db[0])
    assert user_from_db['name'] == users_to_add[1]['name']
    assert user_from_db['surname'] == users_to_add[1]['surname']
    assert user_from_db['email'] == users_to_add[1]['email']
    assert user_from_db['is_active'] is users_to_add[1]['is_active']
    assert user_from_db['user_id'] == users_to_add[1]['user_id']

    users_from_db = await get_user_from_db(users_to_add[2]['user_id'])
    user_from_db = dict(users_from_db[0])
    assert user_from_db['name'] == users_to_add[2]['name']
    assert user_from_db['surname'] == users_to_add[2]['surname']
    assert user_from_db['email'] == users_to_add[2]['email']
    assert user_from_db['is_active'] is users_to_add[2]['is_active']
    assert user_from_db['user_id'] == users_to_add[2]['user_id']


async def test_update_user_not_found(client):
    data_to_update = {
        'name': 'NoPavel',
        'surname': 'NeKozl',
        'email': 'new_life@pochta.pe'
    }
    user_uuid = uuid4()
    resp = client.patch(f'/user/?user_id={user_uuid}', data=json.dumps(data_to_update))
    assert resp.status_code == 404
    assert resp.json() == {'detail': f'User with id:{user_uuid} not found in database.'}


async def test_update_user_duplicate_email(client, create_user_in_db):
    users_to_add = [
        {
            'user_id': uuid4(),
            'name': 'Pavel',
            'surname': 'Kozl',
            'email': 'kozpavelp@gmail.com',
            'is_active': True
        },
        {
            'user_id': uuid4(),
            'name': 'Ivan',
            'surname': 'Assas',
            'email': 'Isas@gmail.kz',
            'is_active': True
        },
    ]
    email_to_update = {
        'email': users_to_add[1]['email']
    }
    for user_data in users_to_add:
        await create_user_in_db(**user_data)
    resp = client.patch(f'/user/?user_id={users_to_add[0]["user_id"]}', data=json.dumps(email_to_update))
    assert resp.status_code == 503
    assert 'duplicate key value violates unique constraint' in resp.json()["detail"]
