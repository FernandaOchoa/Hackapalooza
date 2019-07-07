from setuptools import setup, find_packages 
from codecs import open 
from os import path 
here = path.abspath(path.dirname(__file__)) 

setup(
    name='hacka-palooza',
    version='1.0.0',
    description='Python Flask app as webhook for a chatbot that analizes data from users given their twitter',
    license='Apache-2.0'
)
