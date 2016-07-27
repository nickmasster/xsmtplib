#! /usr/bin/env python

'''A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

from xsmtplib import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xsmtplib',
    version=__version__,

    description='An extension of standard smtplib, which supports proxy tunneling',
    long_description=long_description,

    url='https://github.com/nickmasster/xsmtplib',

    author='Nick M.',
    author_email='nickmasster@users.noreply.github.com',

    license='GPL v3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='smtp proxy email socks4 socks5 http',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'PySocks==1.5.7'
    ]
)
