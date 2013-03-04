lazyapi
=======

A REST interface for MongoDB that runs on your flask development server while you write the app.
Virtually zero config, no schemas and useless in the real world. Much like myself. 

Install the module

    pip install lazyapi

Write a server.py

    #!/usr/bin/env python

    from flask import Flask
    import flask_lazyapi as lazy

    class Answers(lazy.API): pass

    app = Flask(__name__)

    Answers.register(app)

    if __name__ == '__main__':
        app.run(debug=True)

Insert some answers

    curl -X POST -H "content-type: application/json" \
        http://127.0.0.1:5000/answers/ \
        --data "{\"number\":47}"

    {"_id": {"$oid": "510cd66c9537bd71c285fd3a"}, "number": 47}

    curl -X POST -H "content-type: application/json" \
        http://127.0.0.1:5000/answers/ \
        --data "{\"day\": \"Tuesday\"}"

    {"_id": {"$oid": "510cd66c9537bd71c285fd3b"}, "day": "Tuesday"}


Get a listing of what's in there

    curl -X GET -H "content-type: application/json" \
        http://127.0.0.1:5000/answers/

    {"answers": ["http://127.0.0.1:5000/answers/510cd66c9537bd71c285fd3a", "http://127.0.0.1:5000/answers/510cd66c9537bd71c285fd3b"]}


Fetch a specific answer url

    curl -X GET -H "content-type: application/json" \
        http://127.0.0.1:5000/answers/510cd66c9537bd71c285fd3a

    {"_id": {"$oid": "510cd66c9537bd71c285fd3a"}, "number": 47}


Alter the answer and update it

    curl -X PUT -H "content-type: application/json" \
        http://127.0.0.1:5000/answers/510cd66c9537bd71c285fd3a \
        --data "{\"_id\": {\"\$oid\": \"510cd66c9537bd71c285fd3a\"}, \"number\": 3.142}"


    {"_id": {"$oid": "510cd66c9537bd71c285fd3a"}, "number": 3.142}


By default the database name will be entity name + db, e.g.

    class Answers(lazy.API): pass

will use a db called 'answersdb', but you specify that if you want

    class Answers(lazy.API): db = 'mydb'

will use a db called 'mydb'.


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
* A schema would be a nice optional extra
* Search criteria? only for GET surely?
* OPTIONS are never handled
* check for duplicates? return 409? wikipedia just says "The PUT and DELETE methods are idempotent methods."
* block all requests not from localhost?
