flask-lazyapi
=============   

A REST interface for MongoDB that runs on your flask development server while you write the app.
Virtually zero config, no schemas and useless in the real world. Much like myself. 

Install
-------

    pip install flask-lazyapi

Write a server.py
-----------------

    #!/usr/bin/env python

    from flask import Flask
    import flask_lazyapi as lazy

    class Answers(lazy.API): pass

    app = Flask(__name__)

    Answers.register(app)

    if __name__ == '__main__':
        app.run(debug=True)

Empty your database
-------------------

    curl -X DELETE -H "content-type: application/json" http://127.0.0.1:5000/answers/

Insert some answers
-------------------

    curl -X POST -H "content-type: application/json" http://127.0.0.1:5000/answers/ --data "{\"number\":47}"

    http://127.0.0.1:5000/answers/51351b989537bd2ee894db12

    curl -X POST -H "content-type: application/json" http://127.0.0.1:5000/answers/ --data "{\"day\": \"Tuesday\"}"

    http://127.0.0.1:5000/answers/51351b989537bd2ee894db13


Get a listing of what's in there
--------------------------------

    curl -X GET -H "content-type: application/json" http://127.0.0.1:5000/answers/

    {
        "answers": [
            "http://127.0.0.1:5000/answers/51351b989537bd2ee894db12",
            "http://127.0.0.1:5000/answers/51351bc49537bd2ee894db13"
        ]
    }


Query what's in there
--------------------------------

    curl -X GET -H "content-type: application/json" http://127.0.0.1:5000/answers/ --data "{\"day\": \"Tuesday\"}"

    {
        "answers": [
            "http://127.0.0.1:5000/answers/51351bc49537bd2ee894db13"
        ]
    }


Fetch a specific answer entity
------------------------------

    curl -X GET -H "content-type: application/json" http://127.0.0.1:5000/answers/51351b989537bd2ee894db12

    {
        "_id": {"$oid": "51351b989537bd2ee894db12"},
        "created_at": {"$date": 1362434968632},
        "updated_at": {"$date": 1362434968632},
        "number": 47
    }


Modify or replace answer entities
---------------------------------

The rules say that a RESTful API should use PUT to completely replace an entity and PATCH to
update parts of it, but since there's no schema to check the objects against, who can tell? So in this implementation,
you can use PUT to replace the whole collection and PUT or PATCH to replace/modify an entity.

    curl -X PUT -H "content-type: application/json" http://127.0.0.1:5000/answers/51351b989537bd2ee894db12 \
        --data "{\"_id\": {\"\$oid\": \"51351b989537bd2ee894db12\"}, \"number\": 3.142}"


    http://127.0.0.1:5000/answers/51351b989537bd2ee894db12


    curl -X PATCH -H "content-type: application/json" http://127.0.0.1:5000/answers/51351b989537bd2ee894db12 \
        --data "{\"_id\": {\"\$oid\": \"51351b989537bd2ee894db12\"}, \"number\": 3.142}"


    http://127.0.0.1:5000/answers/51351b989537bd2ee894db12


Database Names
--------------

By default the database name will be entity name + db, e.g.

    class Answers(lazy.API): pass

will use a db called 'answersdb', but you specify that if you want

    class Answers(lazy.API): db = 'mydb'

will use a db called 'mydb'.


API Versioning
--------------

If you want to version your interface you can use the normal Blueprint mechanism

    #!/usr/bin/env python

    from flask import Flask, Blueprint
    import flask_lazyapi as lazy

    class Answers(lazy.API): pass

    app = Flask(__name__)

    version = "v1.0"
    bp = Blueprint(version, __name__)
    Answers.register(app)
    app.register_blueprint(bp, url_prefix="/%s" % version)

    if __name__ == '__main__':
        app.run(debug=True)


TODO
----
* A schema would be a nice optional extra
* OPTIONS are never handled
* check for duplicates? return 409? wikipedia just says "The PUT and DELETE methods are idempotent methods."
* block all requests not from localhost?
