import json
import os
import unittest
import tempfile
from datetime import datetime
from dateutil.parser import parse
import userapiserver
from userapiserver.userapiserver import setup_database

TYPE_APPLICATION_JSON = {'content-type': 'application/json'}
FIRST_USER_PAYLOAD = '{"username":"foo",  "password":"bar"}'

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_file = tempfile.mkstemp()
        userapiserver.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_file
        setup_database(userapiserver.app)
        self.app = userapiserver.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_file)

    def createFirstUser(self):
        # Create User
        rv = self.app.post('/users/register', data=FIRST_USER_PAYLOAD, headers={'content-type': 'application/json'})
        assert rv.status_code == 201

    def test_create(self):
        # Bad Request
        rv = self.app.post('/users/register')
        assert rv.status_code == 400
        self.createFirstUser()
        # Conflict
        rv = self.app.post('/users/register', data=FIRST_USER_PAYLOAD, headers={'content-type': 'application/json'})
        assert rv.status_code == 409


    def test_login(self):
        self.createFirstUser()
        # OK
        rv = self.app.post('/auth', data=FIRST_USER_PAYLOAD, headers=TYPE_APPLICATION_JSON)
        assert rv.status_code == 200
        # Unauthorized
        rv = self.app.post('/auth', data='{"username":"foo",  "password":"foo"}', headers=TYPE_APPLICATION_JSON)
        assert rv.status_code == 401
        rv = self.app.post('/auth', headers=TYPE_APPLICATION_JSON)
        assert rv.status_code == 400

    def test_get_requests(self):
        self.createFirstUser()
        rv = self.app.post('/auth', data=FIRST_USER_PAYLOAD, headers=TYPE_APPLICATION_JSON)
        assert rv.status_code == 200
        jsondata = json.loads(rv.data)
        assert jsondata.has_key('access_token')
        access_token = jsondata['access_token']
        authorization_header={'Authorization':'JWT ' + access_token }
        rv = self.app.get('/users/requests', headers=authorization_header)
        assert rv.status_code == 200
        jsondata = json.loads(rv.data)
        assert jsondata.has_key('last_five')
        assert len(jsondata['last_five']) == 1
        request = jsondata['last_five'][0]
        assert request['request_id'] == 1
        assert request['user_id'] == 1
        request_date=parse(request['access_date'])
        assert request_date.date() == datetime.now().date()

if __name__ == '__main__':
    unittest.main()