#!/usr/bin/env python

"""
Call distutils to install Mobius.
"""

from setuptools import setup, find_packages

setup(
    name='mobius',
    version='0.1.1',
    author='James Ladd Jr',
    author_email='mobius.search@gmail.com',
    packages=find_packages(exclude=['mobius.tests']),
    url='https://github.com/jladdjr/mobius',
    license='GPLv2',
    description='A micro search engine',
    long_description=open('README').read(),
    classifiers=[
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 1 - Planning"
    ],
    keywords='web search',
    install_requires=['lxml', 'requests', 'xmlrunner', 'mock']
)
