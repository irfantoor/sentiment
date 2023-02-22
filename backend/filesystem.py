#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/02/22
# Author: Irfan TOOR
# file : backend/filesystem.py

from abc import ABC
import os
import re

class FileSystem(ABC):
    _root = ''

    def __init__(self, root:os.path) -> None:
        if not os.path.exists(root):
            raise Exception(f'path : {root}, does not exist')

        self._root = root

    def _normalize(self, path):
        return path.lstrip('/').rstrip('/')

    def ls(self, path='', re_filter=None):
        ls = os.listdir(os.path.join(self._root, self._normalize(path)))
        if re_filter is None:
            return ls

        ll = []
        patern = re.compile(re_filter)
        for item in ls:
            if patern.match(item):
                ll.append(item)

        return ll

    def load(self, model_name:str):
        pass

    def save(self, model_name:str):
        pass
