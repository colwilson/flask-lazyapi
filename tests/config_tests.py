7#!/usr/bin/env python

import flask_lazyapi as lazy
from flask import Flask, Blueprint
import unittest
from pymongo import MongoClient
from bson.json_util import dumps
#from nose.tools import set_trace; set_trace()


class Alphas(lazy.API): pass

class Betas(lazy.API):
    db = "TestBetasDB"
    
class Gammas(lazy.API):
    version = "v1.0"

class Deltas(lazy.API):
    collection = "dees"


dummy1 = dict(title="title1", text="text1")
dummy2 = dict(title="title2", text="text2")
dummy3 = dict(title="title3", text="text3")
dummy4 = dict(title="title4", text="text4")


class ConfigTestCase(unittest.TestCase):


    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        Alphas.register(app)
        Betas.register(app)      
        Gammas.register(app)
        Deltas.register(app)
        
        self.client = app.test_client()
        self.connection = MongoClient()

    def test_auto_db_name(self):
        collection = 'alphas'
        dbname = collection + 'db'
        home = '/%s/' % collection

        self.do_check_collection_naming(collection, dbname, home)

    def test_specified_db_name(self):
        collection = 'betas'
        dbname = 'TestBetasDB'
        home = '/%s/' % collection
        
        self.do_check_collection_naming(collection, dbname, home)

    def test_versioned_auto_db_name(self):
        collection = 'gammas'
        dbname = collection + 'db'
        home = '/v1.0/%s/' % collection
        
        self.do_check_collection_naming(collection, dbname, home)
        
    def test_specified_collection_name(self):
        collection = 'dees'
        dbname = collection + 'db'
        home = '/%s/' % collection

        self.do_check_collection_naming(collection, dbname, home)

    def do_check_collection_naming(self, collection, dbname, home):

        self.db = self.connection[dbname]
        self.collection = self.db[collection]
        self.connection.drop_database(dbname)

        d = {collection: [dummy1, dummy2, dummy3, dummy4]}

        # put docs
        rv = self.client.post(home, data=dumps(d))
        self.assertEquals(rv.status_code, 200)
        
        # count docs
        c = self.collection.count()
        self.assertEquals(c, 4)
        self.connection.drop_database(dbname)


