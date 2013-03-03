#!/usr/bin/env python

import lazy
from bson.json_util import dumps
from base import LazyBaseTestCase, ENTITY
import time

ROOT = '/' + ENTITY + '/'

class Alphas(lazy.API): pass

    
class ConfigTestCase(LazyBaseTestCase):

    def test_insert_creates_datetimes(self):
        self.app.post(ROOT, data=dumps(self.dummy))
        doc, path = self.get_first_doc()
        self.assertIn('created_at', doc)
        self.assertIn('updated_at', doc)
        
    def test_update_updates_updated_at(self):
        rv = self.app.post(ROOT, data=dumps(self.dummy))
        self.assertEquals(rv.status_code, 201)
        
        doc, path = self.get_first_doc()
        self.assertEquals(doc['created_at'], doc['updated_at'])

        time.sleep(0.1)

        #from nose.tools import set_trace; set_trace()
        self.app.put(path, data=dumps(doc))
        doc, path = self.get_first_doc()
        self.assertNotEquals(doc['created_at'], doc['updated_at'])
        