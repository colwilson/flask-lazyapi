#!/usr/bin/env python

import datetime
from flask import request, url_for
from flask.ext.classy import FlaskView, route
from bson.json_util import dumps, loads, ObjectId
from bson.errors import InvalidId
from pymongo.errors import OperationFailure
from pymongo import MongoClient

class API(FlaskView):
   
    def _rsrc_url(self, id):
        return request.url_root[:-1] + url_for(request.endpoint) + str(id)

    def _ensure_has_datetimes(self, doc):
        if not 'created_at' in doc:
            doc['created_at'] = datetime.datetime.now()
        if not 'updated_at' in doc:
            doc['updated_at'] = datetime.datetime.now()
        return doc

    @property
    def collection(self):
        connection = MongoClient()
        try:
            db = connection[self.db]
        except:
            db = connection[self.get_route_base()+'db']
            
        collection = db[self.get_route_base()]
        return collection   
    
    def index(self):
        if len(request.data) == 0:
            payload = '{}' # the default
        else:
            payload = request.data
        query = loads(payload)
        docs = self.collection.find(query)
        urls = [ self._rsrc_url(doc['_id']) for doc in docs ]
        return (dumps({self.get_route_base(): urls}), 200, None)
            
    def get(self, id):
        try:
            doc = self.collection.find_one(ObjectId(id))
            assert(doc is not None)
            return (dumps(doc), 200, None)
        except InvalidId, e:
            return (str(e), 406, None)
        except Exception, e:
            return (str(e), 404, None)

    def post(self):           
        payload = request.data
        try:
            assert(isinstance(payload, basestring))
            d = loads(payload)
            assert(isinstance(d, dict))         
            if self.get_route_base() in d:                
                try:
                    assert(self.get_route_base() in d)
                    l = d[self.get_route_base()]
                    assert(isinstance(l, list))
                except:
                    # i.e is it a list of things in a dict? { "things": [] }
                    return ('use the format { "%s": [] }' % self.get_route_base(), 405)
                docs = [self._ensure_has_datetimes(doc) for doc in d[self.get_route_base()]]
                ids = self.collection.insert(docs)
                if isinstance(ids, list):
                    return dumps([self._rsrc_url(id) for id in ids])
                else:
                    return ('data was not inserted', 400, None)
            else:
                doc = self._ensure_has_datetimes(d)
                id = self.collection.insert(doc)
                if id:
                    return (self._rsrc_url(id), 201, {'Content-Location': self._rsrc_url(id)})
                else:
                    return ('data was not inserted', 400, None)
        except Exception, e:
            return (str(e), 400, None)

    @route('/<id>', methods=['POST'])
    def post_id(self, id):
        return ('Not implmented', 405, None)
            
    def delete(self):
        try:
            self.collection.remove()
            return ('deleted', 200, None)
        except InvalidId, e:
            return (str(e), 406, None)
        except OperationFailure, e:
            return (str(e), 404, None)
        except Exception, e:
            return (str(e), 500, None)

    @route('/<id>', methods=['DELETE'])
    def delete_id(self, id):
        try:
            self.collection.remove(ObjectId(id))
            return ('deleted ' + id, 200, None)
        except InvalidId, e:
            return (str(e), 406, None)
        except OperationFailure, e:
            return (str(e), 404, None)
        except Exception, e:
            return (str(e), 500, None)
        
    def put(self):
        payload = request.data        
        try:
            assert(isinstance(payload, basestring))
            d = loads(payload)
            assert(type(d) == type(dict()))
            try:
                assert(self.get_route_base() in d)
                l = d[self.get_route_base()]
                assert(isinstance(l, list))
            except:
                # i.e is it a list of things in a dict? { "things": [] }
                return ('use the format { "%s": [] }' % self.get_route_base(), 405)
            docs = d[self.get_route_base()]
            for doc in docs:
                try:
                    assert('_id' in doc)
                    assert('created_at' in doc)
                    assert('updated_at' in doc)
                except:
                    return ('You are trying to update a record which was not previously stored', 405)
                doc['updated_at'] = datetime.datetime.now()

            #empty the collection
            self.collection.remove()
            
            # add new docs
            ids = self.collection.insert(docs)
            if len(ids):
                return ('collection replace ok', 200, {'Content-Location': request.url})
            else:
                return ('data was not updated', 400, None)
        except Exception, e:
            return (str(e), 400, None)
            
    @route('/<id>', methods=['PATCH', 'PUT'])
    def patch_id(self, id):
        payload = request.data        
        try:
            assert(isinstance(payload, basestring))
            doc = loads(payload)
            assert(type(doc) == type(dict()))
            doc['updated_at'] = datetime.datetime.now()
            
            rid = self.collection.save(doc)
            assert(ObjectId(id) == rid)
            
            if rid:
                return (request.url, 200, {'Content-Location': request.url})
            else:
                return ('data was not updated', 500, None)
        except Exception, e:
            return (str(e), 500, None)



