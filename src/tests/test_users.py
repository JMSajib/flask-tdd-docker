from http import client
import json

from src import db
from src.api.models import User

def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'jahidul',
            'email': 'jahidul.momin@brilliant.com.bd'
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'jahidul.momin@brilliant.com.bd was added' in data.get('message')

def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data.get('message')

def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({"email": "john@gmail.com"}),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data.get('message')

def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/users',
        data=json.dumps({
            "email": "jahidul.momin@brilliant.com.bd", 
            "username": "jahid"
        }),
        content_type='application/json'
    )
    resp = client.post(
        '/users',
        data=json.dumps({
            "email": "jahidul.momin@brilliant.com.bd", 
            "username": "jahid"
        }),
        content_type='application/json'
    )

    
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Email already exist' in data.get('message')

def test_single_user(test_app, test_database):
    user = User(username='jahid', email='jahidul.momin@briliant.com.bd')
    db.session.add(user)
    db.session.commit()
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'jahid' in data.get('username')
    assert 'jahidul.momin@briliant.com.bd' in data.get('email')

def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/users/99')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'user 99 does not exist' in data.get('message')
