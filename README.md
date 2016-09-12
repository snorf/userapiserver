UserApiServer
=============

This is a HTTP-based API server using persistent storage that can be consumed by using curl or similar.
The server has 3 resources:
* /users/register - register a user
* /auth - get JWT token
* /users/requests - see last 5 successful login attempts

Comments
-------

This was implemented quite fast in Python so of course there are some obvious limitations:
* There's a self signed HTTPS certificate (hence the "-k" switch for curl below), of course this is
  not ideal but since I'm guessing no one would put it in production it's fine. At least it's encrypted.

* I'm not the best Python hacker which probably shows in the structure of the project, I tried to follow
  guidelines about it but as always on the Internet there's many "best" ways to do it.

* 3:rd party libraries, since I didn't want to reinvent that many wheels I tried using flask and sqlalchemy
  which I've never used nor seen before. It saved me a lot of time but I didn't write any pure SQL statements or
  home made password hashing algorithms.

* A user can register once and never change his/her password nor can he/she unregister.

* The database doesn't have any cleanup functionality so eventually sqlite or the harddrive will say no.

Installation
------------
Install dependencies
```
pip install -r requirements.txt
```

Or install package
```
python setup.py install
```

Usage
-------

Start server
```
python runserver.py
```

Register a user
```
curl -k -H "Content-Type: application/json" \
            -d '{"username":"foo",  "password":"bar"}' \
            https://127.0.0.1:8443/users/register
```
Response should look like:
```
...
< HTTP/1.0 201 CREATED
...
"Created"
```

Login
```
curl -k -H "Content-Type: application/json" \
            -d '{"username":"foo",  "password":"bar"}' \
            https://127.0.0.1:8443/auth
```

Response should be:
```
...
< HTTP/1.0 200 OK
< Content-Type: application/json
...
{
  "access_token": "eyJhbGciOiJIUzI1NicCI6IkpXVCJ9.eyJpZGVu...Q3MzYxNzAxOH0.MaL7UTUWruBAXlXkRGMcEODSKRLclqka2ZXYOCp9nTk"
}
```

To avoid having to copy/paste the access token do this (assuming JQ is installed):
```
TOKEN=`curl -s -k -H "Content-Type: application/json" \
                   -d '{"username":"foo",  "password":"bar"}' \
                   https://127.0.0.1:8443/auth | jq -r .access_token`
```
Then in the next call replace the token with $TOKEN.

Retreive last 5 login attempts
```
curl -k -H "Authorization: JWT \
            $TOKEN" \
            https://127.0.0.1:8443/users/requests
```

Response should look something like this:
```
{
  "last_five": [
    {
      "access_date": "Sun, 11 Sep 2016 19:35:22 GMT",
      "request_id": 18,
      "user_id": 1
    },
    {
      "access_date": "Sun, 11 Sep 2016 19:35:14 GMT",
      "request_id": 17,
      "user_id": 1
    },
    {
      "access_date": "Sun, 11 Sep 2016 19:34:57 GMT",
      "request_id": 16,
      "user_id": 1
    },
    {
      "access_date": "Sun, 11 Sep 2016 19:34:27 GMT",
      "request_id": 15,
      "user_id": 1
    },
    {
      "access_date": "Sun, 11 Sep 2016 19:33:28 GMT",
      "request_id": 14,
      "user_id": 1
    }
  ]
}

```

Run Unit tests

```
python userapiserver_tests.py
```

Should look like this:
```
...
----------------------------------------------------------------------
Ran 3 tests in 2.590s

OK
```