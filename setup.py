#!/usr/bin/env python
from setuptools import setup


setup(
    name='kitchen',
    version='0.01',
    description='Kitchen Shard',
    author='gfreezy',
    author_email='gfreezy@gmail.com',
    install_requires=[
        'peewee',
        'bottle',
        'pymysql',
        'gunicorn',
        'gevent',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
