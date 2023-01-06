import pytest
from faker import Faker
import random 
import sys

sys.path.append('../flaskdir')

import appname as flask_main
import appname.routes.name.middleware as name_middleware

fake = Faker()

@pytest.fixture(scope='session')
def flask_app():
    flask_main.add_routes_to_app()
    return flask_main.app.test_client()

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
