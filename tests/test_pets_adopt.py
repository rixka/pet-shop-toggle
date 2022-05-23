from app import api
from utils import JSON_MIME_TYPE

from bson.json_util import dumps
from jsonschema import validate
from pymongo import MongoClient


HEADERS = {
    'Content-Type': JSON_MIME_TYPE,
    'Accept': JSON_MIME_TYPE
}

DATA = {
    'name': 'Wallace Grommitson',
    'address': '123 Fake Street'
}

db = MongoClient('localhost', 27017).development

def test_adopt_pet():
    pet = db.pets.find_one()
    pet_id = str(pet['_id'])

    res = api.test_client().post(
        '/'.join(['/pets', pet_id, 'adopt']),
        data=dumps(DATA),
        headers=HEADERS
    )

    assert res.status_code == 201
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'message': 'The item was created successfully' }
    assert res.headers.get('Location') is not None

    pet = db.pets.find_one({ '_id': pet_id })
    assert pet['adopt'] == True

    res_adopt = db.adopt.find_one(DATA)
    assert res_adopt.json == DATA

def test_adopt_bad_path():
    res = api.test_client().post(
        '/pets/adopt',
        data=dumps(DATA),
        headers=HEADERS
    )

    assert res.status_code == 404
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Not Found' }

def test_adopt_no_id():
    res = api.test_client().post(
        '/pets//adopt',
        data=dumps(DATA),
        headers=HEADERS    
    )

    assert res.status_code == 400
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Bad Request' }

def test_adopt_bad_id():
    res = api.test_client().post(
        '/pets/xzy/adopt',
        data=dumps(DATA),
        headers=HEADERS
    )

    assert res.status_code == 400
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Bad Request' }

def test_adopt_not_found():
    res = api.test_client().post(
        '/pets/62867b066cd97e903a3ca726/adopt',
        data=dumps(DATA),
        headers=HEADERS
    )

    assert res.status_code == 404
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Not Found' }
