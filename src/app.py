from os import environ
from pymongo import MongoClient
from flask import Flask, request, abort

from utils import (
    JSON_MIME_TYPE, SUPPORTED_FIELDS,
    json_response, validate_object_id
)

MONGO_HOST = environ.get('MONGO_HOST') or 'localhost'
MONGO_DB = environ.get('MONGO_DB') or 'development'

api = Flask(__name__)
db = MongoClient(MONGO_HOST, 27017)[MONGO_DB]


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    abort(404)

@api.route('/health', methods=['GET'])
def health():
    return json_response({'status': 'ok'}, 200)

@api.route('/pets', methods=['GET'])
def pets_list():
    query = {}
    args = request.args or {}

    for key in args:
        if key not in SUPPORTED_FIELDS: abort(400)
        query[key] = args[key]

    data = list(db.pets.find(query)) or abort(404)
    return json_response({ 'data': data })

@api.route('/pets/<pet_id>', methods=['GET'])
def find_pet(pet_id):
    pet = validate_pet_exists(pet_id)
    return json_response({'data': pet })

@api.route('/pets/<pet_id>/adopt', methods=['POST'])
def adopt_pet(pet_id):
    data = request.json
    pet = validate_pet_exists(pet_id)

    if pet['adopted']:
        abort(409)
    else:
        db.pets.update_one(
            { '_id': pet['_id'] },
            { '$set': { 'adopted': True }}
        )

    db.adoptions.insert_one(data)
    return json_response({ 'message': 'The item was created successfully' }, 201)

# === HANDLERS === #

@api.errorhandler(400)
def not_found(error):
    return json_response({'error': 'Bad Request'}, 400)

@api.errorhandler(404)
def not_found(error):
    return json_response({'error': 'Not Found'}, 404)

@api.errorhandler(409)
def internal_error(error):
    return json_response({'error': 'Conflict: Pet already adopted'}, 409)

@api.errorhandler(500)
def internal_error(error):
    return json_response({'error': 'Internal Server Error'}, 500)

@api.errorhandler(501)
def not_implemented(error):
    return json_response({'error': 'Not Implemented'}, 501)

def validate_pet_exists(_id):
    res = db.pets.find_one({
        '_id': validate_object_id(_id)
    })
    return res or abort(404)

# === === === === #

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0')
