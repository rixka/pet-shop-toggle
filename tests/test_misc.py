from app import api
from utils import JSON_MIME_TYPE, Toggler

from jsonschema import validate

SCHEMA = {
        'type': 'object',
        'properties': {
          'status': { 'type': 'string' },
          'statinfo': { 'type': 'array' },
        },
        'required': [ 'status', 'statinfo' ]
    }

def test_simple_health(mocker):
    mocker.patch.object(Toggler, 'check_flag', return_value=False)
    res = api.test_client().get('/health')

    assert res.status_code == 200
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'status': 'ok' }

def test_enhanced_health(mocker):
    mocker.patch.object(Toggler, 'check_flag', return_value=True)
    res = api.test_client().get('/health')

    assert res.status_code == 200
    assert res.mimetype == JSON_MIME_TYPE
    assert validate(res.json, SCHEMA) is None

def test_not_found():
    res = api.test_client().get('/')

    assert res.status_code == 404
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Not Found' }
