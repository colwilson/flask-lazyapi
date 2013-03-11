#!/usr/bin/env python

import flask_lazyapi as lazy
from flask import Flask, url_for
import unittest
from pymongo import MongoClient
from bson.json_util import dumps, loads
from urlparse import urlparse
from bson.json_util import dumps, loads
from base import LazyBaseTestCase, ENTITY
#from nose.tools import set_trace; set_trace()

ENTITY = 'things'
ROOT = '/' + ENTITY + '/'

dummy1 = dict(title="a", text="d")
dummy2 = dict(title="b", text="c")
dummy3 = dict(title="c", text="b")
dummy4 = dict(title="d", text="a")

DB = ENTITY + 'db'

class Things(lazy.API):

    def sorted(self, sort_by, direction):
        docs = self.collection.find().sort(sort_by, dict(asc=1,desc=-1)[direction])
        urls = [ self._resource_url(doc['_id']) for doc in docs ]
        return (dumps({self.get_route_base(): urls}), 200, None)
    

class RestExtensionsTestCase(unittest.TestCase):
    
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        Things.register(app)
        
        self.client = app.test_client()
        self.connection = MongoClient()
        self.db = self.connection[DB]
        self.collection = self.db[ENTITY]
        self.collection.remove()
        print app.url_map
        
    def tearDown(self):
        self.connection.drop_database(DB)

    def post_data(self, o):
        rv = self.client.post('/' + ENTITY + '/', data=dumps(o))
        return urlparse(rv.data).path

    def test_sort_asc(self):
        self.post_data(dummy1)
        self.post_data(dummy2)
        self.post_data(dummy3)
        self.post_data(dummy4)
        rv = self.client.get(ROOT + 'sorted/text/asc')
        d = loads(rv.data)
        l = d[ENTITY]

        texts = []
        for url in l:
            rv = self.client.get(url)
            print url, rv.data
            doc = loads(rv.data)
            texts.append(doc['text'])

        self.assertEquals(texts, ['a', 'b', 'c', 'd'])


    def test_sort_desc(self):
        self.post_data(dummy1)
        self.post_data(dummy3)
        self.post_data(dummy4)
        self.post_data(dummy2)
        rv = self.client.get(ROOT + 'sorted/text/desc')
        d = loads(rv.data)
        l = d[ENTITY]

        texts = []
        for url in l:
            rv = self.client.get(url)
            print url, rv.data
            doc = loads(rv.data)
            texts.append(doc['text'])

        self.assertEquals(texts, ['d', 'c', 'b', 'a'])



