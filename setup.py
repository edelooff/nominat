#!/usr/bin/python

import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.rst')).read()


setup(
    name='nominat',
    version='0.2',
    author='Elmer de Looff',
    author_email='elmer.delooff@gmail.com',
    description='Case-insensitive case-preserving variable name mangler',
    long_description=README,
    url='http://variable-scope.com',
    keywords='name mangling anonymify ',
    classifiers=[
        "Programming Language :: Python"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=[
        'pytest']
)
