import json

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
