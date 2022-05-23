from app import api
from utils import JSON_MIME_TYPE

def test_health():
    res = api.test_client().get('/health')

    assert res.status_code == 200
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'status': 'ok' }

def test_not_found():
    res = api.test_client().get('/')

    assert res.status_code == 404
    assert res.mimetype == JSON_MIME_TYPE
    assert res.json == { 'error': 'Not Found' }
