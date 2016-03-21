# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.0.1',
    description='Sample package for Python-Guide.org',
    long_descriptoin=readme,
    author='Jason Wee',
    author_email='peichieh@gmail.com',
    url='https://github.com/jasonwee/common-util-py',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
