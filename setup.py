#!/usr/bin/env python
import http_shrinkwrap.__init__ as init
from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='http_shrinkwrap',
    version=init.__version__,
    description='A command line tool to minimize curl requests.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    keywords='curl pentest http cli poc',
    author='zrthstr',
    author_email='zrth1k@gmail.com',
    url='https://github.com/zrthstr/http_shrinkwrap',
    platforms='any',
        classifiers=[
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Internet',
            'Topic :: Security',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: Browsers',
            'Topic :: System :: Networking',
            'Topic :: Utilities',
        ],
    entry_points={
        'console_scripts': [
            'http-shrinkwrap = http_shrinkwrap.bin:main',
        ],
    },
    install_requires=['uncurl', 'curlify', 'requests', 'loguru'],
    packages=find_packages(exclude=("tests", "tests.*", "test")),
)
