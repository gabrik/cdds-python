#!/usr/bin/env python3

from setuptools import setup

       
setup(
    name='python-dds',
    version='0.1.1',
    packages=['pydds', ],
    author='kydos',
    url='https://github.com/atolab/python-cdds',
    install_requires=['jsonpickle'],
    py_modules = ['pydds.py_dds_utils'],
)
