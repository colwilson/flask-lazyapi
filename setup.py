import os
from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, 'README.md')) as file:
    long_description = file.read()

setup(
    name='flask-lazyapi',
    version='0.4.3',
    url='https://github.com/colwilson/flask-lazyapi',
    license='BSD',
    author='Col Wilson',
    author_email='colwilson@bcs.org',
    description='A Simple, Restful MongoDB Server built on Flask and Flask-Classy',
    long_description=long_description,
    py_modules=['flask_lazyapi'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Classy',
        'pymongo'
    ],
    package_data = {
        '': ['*.md']
        },
    test_suite='test_lazyapi',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Database :: Front-Ends'        
        ]
    
)

