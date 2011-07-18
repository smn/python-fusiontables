from setuptools import setup, find_packages

setup(
    name = "python-fusiontables",
    version = "0.1",
    url = 'http://github.com/smn/python-fusiontables',
    license = 'MIT',
    description = "Python client for Google Fusion Tables",
    long_description = open('README.rst', 'r').read(),
    author = 'Simon de Haan',
    author_email = "simon@praekeltfoundation.org",
    packages = find_packages(),
    install_requires = [
        'oauth2',
        'httplib2',
    ],
)

