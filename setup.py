import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='flask-lazyapi',
    version='0.3a',
    url='https://github.com/colwilson/flask-lazyapi',
    license='BSD',
    author='Col Wilson',
    author_email='colwilson@bcs.org',
    description='A Simple, Restful MongoDB Server built on Flask and Flask-Classy',
    long_description=read('README.md'),
    py_modules=['flask_lazyapi'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Classy',
        'pymongo'
    ],
    test_suite='test_lazyapi',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Database :: Front-Ends'        
        ]
    
)

