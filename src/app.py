import os
from pymongo import MongoClient
from flask import Flask, request, abort

from utils import (
    Toggler, SUPPORTED_FIELDS,
    json_response, validate_pet_exists
)

api = Flask(__name__)
toggler = Toggler()

MONGO_HOST = os.environ.get('MONGO_HOST') or 'localhost'
MONGO_DB = toggler.check_flag('swap-database') # values: development/staging

db = MongoClient(MONGO_HOST, 27017)[MONGO_DB]


# === ROUTES === #

@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    abort(404)

@api.route('/health', methods=['GET'])
def health():
    if toggler.check_flag('enhanced-health-check'): # values: True/False
        # TODO: cleanup and create test for behaviour

        statinfo = os.stat('./src/app.py')
        return json_response(
            {'status': 'ok', 'statinfo': statinfo}, 200
        )
    else:
        # Simple health check
        return json_response({'status': 'ok'}, 200)

@api.route('/pets', methods=['GET'])
def pets_list():
    """
    Will list all pets and information about them.
    Will accept query parameters if they are supported
    See utils.SUPPORTED_PARAMETERS for more information.
    """
    query = {}
    args = request.args or {}

    if toggler.check_flag('beta-user'):
        # only offer filtering feature to beta users
        for key in args:
            if key not in SUPPORTED_FIELDS: abort(400)
            query[key] = args[key]

    data = list(db.pets.find(query)) or abort(404)
    return json_response({ 'data': data })

@api.route('/pets/<pet_id>', methods=['GET'])
def find_pet(pet_id):
    """
    Will fetch information on a specific pet.
    Expects a valid `pet_id` from the path.
    Will return 404 if `pet_id` is valid but not
    in the database.
    """
    pet = validate_pet_exists(db, pet_id)
    return json_response({'data': pet })

@api.route('/pets/<pet_id>/adopt', methods=['POST'])
def adopt_pet(pet_id):
    """
    Allows for the adoption of pets if they exist
    and are available for adoption.
    Expects a json paylod: {
        'name': 'string',
        'address': 'string'
    }

    as well as a valid `pet_id` from the path.
    """
    data = request.json
    pet = validate_pet_exists(db, pet_id)

    if pet['adopted']:
        abort(409)
    else:
        db.pets.update_one(
            { '_id': pet['_id'] },
            { '$set': { 'adopted': True }}
        )
    if toggler.check_flag('decouple-database'):
        # Pretend this was added to a queue like SQS or rabbitMQ to decouple
        # This would hypothetically reduce the burden on the database
        pass
    else:
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

# === === === === #

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0')
