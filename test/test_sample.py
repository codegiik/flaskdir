import pytest
from faker import Faker
import random 
import sys

sys.path.append('../flaskdir')

import appname
import appname.routes.name.middleware as name_middleware

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 8888
DEFAULT_URL = 'http://{}:{}'.format(DEFAULT_HOST, DEFAULT_PORT)

fake = Faker()

generate_url = lambda x: '{}/{}'.format(DEFAULT_URL, x)

@pytest.fixture(scope='session')
def flask_app():
    appname.add_routes_to_app()
    return appname.app.test_client()

def test_hello_world(flask_app):
    res = flask_app.get('/')
    assert res.text == 'Hello, world!'

def test_hello_name(flask_app):
    name = fake.name()
    res = flask_app.get('/name/{}'.format(name + '/'))
    assert res.text == 'Hello, {}!'.format(name)

def test_banned_name(flask_app):
    name = random.choice(name_middleware.BANNED_NAMES)

    res = flask_app.get('/name/{}'.format(name + '/'))

    assert res.status_code == 400
    assert res.text == 'Bad Request'
    
if __name__ == '__main__':
    pytest.main()
