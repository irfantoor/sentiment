#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/08
# Author: Irfan TOOR
# file : __init__.py

# from typing import List
from sentiment.model import Model
from sentiment.pipeline import Pipeline
from sentiment import backend, transformer, ui, tests, text
from sentiment.setting import PROJECT, VERSION

__author__: str = 'Irfan TOOR'
__name__: str = PROJECT
__email__: str = 'email@irfantoor.com'
__version__: str = '.' . join(map(str, VERSION))

__all__ = ['Model','Pipeline', 'backend','transformer','ui', 'tests', 'text']
