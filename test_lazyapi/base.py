#!/usr/bin/env python

import flask_lazyapi as lazy
from flask import Flask
import unittest
from urlparse import urlparse
from pymongo import MongoClient
from bson.json_util import dumps, loads

ENTITY = 'things'
DB = ENTITY + 'db'

class Things(lazy.API): pass

class LazyBaseTestCase(unittest.TestCase):

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

    def get_first_doc(self):
        rv = self.client.get('/' + ENTITY + '/')
        d = loads(rv.data)
        l = d[ENTITY]
        
        # get the first document
        url = urlparse(l[0])
        path = url.path
        rv = self.client.get(path)
        doc = loads(rv.data)
        return doc, path

    def post_data(self, o):
        rv = self.client.post('/' + ENTITY + '/', data=dumps(o))
        return urlparse(rv.data).path

    def count_data(self):
        rv = self.client.get('/' + ENTITY + '/')
        d = loads(rv.data)
        return len(d[ENTITY])
    
    