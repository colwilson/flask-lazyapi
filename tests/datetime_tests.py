#!/usr/bin/env python

import flask_lazyapi as lazy
from bson.json_util import dumps
from base import LazyBaseTestCase, ENTITY
import time
import datetime
import pytz
from nose.tools import * 

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

    def test_naive_ok_now(self):
        rv = self.client.post(ROOT, data=dumps(dummy))
        time.sleep(0.1)
        doc, path = self.get_first_doc()

        self.assertNotEquals(doc['created_at'], datetime.datetime.now().replace(tzinfo=pytz.utc))

    def test_naive_ok_utcnow(self):
        rv = self.client.post(ROOT, data=dumps(dummy))
        time.sleep(0.1)
        doc, path = self.get_first_doc()

        self.assertNotEquals(doc['created_at'], datetime.datetime.utcnow().replace(tzinfo=pytz.utc))

    @raises(TypeError)
    def test_aware_fails_now(self):
        rv = self.client.post(ROOT, data=dumps(dummy))
        time.sleep(0.1)
        doc, path = self.get_first_doc()
        
        doc['created_at'] == datetime.datetime.now()

    @raises(TypeError)
    def test_aware_fails_utcnow(self):
        rv = self.client.post(ROOT, data=dumps(dummy))
        time.sleep(0.1)
        doc, path = self.get_first_doc()
        
        doc['created_at'] == datetime.datetime.utcnow()
