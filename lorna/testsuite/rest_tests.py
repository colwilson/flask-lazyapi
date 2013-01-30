#!/usr/bin/env python

import lorna
from flask import Flask
import unittest
from urlparse import urlparse
from pymongo import MongoClient
from bson.json_util import dumps, loads, ObjectId

ENTITY = 'tests'
HOME = '/' + ENTITY + '/'
DB = ENTITY + 'db'

class TestsView(lorna.LornaView): pass

class LornaTestCase(unittest.TestCase):

    dummy1 = dict(title="title1", text="text1")
    dummy2 = dict(title="title2", text="text2")
    dummy3 = dict(title="title3", text="text3")
    dummy4 = dict(title="title4", text="text4")
    
    
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        TestsView.register(app)
        self.app = app.test_client()
        #print app.url_map
        
        self.connection = MongoClient()
        self.db = self.connection[DB]
        self.collection = self.db[ENTITY]
        self.collection.remove()

        self.collection.insert(self.dummy1)
        self.collection.insert(self.dummy2)
        self.collection.insert(self.dummy3)
        
    def tearDown(self):
        self.collection.remove()
        
    def do_get_first_doc(self):
        rv = self.app.get(HOME)
        d = loads(rv.data)
        l = d[ENTITY]

        # get the first document
        url0 = urlparse(l[0])
        rv = self.app.get(url0.path)
        doc0 = loads(rv.data)
        return rv, doc0, url0

    def test_get_collection(self):
        rv = self.app.get(HOME)
        d = loads(rv.data)
        l = d[ENTITY]
        assert(len(l) == 3)

        o0 = urlparse(l[0])
        o1 = urlparse(l[1])
        o2 = urlparse(l[2])
        assert(o0.scheme == o1.scheme == o2.scheme)
        assert(o0.netloc == o1.netloc == o2.netloc)
        assert(o0.params == o1.params == o2.params)
        assert(o0.query == o1.query == o2.query)
        assert(o0.path != o1.path != o2.path)
        
    def test_get_resource(self):
        rv0, doc0, url = self.do_get_first_doc()
        
        rv = self.app.get(url.path)
        doc = loads(rv.data)
        assert(self.dummy1 == doc)

    def test_post_collection(self):
        rv = self.app.post(HOME, data=dumps(self.dummy4))
        d = loads(rv.data)
        del d['_id']
        assert(self.dummy4 == d)
        
    def test_post_resource(self):
        rv0, doc0, url = self.do_get_first_doc()
        
        rv = self.app.post(url.path, data=dumps(self.dummy4))
        assert(rv.status_code == 405)

    def test_delete_resource(self):
        rv = self.app.get(HOME)
        d = loads(rv.data)
        l = d[ENTITY]
        
        o0 = urlparse(l[0])
        rv = self.app.delete(o0.path)
        
        rv = self.app.get(HOME)
        d = loads(rv.data)
        l = d[ENTITY]
        assert(len(l) == 2)
        
    def test_delete_collection(self):
        rv = self.app.delete(HOME)
        assert(rv.status_code == 200)
        
        rv = self.app.get(HOME)
        d = loads(rv.data)
        l = d[ENTITY]
        assert(len(l) == 0)
        
    def test_put_resource_results_match(self):

        rv, doc, url = self.do_get_first_doc()

        # alter the doc
        doc['title'] = 'changed title'
        doc['text'] = 'changed text'
        
        # save the modified doc
        rv = self.app.put(url.path, data=dumps(doc))
            
        # check the result is identical
        d = loads(rv.data)
        assert(d == doc)

    def test_put_resource_inserted_ok(self):
    
        rv, doc, url = self.do_get_first_doc()

        # alter the doc
        doc['title'] = 'changed title'
        doc['text'] = 'changed text'

        # save the modified doc
        rv = self.app.put(url.path, data=dumps(doc))

        # check there are still three entries
        rv = self.app.get(HOME)
        d = loads(rv.data)
        l = d[ENTITY]
        assert(len(l) == 3)

    def test_put_collection(self):
        d = {ENTITY: [self.dummy1, self.dummy2, self.dummy3, self.dummy4]}

        # put docs
        rv = self.app.put(HOME, data=dumps(d))
        assert(rv.status_code == 201)

        # count docs
        rv = self.app.get(HOME)
        d = loads(rv.data)
        l = d[ENTITY]
        assert(len(l) == 4)    

if __name__ == '__main__':
    unittest.main()