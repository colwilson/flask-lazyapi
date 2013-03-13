#!/usr/bin/env python

import flask_lazyapi as lazy
from flask import Flask
import unittest
import datetime
from urlparse import urlparse
from pymongo import MongoClient
from bson.json_util import dumps, loads

ENTITY = 'things'
DB = ENTITY + 'db'

class Things(lazy.API): pass

ROOT = '/' + ENTITY + '/'

dummy1a = dict(title="title1", text="texta")
dummy2b = dict(title="title2", text="textb")
dummy3c = dict(title="title3", text="textc")
dummy4d = dict(title="title4", text="textd")
dummy1x = dict(title="title1", text="textx")
dummy2x = dict(title="title2", text="textx")
dummy3x = dict(title="title3", text="textx")
dummy4x = dict(title="title4", text="textx")

class QueryTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        Things.register(app)
        
        self.client = app.test_client()
        self.connection = MongoClient()
        self.db = self.connection[DB]
        self.collection = self.db[ENTITY]
        self.collection.remove()

        self.post_data(dummy1a)
        self.post_data(dummy2b)
        self.post_data(dummy3c)
        self.post_data(dummy4d)
        self.post_data(dummy1x)
        self.post_data(dummy2x)
        self.post_data(dummy3x)
        self.post_data(dummy4x)
        #print app.url_map
        
    def tearDown(self):
        self.connection.drop_database(DB)

    def post_data(self, o):
        rv = self.client.post('/' + ENTITY + '/', data=dumps(o))
        return urlparse(rv.data).path

    def find_test(self):
        query = dict(text='textx')
        rv = self.client.get(ROOT, data=dumps(query))
        d = loads(rv.data)
        l = d[ENTITY]
        self.assertEquals(len(l), 4)
        
    def find_by_time_test(self):
        d = datetime.datetime.now() 
        query = dict(created_at={"$lt": d})
        rv = self.client.get(ROOT, data=dumps(query))
        d = loads(rv.data)
        l = d[ENTITY]
        self.assertEquals(len(l), 8)

    def find_and_test(self):
        query = dict(title="title3", text='textx')
        
        rv = self.client.get(ROOT, data=dumps(query))
        d = loads(rv.data)
        l = d[ENTITY]
        self.assertEquals(len(l), 1)
        
    def find_or_test(self):
        query = {'title': 'title1', '$or': [ {'text': 'texta'}, {'text': 'textx'} ]}
        rv = self.client.get(ROOT, data=dumps(query))
        d = loads(rv.data)
        l = d[ENTITY]
        self.assertEquals(len(l), 2)
        
        