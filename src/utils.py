from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import make_response, request, abort

import ldclient
from ldclient.config import Config

JSON_MIME_TYPE = 'application/json'
SUPPORTED_FIELDS = ['animal', 'name', 'age', 'adopted' ]

def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(dumps(data), status, headers)

def validate_object_id(_id):
    if ObjectId.is_valid(_id):
        return ObjectId(_id)
    else:
        abort(400)

def validate_pet_exists(db, _id):
    res = db.pets.find_one({
        '_id': validate_object_id(_id)
    })
    return res or abort(404)


class Toggler:
    def __init__(self):
        SDK_KEY = '' # TODO: UPDATE YOUR SDK KEY
        ldclient.set_config(Config(SDK_KEY))
        self.client = ldclient.get()

    def check_db_flag(self):
        return self.client.variation('swap-database', {"key": "user@test.com"}, False)

    def check_flag(self, key):
        return self.client.variation(key, {"key": "user@test.com"}, False)
