#!/usr/bin/env python3

from setuptools import setup

       
setup(
    name='python-dds',
    version='0.1.1',
    packages=['cdds', ],
    author='kydos',
    url='https://github.com/atolab/python-cdds',
    install_requires=['jsonpickle'],
    py_modules = ['cdds.py_dds_utils'],
)
