from http import client
import json

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