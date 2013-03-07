#!/usr/bin/env python

from urlparse import urlparse
from bson.json_util import dumps, loads
from base import LazyBaseTestCase, ENTITY
#from nose.tools import set_trace; set_trace()

ROOT = '/' + ENTITY + '/'

dummy1 = dict(title="title1", text="text1")
dummy2 = dict(title="title2", text="text2")
dummy3 = dict(title="title3", text="text3")
dummy4 = dict(title="title4", text="text4")

class GetRestTestCase(LazyBaseTestCase):

    def test_get_uncreated_collection_returns_empty_entity_list(self):
        
        rv = self.client.get(ROOT)
        
        d = loads(rv.data)
        l = d[ENTITY]
        self.assertEquals(len(l), 0)
        
    def test_get_collection(self):
        self.post_data(dummy1)
        self.post_data(dummy2)
        self.post_data(dummy3)

        rv = self.client.get(ROOT)
        d = loads(rv.data)
        l = d[ENTITY]
        self.assertEquals(len(l), 3)

        o0 = urlparse(l[0])
        o1 = urlparse(l[1])
        o2 = urlparse(l[2])
        self.assertEquals(o0.scheme, o1.scheme, o2.scheme)
        self.assertEquals(o0.netloc, o1.netloc, o2.netloc)
        self.assertEquals(o0.params, o1.params, o2.params)
        self.assertEquals(o0.query, o1.query, o2.query)
        self.assertNotEquals(o0.path, o1.path, o2.path)

    def test_get_resource(self):
        self.post_data(dummy1)
        doc, path = self.get_first_doc()
        rv = self.client.get(path)
        doc = loads(rv.data)
        del doc['_id']
        del doc['created_at']
        del doc['updated_at']
        self.assertEquals(dummy1, doc)

class PostRestTestCase(LazyBaseTestCase):
    
    def test_post_thing(self):
        rv = self.client.post(ROOT, data=dumps(dummy1))
        self.assertEquals(rv.status_code, 201)
        
    def test_post_resource_fails(self):
        rv = self.client.post('/' + ENTITY + '/0000000001', data=dumps(dummy1))
        self.assertEquals(rv.status_code, 405)
        
    def test_post_collection(self):
        d = {ENTITY: [dummy1, dummy2, dummy3]}
        rv = self.client.post(ROOT, data=dumps(d))
        self.assertEquals(rv.status_code, 200)

        # should return a list of urls
        d = loads(rv.data)
        self.assertEquals(type(d), type(list()))

class PatchRestTestCase(LazyBaseTestCase):

    def test_patch_unsaved_thing_fails(self):
        rv = self.client.patch(ROOT, data=dumps(dummy1))
        self.assertEquals(rv.status_code, 405)

    def test_patch_collection_containing_unsaved_thing_fails(self):
        def postAndGet(d):
            path = self.post_data(d)
            rv = self.client.get(path)
            return loads(rv.data), path
        
        # don't save all objects first
        d = {ENTITY: [postAndGet(dummy1), dummy2, dummy3]}
        
        # patch docs
        rv = self.client.patch(ROOT, data=dumps(d))
        self.assertEquals(rv.status_code, 405)
        
    def test_update_resource(self):
        def postAndGet(d):
            path = self.post_data(d)
            rv = self.client.get(path)
            return loads(rv.data), path

        doc, path = postAndGet(dummy1)
        doc['title'] = 'new title'
        rv = self.client.patch(path, data=dumps(doc))
        self.assertEquals(rv.status_code, 200)
        
    def test_update_collection(self):
        def postAndGet(d):
            path = self.post_data(d)
            rv = self.client.get(path)
            return loads(rv.data)
        
        d = {ENTITY: [postAndGet(dummy1), postAndGet(dummy2), postAndGet(dummy3)]}
        
        # put docs
        rv = self.client.put(ROOT, data=dumps(d))
        self.assertEquals(rv.status_code, 200)        
        self.assertEquals(self.count_data(), 3)


class PutRestTestCase(LazyBaseTestCase):

    def test_put_unsaved_thing_fails(self):
        rv = self.client.put(ROOT, data=dumps(dummy1))
        self.assertEquals(rv.status_code, 405)

    def test_put_collection_containing_unsaved_thing_fails(self):
        def postAndGet(d):
            path = self.post_data(d)
            rv = self.client.get(path)
            return loads(rv.data), path

        # don't save all objects first
        d = {ENTITY: [postAndGet(dummy1), dummy2, dummy3]}

        # put docs
        rv = self.client.put(ROOT, data=dumps(d))
        self.assertEquals(rv.status_code, 405)

    def test_update_resource(self):
        def postAndGet(d):
            path = self.post_data(d)
            rv = self.client.get(path)
            return loads(rv.data), path

        doc, path = postAndGet(dummy1)
        doc['title'] = 'new title'
        rv = self.client.put(path, data=dumps(doc))
        self.assertEquals(rv.status_code, 200)

    def test_update_collection(self):
        def postAndGet(d):
            path = self.post_data(d)
            rv = self.client.get(path)
            return loads(rv.data)

        d = {ENTITY: [postAndGet(dummy1), postAndGet(dummy2), postAndGet(dummy3)]}

        # put docs
        rv = self.client.put(ROOT, data=dumps(d))
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(self.count_data(), 3)


class DeleteRestTestCase(LazyBaseTestCase):
    
    def test_delete_resource(self):
        self.post_data(dummy1)
        self.post_data(dummy2)
        self.post_data(dummy3)
        doc, path = self.get_first_doc()

        rv = self.client.delete(path)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(self.count_data(), 2)

    def test_delete_collection(self):
        self.post_data(dummy1)
        self.post_data(dummy2)
        self.post_data(dummy3)
        
        rv = self.client.delete(ROOT)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(self.count_data(),0)

