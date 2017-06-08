# -*- coding: utf-8 -*-
import codecs
import os.path
from setuptools import setup

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(PROJECT_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='restQL',
    version='0.1.0',
    py_modules=['restQL'],
    install_requires=[
        'python-box==3.0.1',
        'requests[security]==2.17.3',
        'six==1.10.0'
    ],
    test_suite='tests',
    tests_require=[
        'mock==2.0.0; python_version == "2.7"',
        'pytest==3.1.1',
        'pytest-cov==2.5.1',
        'tox==2.7.0'
    ],
    url='https://github.com/thulio/restQL-python',
    license='MIT',
    author='Thúlio Costa',
    author_email='contact@thul.io',
    description="A restQL client for Python 2 and 3",
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)