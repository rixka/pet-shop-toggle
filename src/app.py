from flask import Flask, request, abort

from utils import (
    json_response, validate_object_id,
    parse_query, check_not_empty
)

api = Flask(__name__)

@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    abort(404)

@api.route('/health', methods=['GET'])
def health():
    return json_response({'status': 'ok'}, 200)



# === HANDLERS === #

@api.errorhandler(400)
def not_found(error):
    return json_response({'error': 'Bad Request'}, 400)

@api.errorhandler(404)
def not_found(error):
    return json_response({'error': 'Not Found'}, 404)

@api.errorhandler(500)
def internal_error(error):
    return json_response({'error': 'Internal Server Error'}, 500)

@api.errorhandler(501)
def not_implemented(error):
    return json_response({'error': 'Not Implemented'}, 501)

# === === === === #

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0')
