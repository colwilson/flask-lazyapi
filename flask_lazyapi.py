#!/usr/bin/env python

import datetime, pytz
from flask import request, url_for, current_app
from flask.ext.classy import FlaskView, route
from bson.json_util import dumps, loads, ObjectId
from bson.errors import InvalidId
from pymongo.errors import OperationFailure
from pymongo import MongoClient

class API(FlaskView):
   
    def _resource_url(self, id):
        get_endpoint = request.endpoint.split(':')[0] + ':get'
        return url_for(get_endpoint, id=id, _external = not current_app.config['TESTING'])

    def _ensure_has_datetimes(self, doc):
        if not 'created_at' in doc:
            doc['created_at'] = rightnow()
        if not 'updated_at' in doc:
            doc['updated_at'] = rightnow()
        return doc


    @classmethod
    def _get_collection_name(cls):
        
        if hasattr(cls, "collection"):
            return cls.collection
        elif hasattr(cls, "route_base"):
            route_base = cls.route_base
        else:
            if cls.__name__.endswith("View"):
                route_base = cls.__name__[:-4].lower()
            else:
                route_base = cls.__name__.lower()
        
        return route_base.strip("/")

        
    @classmethod
    def get_route_base(cls):
        collection_name = cls._get_collection_name()

        if hasattr(cls, "version"):
            return cls.version + "/" + cls._get_collection_name()
        else:
            return cls._get_collection_name()

        
    @property
    def docs(self):
        connection = MongoClient()
        collection_name = self._get_collection_name()
        
        try:
            db = connection[self.db]
        except:
            db = connection[collection_name + "db"]

        return db[collection_name]

    
    def index(self):
        #from nose.tools import set_trace; set_trace()
        q = loads(request.args.get('q', '{}'))
        docs = self.docs.find(q)
        urls = [ self._resource_url(doc['_id']) for doc in docs ]
        return (dumps({self.get_route_base(): urls}), 200, None)
            
    def get(self, id):
        try:
            doc = self.docs.find_one(ObjectId(id))
            assert(doc is not None)
            return (dumps(doc), 200, None)
        except InvalidId, e:
            return (str(e), 406, None)
        except Exception, e:
            return (str(e), 404, None)

    def post(self):           
        payload = request.data
        collection_name = self._get_collection_name()
        try:
            assert(isinstance(payload, basestring))
            d = loads(payload)
            assert(isinstance(d, dict))
            if collection_name in d:
                try:
                    l = d[collection_name]
                    assert(isinstance(l, list))
                except:
                    # i.e is it a list of things in a dict? { "things": [] }
                    return ('use the format { "%s": [] }' % collection_name, 405)
                docs = [self._ensure_has_datetimes(doc) for doc in d[collection_name]]
                ids = self.docs.insert(docs)
                if isinstance(ids, list):
                    return dumps([self._resource_url(id) for id in ids]) # a 200 (not a 201 inserted)
                else:
                    return ('data was not inserted', 400, None)
            else:
                doc = self._ensure_has_datetimes(d)
                id = self.docs.insert(doc)
                if id:
                    return (self._resource_url(id), 201, {'Content-Location': self._resource_url(id)})
                else:
                    return ('data was not inserted', 400, None)
        except Exception, e:
            print str(e)
            return (str(e), 400, None)

    @route('/<id>', methods=['POST'])
    def post_id(self, id):
        return ('Not implmented', 405, None)
            
    def delete(self):
        try:
            self.docs.remove()
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
            self.docs.remove(ObjectId(id))
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
                doc['updated_at'] = rightnow()

            #empty the collection
            self.docs.remove()
            
            # add new docs
            ids = self.docs.insert(docs)
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
            doc['updated_at'] = rightnow()
            
            rid = self.docs.save(doc)
            assert(ObjectId(id) == rid)
            
            if rid:
                return (request.url, 200, {'Content-Location': request.url})
            else:
                return ('data was not updated', 500, None)
        except Exception, e:
            return (str(e), 500, None)


## utils

def dump(o):
    import werkzeug
    if type(o) == werkzeug.routing.Map:
        for r in o.iter_rules():
            print "%24s %s" % ('|'.join(r.methods), r)


def rightnow():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
