#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : setup.py
#  Author      : Feather.et.ELF <fledna@qq.com>
#  Created     : Thu Jun 09 09:51:28 2011 by Feather.et.ELF
#  Copyright   : Feather Workshop (c) 2011
#  Description : Renren API bingding
#  Time-stamp: <2011-06-09 10:35:37 andelf>


#from distutils.core import setup
from setuptools import setup, find_packages
import os, sys

lib_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, lib_path)

from renren import version

__doc__ = """
renren.com is a sns service that is popular among Chinese.

This is the SDK tools for renren.com, written by @andelf.

NOTE: this is a thrid party SDK, use at your risk.
"""

setup(name = "pyrenren",
      version = version,
      author = "andelf",
      author_email = "andelf@gmail.com",
      description = ("renren.com API SDK for python"),
      license = "MIT",
      keywords= "renren sns library xiaonei api",
      url="http://github.com/andelf/pyrenren",
      packages = ['renren'],
      long_description = __doc__,
      classifiers = [
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Natural Language :: Chinese (Simplified)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.0",
          "Programming Language :: Python :: 3.1",
          "Programming Language :: Python :: 3.2",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
          "Topic :: Utilities"
          ],
      zip_safe = True,
      install_requires = [
          "httplib2 >= 0.6.0",
          ],
      )

