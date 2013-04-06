'''
A REST interface for MongoDB that runs on your flask development server while you write the app.
Virtually zero config, no schemas and useless in the real world. Much like myself. 

'''

#from distutils.core import setup
from setuptools import setup

setup   (
    name = 'flask-lazyapi',
    version = '0.4.8',
    license = 'BSD',
    description = 'A Simple, Restful MongoDB Server built on Flask and Flask-Classy',
    long_description = __doc__,
    url = 'https://github.com/colwilson/flask-lazyapi',

    author = 'Col Wilson',
    author_email = 'colwilson@bcs.org',

    platforms = 'any',
    py_modules=['flask_lazyapi'],

    install_requires = [
        'Flask==0.9',
        'Flask-Classy==0.5.2',
        'pymongo==2.4.2',
        'pytz==2013b' ],

    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules' ]
    
)

