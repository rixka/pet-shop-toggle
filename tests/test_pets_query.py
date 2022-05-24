from app import api
from utils import JSON_MIME_TYPE, Toggler

from jsonschema import validate


SCHEMA = {
          'type': 'array',
          'items': {
            'type': 'object',
            'properties': {
              'animal': { 'type': 'string' },
              'name': { 'type': 'string' },
              'adopted': { 'type': 'boolean' },
              'age': { 'type': 'integer' },
              'description': { 'type': 'string' }
            },
            'required': [ 'animal', 'name', 'age' ]
          }
        }


def test_list():
    res = api.test_client().get('/pets')

    assert res.status_code == 200
    assert validate(res.json['data'], SCHEMA) is None
    assert len(res.json['data']) == 12

def test_list_filter_dog_not_beta(mocker):
    mocker.patch.object(Toggler, 'check_flag', return_value=False)
    res = api.test_client().get('/pets?animal=dog')

    assert res.status_code == 200
    assert res.mimetype == JSON_MIME_TYPE
    assert validate(res.json['data'], SCHEMA) is None
    assert len(res.json['data']) == 12

def test_list_filter_dog(mocker):
    mocker.patch.object(Toggler, 'check_flag', return_value=True)
    res = api.test_client().get('/pets?animal=dog')

    assert res.status_code == 200
    assert res.mimetype == JSON_MIME_TYPE
    assert validate(res.json['data'], SCHEMA) is None
    assert len(res.json['data']) == 3

def test_list_bad_filter(mocker):
    mocker.patch.object(Toggler, 'check_flag', return_value=True)
    res = api.test_client().get('/pets?breed=poodle')

    assert res.status_code == 400
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Bad Request' }

def test_animal_not_found(mocker):
    mocker.patch.object(Toggler, 'check_flag', return_value=True)
    res = api.test_client().get('/pets?animal=unicorn')

    assert res.status_code == 404
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Not Found' }
