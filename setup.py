from setuptools import setup

setup(
    name='flask-lazyapi',
    version='0.3',
    url='https://github.com/colwilson/flask-lazyapi',
    license='BSD',
    author='Col Wilson',
    author_email='colwilson@bcs.org',
    description='A Simple, Restful MongoDB Server built on Flask and Flask-Classy',
    long_description=__doc__,
    py_modules=['flask_lazyapi'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Classy',
        'pymongo'
    ],
    test_suite='test_lazyapi'
)

