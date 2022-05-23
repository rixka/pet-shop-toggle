from app import api
from utils import JSON_MIME_TYPE

from jsonschema import validate
from pymongo import MongoClient


SCHEMA = {
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


db = MongoClient('localhost', 27017).development
pet_id = str(db.pets.find_one()['_id'])

def test_pets_id():
    res = api.test_client().get(
        '/'.join(['/pets', pet_id])
    )

    assert res.status_code == 200
    assert res.mimetype == JSON_MIME_TYPE
    assert validate(res.json['data'], SCHEMA) is None

def test_pets_no_id():
    res = api.test_client().get('/pets/')

    assert res.status_code == 404
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Not Found' }

def test_bad_id():
    res = api.test_client().get('/pets/123')

    assert res.status_code == 400
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Bad Request' }

def test_pet_not_found():
    res = api.test_client().get('/pets/5abd9fbcd48b40737d3c14db')

    assert res.status_code == 404
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Not Found' }
