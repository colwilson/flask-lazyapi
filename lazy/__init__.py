#!/usr/bin/env python

from flask import request, url_for, make_response, current_app
from flask.ext.classy import FlaskView, route
from bson.json_util import dumps, loads, ObjectId
from bson.errors import InvalidId
from pymongo.errors import OperationFailure
from pymongo import MongoClient
#from nose.tools import set_trace; set_trace()


class API(FlaskView):

    def _rsrc_url(self, id):
        return request.url_root[:-1] + url_for(request.endpoint) + str(id)

    def collection(self):
        connection = MongoClient()
        try:
            db = connection[self.db]
        except:
            db = connection[self.get_route_base()+'db']
            
        collection = db[self.get_route_base()]
        return collection   
    
    def index(self):
        docs = self.collection().find()
        urls = [ self._rsrc_url(doc['_id']) for doc in docs ]
        return (dumps({self.get_route_base(): urls}), 200, None)

            
    def get(self, id):
        try:
            doc = self.collection().find_one(ObjectId(id))
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
            doc = loads(payload)
            # TODO check for duplicates? return 409?
            # wikipedia just says "The PUT and DELETE methods are idempotent methods."
            id = self.collection().insert(doc)
            if id:
                return (dumps(doc), 201, {'Content-Location': self._rsrc_url(id)})
            else:
                return ('data was not inserted', 400, None)
        except Exception, e:
            return (str(e), 400, None)

    @route('/<id>', methods=['POST'])
    def post_id(self, id):
        return ('Not implmented', 405, None)
            
    def delete(self):
        try:
            doc = self.collection().remove()
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
            doc = self.collection().remove(ObjectId(id))
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
            obj = loads(payload)
            assert(type(obj) == type(dict()))
            assert(self.get_route_base() in obj)
            docs = obj[self.get_route_base()]

            #empty the collection
            self.collection().remove()

            # add new docs
            ids = self.collection().insert(docs)
            if len(ids):
                return ('collection replace ok', 200, {'Content-Location': request.url})
            else:
                return ('data was not updated', 400, None)
        except Exception, e:      
            return (str(e), 400, None)
            
    @route('/<id>', methods=['PUT'])
    def put_id(self, id):
        payload = request.data
        
        try:
            assert(isinstance(payload, basestring))
            doc = loads(payload)
            assert('_id' in doc)
            assert(str(doc['_id']) == id)
            doc['_id'] == id
            
            id0 = self.collection().save(doc)
            
            if id0:
                if (id0 == ObjectId(id)):
                    return (dumps(doc), 200, {'Content-Location': request.url})
                else:
                    return ('ids do not match', 405, None)
            else:
                return ('data was not updated', 500, None)
        except Exception, e:
            return (str(e), 500, None)



