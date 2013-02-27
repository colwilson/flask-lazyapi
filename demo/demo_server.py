#!/usr/bin/env python

from flask import Flask
import lazy

class Answers(lazy.API): pass

class Questions(lazy.API): db = "myquestionsdatabase"
    
app = Flask(__name__)

Answers.register(app)
Questions.register(app)

if __name__ == '__main__':
    app.run(debug=True)




  