#!/usr/bin/env python

from flask import Flask
from lorna import LornaView

class ArticlesView(LornaView): pass


app = Flask(__name__)

ArticlesView.register(app)


if __name__ == '__main__':
    app.run(debug=True)


