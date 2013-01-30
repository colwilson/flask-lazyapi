#!/usr/bin/env python

from flask import Flask
import lorna

class ArticlesView(lorna.LornaView): pass


app = Flask(__name__)

ArticlesView.register(app)


if __name__ == '__main__':
    app.run(debug=True)


