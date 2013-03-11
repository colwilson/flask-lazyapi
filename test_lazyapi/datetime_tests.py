#!/usr/bin/env python

import flask_lazyapi as lazy
from bson.json_util import dumps
from base import LazyBaseTestCase, ENTITY
import time

ROOT = '/' + ENTITY + '/'

class Alphas(lazy.API): pass

dummy = dict(title="title", text="text")

class ConfigTestCase(LazyBaseTestCase):

    def test_insert_creates_datetimes(self):
        self.client.post(ROOT, data=dumps(dummy))
        doc, path = self.get_first_doc()
        self.assertIn('created_at', doc)
        self.assertIn('updated_at', doc)
        
    def test_update_updates_updated_at(self):
        rv = self.client.post(ROOT, data=dumps(dummy))
        self.assertEquals(rv.status_code, 201)
        
        doc, path = self.get_first_doc()
        self.assertEquals(doc['created_at'], doc['updated_at'])

        time.sleep(0.1)

        self.client.put(path, data=dumps(doc))
        doc, path = self.get_first_doc()
        self.assertNotEquals(doc['created_at'], doc['updated_at'])
        