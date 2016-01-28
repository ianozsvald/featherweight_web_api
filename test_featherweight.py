import unittest
import json
import featherweight_api


def trivial_fn(x):
    """Example function"""
    return x*2

featherweight_api.register(trivial_fn)


class Test(unittest.TestCase):
    def setUp(self):
        self.app = featherweight_api.app.test_client()

    def test_try_failure_missing_fn(self):
        rv = self.app.get('/nothing')
        assert rv.status_code == 404 # this call cannot succeed

    def test_try_failure(self):
        rv = self.app.get('/trivial_fn')
        assert rv.status_code == 200  # this call must succeed
        data = rv.data.decode('utf8')
        jsn = json.loads(data)
        assert jsn['success'] == False, "We expect this call failed as it missed an argument"

    def test_try_failure_bad_arg(self):
        rv = self.app.get('/trivial_fn?nothing=1')
        assert rv.status_code == 200  # this call must succeed
        data = rv.data.decode('utf8')
        jsn = json.loads(data)
        assert jsn['success'] == False, "We expect this call failed as it has the wrong argument"

    def test_try_success(self):
        rv = self.app.get('/trivial_fn?x=10')
        assert rv.status_code == 200  # this call must succeed
        data = rv.data.decode('utf8')
        jsn = json.loads(data)
        assert jsn['success'] == True
        assert jsn['result'] == 20.0


    def test_try_success_POST(self):
        # POST some JSON data (encoded as a string)
        data = json.dumps({'x': 11})
        rv = self.app.post('/trivial_fn', data=data, headers={'Content-Type': 'application/json'})
        assert rv.status_code == 200  # this call must succeed
        data = rv.data.decode('utf8')
        jsn = json.loads(data)
        assert jsn['success'] == True
        assert jsn['result'] == 22.0
