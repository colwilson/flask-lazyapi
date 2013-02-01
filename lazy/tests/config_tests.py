#!/usr/bin/env python

import lazy
from flask import Flask
import unittest
from urlparse import urlparse
from pymongo import MongoClient
from bson.json_util import dumps, loads, ObjectId


class Alphas(lazy.API): pass

class Betas(lazy.API):
    db = "TestBetasDB"


class ConfigTestCase(unittest.TestCase):

    dummy1 = dict(title="title1", text="text1")
    dummy2 = dict(title="title2", text="text2")
    dummy3 = dict(title="title3", text="text3")
    dummy4 = dict(title="title4", text="text4")
    
    
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        Alphas.register(app)
        Betas.register(app)
        self.app = app.test_client()
        #print app.url_map        
        
    def test_auto_db_name(self):
        entity = 'alphas'
        dbname = entity + 'db'

        self.do_check_collection_naming(entity, dbname)
            
    def test_specified_db_name(self):
        entity = 'betas'
        dbname = 'TestBetasDB'
            
        self.do_check_collection_naming(entity, dbname)
            
    def do_check_collection_naming(self, entity, dbname):
        home = '/%s/' % entity
        
        d = {entity: [self.dummy1, self.dummy2, self.dummy3, self.dummy4]}

        # put docs
        rv = self.app.put(home, data=dumps(d))

        # count docs
        connection = MongoClient()
        db = connection[dbname]
        collection = db[entity]
        c = collection.count()
        
        assert(c == 4)
        collection.remove()
        connection.drop_database(dbname)
        


        

if __name__ == '__main__':
    unittest.main()