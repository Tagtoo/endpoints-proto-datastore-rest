import unittest
import webtest
from google.appengine.ext import testbed
import json
import random
import base64
import re
from endpoints_proto_datastore_rest import EndpointRestBuilder
from endpoints_proto_datastore.ndb import EndpointsModel


class RestApiTest(unittest.TestCase):
    def setUp(self):
        tb = testbed.Testbed()
        tb.setup_env(current_version_id='testbed.version') #needed because endpoints expects a . in this value
        tb.activate()
        tb.init_all_stubs()
        self.testbed = tb


    def testEndpointRest(self):
        from google.appengine.ext import ndb
        import endpoints

        class Test(EndpointsModel):
            _message_fields_schema = ('id', 'a', 'b')
            a = ndb.IntegerProperty()
            b = ndb.TextProperty()



        builder = EndpointRestBuilder(Test)
        api = builder.build(api_name='api', name="test", version="v1", description="test")

        app = endpoints.api_server([api], restricted=False)
        testapp = webtest.TestApp(app)

        msg = {}
        resp = testapp.post_json('/_ah/spi/api.list', msg).json
        self.assertEqual(resp, {})

        obj = Test(id=1, a=2, b="3")
        obj.put()

        resp = testapp.post_json('/_ah/spi/api.list', msg).json
        self.assertEqual(resp, {'items':[{'a': '2', 'b': '3', 'id': '1'}]})

        resp = testapp.post_json('/_ah/spi/api.get', {
            "id": 1
        }).json
        self.assertEqual(resp, {'a': '2', 'b': '3', 'id': '1'})

        resp = testapp.post_json('/_ah/spi/api.insert', {
            "id": 3,
            "a": 4
        }).json
        self.assertEqual(resp.get('a'), '4')

        resp = testapp.post_json('/_ah/spi/api.update', {
            "id": 3,
            "a": 5
        }).json
        self.assertEqual(resp.get('a'), '5')

        resp = testapp.post_json('/_ah/spi/api.list', {}).json
        self.assertEqual(resp, {u'items': [{u'a': u'2', u'b': u'3', u'id': u'1'}, {u'a': u'5', u'id': u'3'}]})

        resp = testapp.post_json('/_ah/spi/api.delete', {
            "id": 3
        }).json
        self.assertEqual(resp, {u'a': u'5', u'id': u'3'})

    def tearDown(self):
        self.testbed.deactivate()
