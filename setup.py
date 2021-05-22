#!/usr/bin/env python
import http_shrinkwrap.__init__ as init
from setuptools import setup, find_packages

setup(
    name='http_shrinkwrap',
    #version='0.0.2', # main.__version__
    version=init.__version__,
    description='A library and commandline tool to minimize curl requests',
    author='zrthstr',
    author_email='zrth1k@gmail.com',
    url='https://github.com/zrthstr/http_shrinkwrap',
    entry_points={
        'console_scripts': [
            'uncurl = http_shrinkwrap.bin:main',
        ],
    },
    install_requires=['uncurl', 'curlify', 'requests', 'loguru'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
