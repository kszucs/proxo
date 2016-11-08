#!/usr/bin/env python
# coding: utf-8

from os.path import exists

from setuptools import setup

setup(name='proxo',
      version='1.0.2',
      description='Object proxies (wrappers) for protobuf messages',
      url='http://github.com/kszucs/proxo',
      maintainer='Krisztián Szűcs',
      maintainer_email='szucs.krisztian@gmail.com',
      license='Apache License, Version 2.0',
      keywords='protobuf dict object wrapper proxy',
      packages=['proxo'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      install_requires=['protobuf'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      zip_safe=False)
