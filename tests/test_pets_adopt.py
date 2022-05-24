from app import api
from utils import JSON_MIME_TYPE

from bson.json_util import dumps
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
pet = db.pets.find_one()
pet_id = str(pet['_id'])


def test_adopt_pet():
    db.pets.update_one(
        { '_id': pet['_id'] },
        { '$set': { 'adopted': False }}
    )

    res = api.test_client().post(
        '/'.join(['/pets', pet_id, 'adopt']),
        data=dumps(DATA),
        headers=HEADERS
    )

    assert res.status_code == 201
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'message': 'The item was created successfully' }

    updated_pet = db.pets.find_one({ '_id': pet['_id'] })
    assert pet['adopted'] == True

    res_adopt = db.adoptions.find_one(DATA)
    assert res_adopt['address'] == DATA['address']
    assert res_adopt['name'] == DATA['name']

def test_adopt_failed():
    pet = db.pets.find_one()
    pet_id = str(pet['_id'])

    db.pets.update_one(
        { '_id': pet['_id'] },
        { '$set': { 'adopted': True }}
    )

    res = api.test_client().post(
        '/'.join(['/pets', pet_id, 'adopt']),
        data=dumps(DATA),
        headers=HEADERS
    )

    assert res.status_code == 409
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == {'error': 'Conflict: Pet already adopted'}

    pet = db.pets.find_one({ '_id': pet['_id'] })
    assert pet['adopted'] == True

    res_adopt = db.adoptions.find_one(DATA)
    assert res_adopt['address'] == DATA['address']
    assert res_adopt['name'] == DATA['name']

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
