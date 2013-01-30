from setuptools import setup

setup(name='Lorna',
    version='0.1',
    description='Lorna Restful MongoDB Server',
    author='Col Wilson',
    author_email='colwilson@bcs.org',
    packages=['lorna'],
    include_package_data=True,
    zip_safe=False,
    test_suite = "lorna.testsuite.rest_tests",
    install_requires=[
        "Flask==0.9",
        "Flask-Classy==0.5.2",
        "Jinja2==2.6",
        "Werkzeug==0.8.3",
        "anyjson==0.3.3",
        "argparse==1.2.1",
        "coverage==3.6",
        "distribute==0.6.24",
        "nose==1.2.1",
        "pymongo==2.4.2",
        "wsgiref==0.1.2"
    ]
)

    