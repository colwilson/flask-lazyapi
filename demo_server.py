#!/usr/bin/env python

from flask import Flask
import flask_lazyapi as lazy
import random

class AugmentedRestInterface(lazy.API):
    db = "my_database"
    
    def sorted(self, sort_by, direction):
        docs = self.docs.find().sort(sort_by, dict(asc=1,desc=-1)[direction])
        urls = [ self._resource_url(doc['_id']) for doc in docs ]
        return (dumps({self.get_route_base(): urls}), 200, None)

    def random(self):
        docs = self.docs.find()
        doc = random.choice(docs)
        url = self._resourceS_url(doc['_id'])
        return url
        
class Answers(AugmentedRestInterface): pass

class Questions(AugmentedRestInterface): pass
    
app = Flask(__name__)

Answers.register(app)
Questions.register(app)

if __name__ == '__main__':
    app.run(debug=True)




  
