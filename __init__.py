#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/08
# Author: Irfan TOOR
# file : __init__.py

# from typing import List
from .model import Model
from .pipeline import Pipeline
from . import backend, transformer, ui
from .setting import PROJECT, VERSION

__author__: str = 'Irfan TOOR'
__name__: str = PROJECT
__email__: str = 'email@irfantoor.com'
__version__: str = '.' . join(map(str, VERSION))

__all__ = ['Model','Pipeline', 'backend','transformer','ui']
