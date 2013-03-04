#!/usr/bin/env python

import flask_lazyapi as lazy
from flask import Flask, Blueprint
import unittest
from pymongo import MongoClient
from bson.json_util import dumps


class Alphas(lazy.API): pass

class Betas(lazy.API):
    db = "TestBetasDB"
    
class Gammas(lazy.API):
    pass
    # bp registered as version = "v1.0"


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
        
        bp = Blueprint("v1.0", __name__)
        Gammas.register(bp)
        app.register_blueprint(bp, url_prefix="/v1.0")
        
        self.app = app.test_client()

        self.connection = MongoClient()
        #print app.url_map

    def test_auto_db_name(self):
        entity = 'alphas'
        dbname = entity + 'db'
        home = '/%s/' % entity

        self.do_check_collection_naming(entity, dbname, home)

    def test_specified_db_name(self):
        entity = 'betas'
        dbname = 'TestBetasDB'
        home = '/%s/' % entity
        
        self.do_check_collection_naming(entity, dbname, home)

    def test_versioned_auto_db_name(self):
        entity = 'gammas'
        dbname = entity + 'db'
        home = '/v1.0/%s/' % entity
        
        self.do_check_collection_naming(entity, dbname, home)
        
    def do_check_collection_naming(self, entity, dbname, home):

        self.db = self.connection[dbname]
        self.collection = self.db[entity]
        self.connection.drop_database(dbname)

        d = {entity: [dummy1, dummy2, dummy3, dummy4]}

        # put docs
        rv = self.app.post(home, data=dumps(d))
        self.assertEquals(rv.status_code, 200)
        
        # count docs
        c = self.collection.count()
        self.assertEquals(c, 4)
        self.connection.drop_database(dbname)

